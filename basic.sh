#!/bin/bash

# Script to run the basic sequence alignment algorithm
# Usage: ./basic.sh [input_file] [output_file]
# If no arguments provided, runs all Datapoints/in1.txt~in15.txt

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# If no arguments provided, run all Datapoints files
if [ $# -eq 0 ]; then
    echo "No arguments provided. Running all Datapoints files (in1.txt~in15.txt)..."
    echo ""
    
    DATAPOINTS_DIR="${SCRIPT_DIR}/Data/Datapoints"
    OUTPUT_DIR="${SCRIPT_DIR}/Data/Output"
    SUCCESS_COUNT=0
    FAIL_COUNT=0
    
    # Process all input files from in1.txt to in15.txt
    for i in {1..15}; do
        INPUT_FILE="${DATAPOINTS_DIR}/in${i}.txt"
        OUTPUT_FILE="${OUTPUT_DIR}/output${i}.txt"
        
        if [ -f "${INPUT_FILE}" ]; then
            echo "Processing: in${i}.txt -> output${i}.txt"
            python3 "${SCRIPT_DIR}/src/basic.py" "${INPUT_FILE}" "${OUTPUT_FILE}"
            
            if [ $? -eq 0 ]; then
                echo "  ✓ Completed successfully"
                ((SUCCESS_COUNT++))
            else
                echo "  ✗ Failed"
                ((FAIL_COUNT++))
            fi
            echo ""
        else
            echo "Warning: ${INPUT_FILE} not found, skipping..."
            echo ""
        fi
    done
    
    echo "========================================="
    echo "Summary: ${SUCCESS_COUNT} succeeded, ${FAIL_COUNT} failed"
    echo "========================================="
    
    if [ ${FAIL_COUNT} -eq 0 ]; then
        exit 0
    else
        exit 1
    fi

# If arguments provided, run single file
elif [ $# -eq 2 ]; then
    INPUT_FILE="$1"
    OUTPUT_FILE="$2"
    
    echo "Running basic sequence alignment algorithm..."
    echo "  Input:  ${INPUT_FILE}"
    echo "  Output: ${OUTPUT_FILE}"
    echo ""
    
    python3 "${SCRIPT_DIR}/src/basic.py" "${INPUT_FILE}" "${OUTPUT_FILE}"
    
    # Check exit status
    if [ $? -eq 0 ]; then
        echo "Execution completed successfully."
    else
        echo "Execution failed."
        exit 1
    fi
else
    echo "Usage: $0 [input_file] [output_file]"
    echo "   or: $0  (runs all Datapoints/in1.txt~in15.txt)"
    exit 1
fi

