#!/bin/zsh

while IFS= read -r file; do
    if [ ! -d "/encodes" ]; then
        echo "Creating /encodes directory"
        mkdir /encodes
    fi

    echo "Processing file: $file"

    filename=$(basename "$file")
    HandBrakeCLI --input "$file" --output "/encodes/${filename}" --preset-import-file /var/cli/presets/anime_opus.json -Z "Anime opus"

    if [ ! -d "/originals" ]; then
        echo "Creating /originals directory"
        mkdir /originals
    fi

    echo "Moving original file to /originals/${filename}"
    mv "$file" "/originals/${filename}"

    echo "Moving encoded file /encodes/${filename} to original file location ${file}"
    mv "/encodes/${filename}" "$file"
done

echo "All files processed."
