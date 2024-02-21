#!/bin/bash

# Check if a filename is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename=$1

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File $filename not found!"
    exit 1
fi

# Read the file line by line, trim leading/trailing spaces, and echo non-empty lines
while IFS= read -r line; do
    # Trim leading and trailing whitespace
    trimmed_line=$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    
    # Check if the trimmed line is not empty
    if [ -n "$trimmed_line" ]; then
        echo "$trimmed_line"
    fi
done < "$filename"
