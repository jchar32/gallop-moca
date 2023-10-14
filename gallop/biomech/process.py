import numpy as np
from scipy.signal import butter, filtfilt


def lowpass_filter(data: np.ndarray, cutoff: float, Fs: int, order: int = 2) -> np.ndarray:
    """perform simple lowpass butterworth filter on signal that may contain NaNs

    Args:
        data (ndarray): data to be filtered. Can be 1D or 2D. If 2D, the first dimension is considered individual signals and filtered independently
        cutoff (int): cut off frequecy of filter
        Fs (int): sampling rate of data to be filtered
        order (int, optional): order of the single-pass filter. filtfilt resulting order is twice this value. Defaults to 2.

    Returns:
        ndarray: filtered data in same format as input data. If input data contains NaNs, the output data will contain NaNs in the same locations
    """
    b, a = butter(order, cutoff, btype="low", analog=False, fs=Fs)
    if np.sum(~np.isfinite(data)) == 0:
        return filtfilt(b, a, data, method="pad", padlen=max(data.shape) - 1)

    # init output array
    data_out = np.full(data.shape, np.nan)

    if np.ndim(data) == 1:
        non_nan_idx = np.where(np.isfinite(data))[0]
        clean_signal = data[non_nan_idx]

        y = filtfilt(b, a, clean_signal, method="pad", padlen=max(clean_signal.shape) - 1)
        np.put(data_out, non_nan_idx, y)
    else:
        # iterate over each axis
        for axis in range(data.shape[0]):
            non_nan_idx = np.where(np.isfinite(data[axis, :]))[0]
            clean_signal = data[axis, non_nan_idx]

            y = filtfilt(b, a, clean_signal, method="pad", padlen=max(clean_signal.shape) - 1)
            np.put(data_out[axis, :], non_nan_idx, y)

    return data_out
