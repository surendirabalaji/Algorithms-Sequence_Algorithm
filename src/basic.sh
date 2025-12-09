#!/bin/bash
# basic.sh — runs the basic sequence alignment program

set -e 

if command -v python3 &> /dev/null; then
    PY="python3"
elif command -v python &> /dev/null; then
    PY="python"
else
    echo "Error: Python not found!"
    exit 1
fi

echo "Running basic sequence alignment algorithm..."
echo "  Input:  $1"
echo "  Output: $2"

# Run the Python script
$PY basic.py "$1" "$2"

echo "Execution finished successfully."
