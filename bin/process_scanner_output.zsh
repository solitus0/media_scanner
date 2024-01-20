#!/bin/zsh

# Retrieve directories from environment variables
encodes_temp_dir="${ENCODES_TEMP_DIR}"
originals_dir="${ORIGINALS_DIR}"
presets_dir="${PRESETS_DIR}"

# Exit if any required directory does not exist
if [ ! -d "$encodes_temp_dir" ] || [ ! -d "$originals_dir" ] || [ ! -d "$presets_dir" ]; then
    echo "One or more required directories do not exist."
    exit 1
fi

json_array=$@

# Convert JSON array to newline-separated paths
IFS=$'\n' file_paths=($(echo $json_array | jq -r '.[]'))

for file in "${file_paths[@]}"; do
    echo "Processing file: $file"

    filename=$(basename "$file")
    HandBrakeCLI --input "$file" --output "${encodes_temp_dir}/${filename}" --preset-import-file "${presets_dir}/anime_opus.json" -Z "Anime opus"
    if [ $? -ne 0 ]; then
        echo "Handbrake failed to encode file: $file"
        continue
    fi

    echo "Moving original file to ${originals_dir}/${filename}"
    mv "$file" "${originals_dir}/${filename}"

    echo "Moving encoded file ${encodes_temp_dir}/${filename} to original file location ${file}"
    mv "${encodes_temp_dir}/${filename}" "$file"
done
