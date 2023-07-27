#!/bin/bash

cd "$(dirname "$0")/.."

# Gets all the .wav files

files=()
src="./samples"
for file in $src/*.wav; do
    files+=("$file")
done

# Calculates n cycles of execution for all the samples

n=$1
start=$(date +%s%N)
for ((i = 0; i < n; i++)); do
    for f in "${files[@]}"; do
        "./src/main.out" "$f" >> /dev/null
    done
done
end=$(date +%s%N)

execution_time=$((end - start))
average=$((execution_time / n / 1000000))
rm output.wav
echo -e "\033[0;33;91mAverage execution time for $n cycles:\033[0m \033[0;31m$average ms\033[0m"
