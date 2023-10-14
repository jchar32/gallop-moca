import numpy as np
from gallop.biomech.process import lowpass_filter
import pytest
from scipy import signal


@pytest.fixture
def testsignals():
    Fs = 1000  # sample rate
    dt = 1 / Fs  # time step
    stop_time = 10  # time of signal in sec
    t = np.arange(0, stop_time - dt, dt)
    Fc = 2  # freq of wave in hz

    x_pure = np.sin(2 * np.pi * Fc * t)
    x_mixed = np.sin(2 * np.pi * Fc * t) + np.sin(2 * np.pi * 2 * (Fc + 5) * t)
    return x_pure, x_mixed, Fc, Fs


def test_lowpass_filter_1d():
    # Test 1D data
    data = np.random.rand(1000)
    filtered_data = lowpass_filter(data, cutoff=10, Fs=100, order=2)
    assert filtered_data.shape == data.shape


def test_lowpass_filter_2d():
    # Test 2D data
    data = np.random.rand(10, 1000)
    filtered_data = lowpass_filter(data, cutoff=10, Fs=100, order=2)
    assert filtered_data.shape == data.shape


def test_lowpass_filter_invalid_data():
    # Test invalid data
    data = np.array([1, 2, np.nan, 4, 5])
    filtered_data = lowpass_filter(data, cutoff=10, Fs=100, order=2)
    assert np.isnan(filtered_data).any()


def test_lowpass_filter_long_array():
    # Test long array of data
    data = np.random.rand(10000)
    filtered_data = lowpass_filter(data, cutoff=10, Fs=100, order=2)
    assert filtered_data.shape == data.shape


def test_lowpass_filter_removehighfreq(testsignals):
    x_pure, x_mixed, Fc, Fs = testsignals
    xfilt = lowpass_filter(x_mixed, cutoff=Fc + 1, Fs=Fs, order=6)

    pmixed = np.abs(np.fft.fft(x_mixed)) ** 2
    dt = 1 / Fs
    freqsmixed = np.abs(np.fft.fftfreq(len(pmixed), dt))
    idx = signal.find_peaks(pmixed, threshold=np.mean(pmixed) * 1.25)[0]
    peak_freqs_mixed = np.unique(freqsmixed[idx])

    ppure = np.abs(np.fft.fft(x_pure)) ** 2
    dt = 1 / Fs
    freqs_pure = np.abs(np.fft.fftfreq(len(ppure), dt))
    idx_pure = signal.find_peaks(ppure, threshold=np.mean(ppure) * 1.25)[0]
    peak_freqs_pure = np.unique(freqs_pure[idx_pure])

    pfilt = np.abs(np.fft.fft(xfilt)) ** 2
    dt = 1 / Fs
    freqs_filt = np.abs(np.fft.fftfreq(len(pfilt), dt))
    idx_filt = signal.find_peaks(pfilt, threshold=np.mean(pfilt) * 1.25)[0]
    peak_freqs_filt = np.unique(freqs_filt[idx_filt])

    assert peak_freqs_pure.shape[0] == 1, "Pure signal should have one peak"
    assert peak_freqs_mixed.shape[0] == 2, "Mixed signal should have two peaks"
    assert peak_freqs_filt.shape[0] == 1, "Filtered signal should have one peak"
    assert peak_freqs_pure.shape[0] == peak_freqs_filt.shape[0], "Filtered signal should have same number of peaks as pure signal"
