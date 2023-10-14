import pytest
import xarray as xr

from gallop.io import read


@pytest.fixture
def get_data_path():
    return "./dev data/overground/test_case/Static.c3d"


def test_read_c3d_badpath():
    with pytest.raises(ValueError) as excinfo:
        read.c3d("bad_path")
    assert str(excinfo.value) == "File path does not exist."


def test_read_c3d_returnformat(get_data_path):
    trial = read.c3d(get_data_path)
    markers = trial.markers
    raw_analog = trial.raw_analog
    assert isinstance(markers, xr.DataArray)
    assert isinstance(raw_analog, xr.DataArray)


def test_read_c3d_components(get_data_path):
    trial = read.c3d(get_data_path)
    markers = trial.markers
    raw_analog = trial.raw_analog

    assert "axis" in markers.dims
    assert "channel" in markers.dims
    assert "time" in markers.dims
    assert "channel" in raw_analog.dims
    assert "plate" in raw_analog.dims
    assert "time" in raw_analog.dims
    assert markers.ndim == 3
    assert raw_analog.ndim == 3
