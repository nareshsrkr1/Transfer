#!/bin/bash

# Function to extract the date timestamp from a file name
extract_datestamp() {
    filename="$1"
    # Extract the datestamp (YYYYMMDD) from the filename
    datestamp=$(echo "$filename" | grep -oP '\d{8}')
    echo "$datestamp"
}

# Get a list of unique datestamps from the filenames in the directory
datestamps=$(find . -type f -name "*sr14*.dat" -o -name "*sr14*.ctl" | while read -r file; do extract_datestamp "$file"; done | sort -u)

# Loop through each datestamp
for datestamp in $datestamps; do
    # Create a tarball for files with the current datestamp
    tar_filename="${datestamp}.tar.gz"
    find . -type f \( -name "*sr14*${datestamp}.dat" -o -name "*sr14*${datestamp}.ctl" \) -exec tar -rvf "$tar_filename" {} \;
done

# Compress the tarballs
for datestamp in $datestamps; do
    tar_filename="${datestamp}.tar"
    gzip "$tar_filename"
done
