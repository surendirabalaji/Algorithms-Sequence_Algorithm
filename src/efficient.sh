#!/bin/bash
# efficient.sh — runs the efficient sequence alignment program

set -e  

if command -v python3 &> /dev/null; then
    PY="python3"
elif command -v python &> /dev/null; then
    PY="python"
else
    echo "Error: Python not found!"
    exit 1
fi

echo "Running efficient sequence alignment algorithm..."
echo "  Input:  $1"
echo "  Output: $2"

# Run the Python script
$PY efficient.py "$1" "$2"

echo "Execution finished successfully."
