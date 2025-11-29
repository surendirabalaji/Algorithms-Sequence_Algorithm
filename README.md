# Sequence Alignment Algorithm

A dynamic programming implementation for computing the minimum alignment cost between two DNA sequences.

## Overview

This project implements a sequence alignment algorithm using dynamic programming to find the optimal alignment between two DNA sequences (composed of A, C, G, T nucleotides). The algorithm minimizes the total alignment cost by considering match/mismatch costs and gap penalties.

## Algorithm

The algorithm uses the following recurrence relation:

```
OPT(i, j) = min(
    OPT(i-1, j-1) + alpha_ij,  // match/mismatch
    OPT(i-1, j) + gap,          // gap in sequence 2
    OPT(i, j-1) + gap           // gap in sequence 1
)
```

Where:
- `i, j` are indices of the two input sequences
- `alpha_ij` is the mismatch cost between characters at positions i and j
- `gap` is the gap penalty (default: 30)

### Cost Matrix

The mismatch costs between nucleotides are defined as follows:

|     | A   | C   | G   | T   |
|-----|-----|-----|-----|-----|
| **A** | 0   | 110 | 48  | 94  |
| **C** | 110 | 0   | 118 | 48  |
| **G** | 48  | 118 | 0   | 110 |
| **T** | 94  | 48  | 110 | 0   |

## Requirements

- Python 3.x
- Bash (for running the shell script)

## Project Structure

```
Algorithms-Sequence_Algorithm/
├── src/
│   └── basic.py          # Main algorithm implementation
├── Data/
│   ├── Datapoints/       # Input test files (in1.txt ~ in15.txt)
│   ├── Output/           # Generated output files (output1.txt ~ output15.txt)
│   └── SampleTestCases/  # Sample test cases
├── basic.sh              # Shell script for batch processing
├── test_basic.sh         # Test script for SampleTestCases
├── string_generator.py   # String generation utilities
└── README.md             
```

## Input Format

The input file should contain base strings and indices for string augmentation. The format supports two styles:

**Format 1 (Explicit counts):**
```
s0
j
index1
index2
...
indexj
t0
k
index1
index2
...
indexk
```

**Format 2 (Implicit lists):**
```
s0
index1
index2
...
t0
index1
index2
...
```

The algorithm will augment the base strings by inserting the string into itself at the specified indices iteratively.

Example (`in1.txt`):
```
CCAG
2
CATG
3
```

## Output Format

The output file contains a single integer representing the minimum alignment cost.

Example (`output1.txt`):
```
90
```

## Usage

### Method 1: Using the Shell Script (Recommended)

#### Run all test cases (in1.txt ~ in15.txt)

```bash
./basic.sh
```

This will:
- Process all files from `Data/Datapoints/in1.txt` to `in15.txt`
- Generate output files `output1.txt` to `output15.txt` in `Data/Output/`
- Display progress and summary statistics

#### Run a single test case

```bash
./basic.sh <input_file> <output_file>
```

Example:
```bash
./basic.sh Data/Datapoints/in1.txt result.txt
```

### Method 2: Direct Python Execution

You can also run the Python script directly:

```bash
python3 src/basic.py <input_file> <output_file>
```

Example:
```bash
python3 src/basic.py Data/Datapoints/in1.txt output.txt
```

### Testing

To test the algorithm against SampleTestCases:

```bash
./test_basic.sh
```

This will compare the computed costs with expected values from `Data/SampleTestCases/output*.txt` files.

## Examples

### Example 1: Process all datapoints

```bash
cd Algorithms-Sequence_Algorithm
./basic.sh
```

Output:
```
No arguments provided. Running all Datapoints files (in1.txt~in15.txt)...

Processing: in1.txt -> output1.txt
Minimum alignment cost: 90
Result written to /path/to/Data/Output/output1.txt
  ✓ Completed successfully

Processing: in2.txt -> output2.txt
...

=========================================
Summary: 15 succeeded, 0 failed
=========================================
```

### Example 2: Process a single file

```bash
./basic.sh Data/Datapoints/in1.txt my_output.txt
```

Output:
```
Running basic sequence alignment algorithm...
  Input:  Data/Datapoints/in1.txt
  Output: my_output.txt

Minimum alignment cost: 90
Result written to my_output.txt
Execution completed successfully.
```

## How It Works

1. **Input Parsing**: The program reads the input file and extracts base strings (s0, t0) and their respective indices.

2. **String Augmentation**: Using the `generate_string()` function, each base string is iteratively augmented by inserting itself at the specified indices. This process doubles the string length at each step.

3. **Alignment Calculation**: The augmented strings are then used as input to the dynamic programming algorithm, which computes the minimum alignment cost.

4. **Output**: The result is written to the specified output file.

## Notes

- The output directory (`Data/Output/`) will be created automatically if it doesn't exist
- Input files must contain valid base strings and indices
- The algorithm uses a gap penalty of 30 by default
- All sequences should only contain characters A, C, G, or T
- String augmentation follows the pattern: `s[:idx+1] + s + s[idx+1:]` at each index

## License

See LICENSE file for details.
