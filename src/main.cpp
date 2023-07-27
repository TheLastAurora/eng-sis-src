/*

Sistemas de Cancelamento Ativo de Ruídos Acústicos - Módulo de Inversão de Ondas Sonoras

*/


#include <iostream>
#include <fstream>
#include <vector>
#include <thread>

using namespace std;

const string outputFileName = "output.wav";

struct WavHeader {
    char chunkId[4];
    uint32_t chunkSize;
    char format[4];
    char subChunk1Id[4];
    uint32_t subChunk1Size;
    uint16_t audioFormat;
    uint16_t numChannels;
    uint32_t sampleRate;
    uint32_t byteRate;
    uint16_t blockAlign;
    uint16_t bitsPerSample;
    char subChunk2Id[4];
    uint32_t subChunk2Size;
};

void invertAudio(vector<int16_t>& audioData, size_t start, size_t end) {
    for (size_t i = start; i < end; ++i) {
        audioData[i] = -audioData[i];
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " <input_file_path>" << endl;
        return 1;
    }

    const string inputFileName = argv[1];

    ifstream inputFile(inputFileName, ios::binary);

    if (!inputFile) {
        cerr << "Error opening file: " << inputFileName << endl;
        return 1;
    }

    WavHeader header;
    inputFile.read(reinterpret_cast<char*>(&header), sizeof(WavHeader));

    if (string(header.chunkId, 4) != "RIFF" ||
        string(header.format, 4) != "WAVE" ||
        string(header.subChunk1Id, 4) != "fmt " ||
        header.audioFormat != 1 ||
        header.bitsPerSample != 16 ||
        string(header.subChunk2Id, 4) != "data") {
        cerr << "Invalid WAV file format." << endl;
        return 1;
    }

    vector<int16_t> audioData(header.subChunk2Size / sizeof(int16_t));
    inputFile.read(reinterpret_cast<char*>(audioData.data()), header.subChunk2Size);

    inputFile.close();

    const size_t numThreads = thread::hardware_concurrency();
    vector<thread> threads;

    const size_t samplesPerThread = audioData.size() / numThreads;

    for (size_t i = 0; i < numThreads; ++i) {
        size_t start = i * samplesPerThread;
        size_t end = (i == numThreads - 1) ? audioData.size() : (i + 1) * samplesPerThread;

        threads.emplace_back(invertAudio, ref(audioData), start, end);
    }

    for (auto& thread : threads) {
        thread.join();
    }

    ofstream outputFile(outputFileName, ios::binary);

    if (!outputFile) {
        cerr << "Error opening file for writing: " << outputFileName << endl;
        return 1;
    }

    outputFile.write(reinterpret_cast<const char*>(&header), sizeof(WavHeader));
    outputFile.write(reinterpret_cast<const char*>(audioData.data()), header.subChunk2Size);

    outputFile.close();

    cout << "Audio inversion complete. Output written to: " << outputFileName << endl;

    return 0;
}

