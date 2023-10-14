import numpy as np
from gallop.biomech.process import lowpass_filter


def test_lowpass_filter_with_good_data():
    # Test lowpass_filter with good data
    data = np.array([1, 2, 3, 4, 5])
    cutoff = 2
    Fs = 10
    expected_output = np.array([1.00000000e00, 1.00000000e00, 1.00000000e00, 1.00000000e00, 9.99999999e-01])
    assert np.allclose(lowpass_filter(data, cutoff, Fs), expected_output)


def test_lowpass_filter_with_bad_data():
    # Test lowpass_filter with bad data
    data = np.array([1, 2, np.nan, 4, 5])
    cutoff = 2
    Fs = 10
    expected_output = np.array([1.00000000e00, 1.00000000e00, np.nan, 1.00000000e00, 9.99999999e-01])
    assert np.allclose(lowpass_filter(data, cutoff, Fs), expected_output)


def test_lowpass_filter_with_2d_data():
    # Test lowpass_filter with 2D data
    data = np.array([[1, 2, 3], [4, 5, np.nan], [7, 8, 9]])
    cutoff = 2
    Fs = 10
    expected_output = np.array(
        [[1.00000000e00, 1.00000000e00, 1.00000000e00], [1.00000000e00, 1.00000000e00, np.nan], [1.00000000e00, 1.00000000e00, 1.00000000e00]]
    )
    assert np.allclose(lowpass_filter(data, cutoff, Fs), expected_output)
