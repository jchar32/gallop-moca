import os

import ezc3d
import numpy as np
import xarray as xr

from gallop.biomech import transforms
from gallop.io import Trial, ui


def c3d(data_path: str = ""):
    """ingest and parse a c3d file into marker and analog data xarrays.
    Relies on the ezc3d package to read in the c3d file prior to parsing.
    Assumptions:
        c3d file contains both marker and analog data
        force plates are AMTI (type 2 / 4)
        marker data are stored in xyz format per marker
        analog data are stored in in 6 channels (fx, fy, fz, mx, fy, mz)

    Args:
        data_path (str): full file path to c3d file

    Returns:
        DataArray: separate xarray DataArrays for markers and raw_analog data
    """
    if data_path == "":
        data_path = ui.get_path(wildcard="*.c3d")

    if data_path == "":
        raise ValueError("No file path selected for c3d file.")

    if os.path.exists(data_path) is False:
        raise ValueError("File path does not exist.")

    # Read in c3d file
    c3d_data = ezc3d.c3d(data_path)

    # Parse c3d file into markers and analog data
    markers, raw_analog = parse_c3d(c3d_data)

    # place marker and raw_analog into class
    trial = Trial.Trial(markers, raw_analog)
    return trial


def parse_c3d(c3d_data):
    """custom parseing of a c3d file into marker and analog data xarrays. This should be reasonably universal though it testing on different motion catpure systems is limited. This function is called by the c3d function.

    Args:
        c3d_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    # ** VIDEO DATA - Compile comonents from c3d
    point_params = {}
    for param in c3d_data["header"]["points"]:
        point_params[param] = c3d_data["header"]["points"][param]

    for param in c3d_data["parameters"]["POINT"]:
        try:
            point_params[param] = c3d_data["parameters"]["POINT"][param]["value"]
        except KeyError:
            continue
        if len(c3d_data["parameters"]["POINT"][param]["value"]) > 1:
            point_params[param] = c3d_data["parameters"]["POINT"][param]["value"]
        else:
            point_params[param] = c3d_data["parameters"]["POINT"][param]["value"][0]

    # ** Store video data in xarray
    marker_data = c3d_data["data"]["points"]
    axes = ["x", "y", "z", "w"]
    channel = point_params["LABELS"]
    point_collection_time_sec = point_params["last_frame"] / point_params["RATE"]
    time = list(np.array(np.linspace(0, point_collection_time_sec, point_params["last_frame"] + 1)))

    markers: xr.DataArray = xr.DataArray(
        marker_data,
        coords=[axes, channel, time],
        dims=["axis", "channel", "time"],
        attrs=point_params,
    )

    # ** ANALOG DATA - Compile comonents from c3d
    analog_params = {}
    for param in c3d_data["header"]["analogs"]:
        analog_params[param] = c3d_data["header"]["analogs"][param]

    # ** force platform configurations
    for param in c3d_data["parameters"]["FORCE_PLATFORM"]:
        try:
            analog_params[param] = c3d_data["parameters"]["FORCE_PLATFORM"][param]["value"]
        except KeyError:
            continue
        analog_params[param] = c3d_data["parameters"]["FORCE_PLATFORM"][param]["value"]

    # ** Analog data parameters
    for param in c3d_data["parameters"]["ANALOG"]:
        try:
            analog_params[param] = c3d_data["parameters"]["ANALOG"][param]["value"]
        except KeyError:
            analog_params[param] = c3d_data["parameters"]["ANALOG"][param]
            continue

        if len(c3d_data["parameters"]["ANALOG"][param]["value"]) > 1:
            analog_params[param] = c3d_data["parameters"]["ANALOG"][param]["value"]
        else:
            analog_params[param] = c3d_data["parameters"]["ANALOG"][param]["value"][0]

    # ** Check the channels to determine the number of used Force Platforms
    unused_FP_channels = [idx for idx, value in enumerate(analog_params["LABELS"]) if value == ""]
    used_FP_channels = [idx for idx, value in enumerate(analog_params["LABELS"]) if value != ""]
    num_FP_used = int(len(used_FP_channels) / 6)  # assumes 6 channels per FP

    analog_params["UNUSED_CHANNEL_IDX"] = unused_FP_channels
    analog_params["USED_CHANNEL_IDX"] = used_FP_channels
    analog_params["FP_USED"] = num_FP_used

    # ** Store analog data in xarray
    raw_analog_data = np.zeros((6, num_FP_used, analog_params["last_frame"] + 1))
    for plate in range(num_FP_used):
        if plate == 0:
            raw_analog_data[: (1 + plate) * 6, plate, :] = c3d_data["data"]["analogs"][0, : (1 + plate) * 6, :]
        else:
            raw_analog_data[: plate * 6, plate, :] = c3d_data["data"]["analogs"][0, (plate * 6) : (1 + plate) * 6, :]

    channel = ["fx", "fy", "fz", "mx", "my", "mz"]
    plate = [f"FP{i+1}" for i in range(num_FP_used)]
    analog_collection_time_sec = analog_params["last_frame"] / analog_params["frame_rate"]
    time = list(np.array(np.linspace(0, analog_collection_time_sec, analog_params["last_frame"] + 1)))

    raw_analog: xr.DataArray = xr.DataArray(
        raw_analog_data,
        coords=[channel, plate, time],
        dims=["channel", "plate", "time"],
        attrs=analog_params,
    )

    (
        raw_analog.attrs["ORIGIN_GCS"],
        raw_analog.attrs["FP_CS"],
    ) = transforms.get_fp_coordsys(raw_analog)
    return markers, raw_analog
