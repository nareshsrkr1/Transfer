#!/bin/bash

# Check if a date argument is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <YYYYMMDD>"
  exit 1
fi

# Input date argument and calculate the previous day's date
ARG_DATE="$1"
PREV_DATE=$(date -d "$ARG_DATE -1 day" +%Y%m%d)

# Define file directory and find the corresponding file
FILE_DIR="/1sr14/QFC/PRD/data/recv"
OLD_FILE=$(find "$FILE_DIR" -name "1MCR_${PREV_DATE}.dat")

if [ -z "$OLD_FILE" ]; then
  echo "File for date $PREV_DATE not found in $FILE_DIR"
  exit 1
fi

# Construct new file name and backup file name
NEW_FILE="${FILE_DIR}/1MCR_${ARG_DATE}.dat"
BACKUP_FILE="${OLD_FILE}.bak"

# Take a backup of the original file
cp "$OLD_FILE" "$BACKUP_FILE"
echo "Backup created: $BACKUP_FILE"

# Replace the date in the first column and save to the new file
awk -v old_date=$(date -d "$PREV_DATE" +'%m/%d/%Y') \
    -v new_date=$(date -d "$ARG_DATE" +'%m/%d/%Y') \
    'BEGIN {OFS=FS="|"} 
     {gsub(old_date, new_date, $1); print}' "$OLD_FILE" > "$NEW_FILE"

echo "New file created: $NEW_FILE"
