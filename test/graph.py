from scipy.io import wavfile
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import subprocess
import os


def plot_audio_samples(ax, sample, output, sample_rate, title1, title2):
    time = np.arange(len(sample)) / sample_rate

    ax[0].plot(time, sample)
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(title1)

    ax[1].plot(time, output)
    ax[1].set_xlabel("Tempo (ms)")
    ax[1].set_ylabel("Amplitude")
    ax[1].set_title(title2)


def format_y_ticks_with_two_decimals(ax):
    formatter = ticker.FormatStrFormatter("%.2f")
    ax.yaxis.set_major_formatter(formatter)


sample_rate, sample1 = wavfile.read("./samples/cenario_1.wav")
sample_rate, sample2 = wavfile.read("./samples/cenario_2.wav")
sample_rate, sample3 = wavfile.read("./samples/cenario_3.wav")

out = []
for i in range(1, 4):

    subprocess.run(
        f"cd ./src && ./main.out ../samples/cenario_{i}.wav >> /dev/null", shell=True, text=True)
    sleep(1)
    out.append(wavfile.read("./src/output.wav")[1])
    os.remove("./src/output.wav")
out1, out2, out3 = out


fig, axes = plt.subplots(3, 2, figsize=(10, 5), sharex=True, tight_layout=True)
fig.suptitle("Sample vs Output")


plot_audio_samples(axes[0], sample1, out1, sample_rate,
                   "Cenário 1", "Output 1")
plot_audio_samples(axes[1], sample2, out2, sample_rate,
                   "Cenário 2", "Output 2")
plot_audio_samples(axes[2], sample3, out3, sample_rate,
                   "Cenário 3", "Output 3")


for ax in axes.ravel():
    format_y_ticks_with_two_decimals(ax)


plt.subplots_adjust(hspace=0.4)
plt.savefig("sample_vs_output.jpg", dpi=300, bbox_inches='tight')
