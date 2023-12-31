import numpy as np
import xarray as xr


def get_fp_coordsys(raw_analog: xr.DataArray):
    """
    Calculates the force plate coordinate system in global coordinate system.

    Args:
        raw_analog (xr.DataArray): A numpy array containing raw analog data that was generated from the io.read.c3d function. This array should be of type xarray

    Returns:
        tuple: A tuple containing the force plate origin in global coordinate system and the force plate coordinate system.
    """

    num_plates = raw_analog.attrs["FP_USED"]
    fp_origin_gcs = np.zeros((3, num_plates))
    fp_cs = np.zeros((3, 3, num_plates))

    for plate in range(num_plates):
        corners = raw_analog.attrs["CORNERS"][:, :, plate]
        fp_origin_gcs[:, plate] = np.mean(corners, axis=1)

        # ** force plate to GCS
        fp_y = (corners[:, 1] - corners[:, 2]) / np.linalg.norm(corners[:, 1] - corners[:, 2])
        fp_x = (corners[:, 3] - corners[:, 2]) / np.linalg.norm(corners[:, 3] - corners[:, 2])
        fp_z = np.cross(fp_x, fp_y)
        fp_cs[:, :, plate] = np.vstack((fp_x, fp_y, fp_z))

    return (fp_origin_gcs, fp_cs)
