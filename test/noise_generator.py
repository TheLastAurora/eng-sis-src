import numpy as np
from scipy.io import wavfile
import os


def gen_constant_noise(duration: int, sample_rate: int = 44100, amplitude: float = 0.1):
    """Generates constant audio signal"""
    num_samples = int(duration * sample_rate)
    samples = np.random.uniform(-amplitude, amplitude, num_samples)
    return samples


def gen_variable_noise(duration: int, sample_rate: int = 44100, amplitude_min: float = 0.1, amplitude_max: float = 0.2):
    """Generates variable audio signal"""
    num_samples = int(duration * sample_rate)
    samples = np.random.uniform(-amplitude_max, amplitude_max, num_samples)
    amplitude_ramp = np.linspace(amplitude_min, amplitude_max, num_samples)
    samples = samples * amplitude_ramp
    return samples


def gen_noise_from_frequencies(duration: int, sample_rate: int, frequencies: list = [200, 700, 1500], amplitude: float = 0.1):
    num_samples = int(duration * sample_rate)
    samples = np.zeros(num_samples)
    time = np.arange(num_samples) / sample_rate
    for freq in frequencies:
        samples += amplitude * np.sin(2 * np.pi * freq * time)
    return samples


def gen_linear_from_frequencies(duration: int, sample_rate: int, frequencies: list = [0, 20000], amplitude: float = 0.1):
    num_samples = int(duration * sample_rate)
    samples = np.zeros(num_samples)
    time = np.arange(num_samples) / sample_rate

    
    frequency_start = frequencies[0]
    frequency_end = frequencies[-1]
    frequency_step = (frequency_end - frequency_start) / num_samples

    for i in range(num_samples):
        freq = frequency_start + i * frequency_step
        samples[i] = amplitude * np.sin(2 * np.pi * freq * time[i])

    return samples


def save_wav(filename, samples, sample_rate):
    wavfile.write(filename, sample_rate, (samples * 32767).astype(np.int16))


sample_rate = 44100
output_folder = "samples"
os.makedirs(output_folder, exist_ok=True)

sample1 = gen_constant_noise(1e-2, sample_rate, 0.1)
sample2 = gen_variable_noise(1e-2, sample_rate, 0.1, 0.4)
sample3 = gen_noise_from_frequencies(2e-2, sample_rate, [200, 400, 2500], 0.5)


save_wav(os.path.join(output_folder, "scenario_1.wav"), sample1, sample_rate)
save_wav(os.path.join(output_folder, "scenario_2.wav"), sample2, sample_rate)
save_wav(os.path.join(output_folder, "scenario_3.wav"), sample3, sample_rate)
