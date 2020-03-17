#!/bin/sh
# Put the arguments sent by Octolapse into variables for easy use
SNAPSHOT_NUMBER=$1
DELAY_SECONDS=$2
DATA_DIRECTORY=$3
SNAPSHOT_DIRECTORY=$4
SNAPSHOT_FILENAME=$5
SNAPSHOT_FULL_PATH=$6
MY_DIR="/home/pi/timelapse/"

# Check to see if the snapshot directory exists
if [ ! -d "${SNAPSHOT_DIRECTORY}" ];
then
  echo "Creating directory: ${SNAPSHOT_DIRECTORY}"
  mkdir -p "${SNAPSHOT_DIRECTORY}"
fi


python "/home/pi/photo/capture.py" "${MY_DIR}"


FILEEXT="jpg"

NEWEST=`ls -tr1d "${MY_DIR}Camera/"*.${FILEEXT} 2>/dev/null | tail -1`

if [ -z "${NEWEST}" ] ; then
    echo "No file to copy"
    exit 1
elif [ -d "${NEWEST}" ] ; then
    echo "The most recent entry is a directory"
    exit 1
else
    echo "Copying ${NEWEST}"
    cp -p "${NEWEST}" "${SNAPSHOT_FULL_PATH}"
fi

if [ ! -f "${SNAPSHOT_FULL_PATH}" ];
then
  echo "The snapshot was not found in the expected directory: '${SNAPSHOT_FULL_PATH}'." >&2 
  exit 1
fi
