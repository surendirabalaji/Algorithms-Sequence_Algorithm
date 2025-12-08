import sys
import os
import time
from typing import Tuple, List

# ============================================================================
# String Generation Functions (from string_generator.py)
# ============================================================================

def generate_string(base, indices):
    """
    Iteratively inserts the string into itself after given indices.
    Each step doubles the string length, matching the project specification.
    """
    s = base
    for idx in indices:
        s = s[:idx + 1] + s + s[idx + 1:]
    return s


def parse_input_file(input_path):
    """
    Reads the input file and extracts:
    - base string s0
    - j indices for s
    - base string t0
    - k indices for t
    
    Uses Format 2 (Implicit lists): s0, indices..., t0, indices...
    This is the standard format used by the test cases.
    """
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return "", [], "", []

    def is_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def is_dna_base_string(s):
        """Check if string contains only valid DNA bases (A, C, G, T)"""
        return len(s) > 0 and all(c in 'ACGT' for c in s.upper())

    try:
        # Format 2: Implicit lists (s0, indices..., t0, indices...)
        s0 = lines[0]
        s_indices = []
        idx = 1
        
        # Collect all integer indices for first string
        while idx < len(lines) and is_int(lines[idx]) and not is_dna_base_string(lines[idx]):
            s_indices.append(int(lines[idx]))
            idx += 1
            
        # Next non-integer should be t0
        if idx < len(lines):
            t0 = lines[idx]
            idx += 1
            t_indices = []
            
            # Collect all integer indices for second string
            while idx < len(lines) and is_int(lines[idx]) and not is_dna_base_string(lines[idx]):
                t_indices.append(int(lines[idx]))
                idx += 1
                
            return s0, s_indices, t0, t_indices
        else:
            return s0, s_indices, "", []
            
    except Exception as e:
        raise ValueError(f"Failed to parse {input_path}: {e}")


def generate_input_strings(input_path):
    """
    Main function:
    Reads the input file and generates s_j and t_k.
    Returns the final two expanded strings.
    """
    s0, s_idx, t0, t_idx = parse_input_file(input_path)

    final_s = generate_string(s0, s_idx)
    final_t = generate_string(t0, t_idx)

    return final_s, final_t


# ============================================================================
# Sequence Alignment Algorithm
# ============================================================================

# Alpha matrix (mismatch cost table)
#     A   C   G   T
ALPHA = {
    'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
    'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
    'G': {'A': 48, 'G': 0, 'C': 118, 'T': 110},
    'T': {'A': 94, 'T': 0, 'C': 48, 'G': 110}
}

# Gap penalty
GAP = 30
DELTA = GAP  # Alias for consistency with memory-efficient implementation


def get_alpha(char1, char2):
    """Get the mismatch cost between two characters."""
    return ALPHA.get(char1, {}).get(char2, 0)


def sequence_alignment(str1, str2, gap=GAP):
    """
    Compute the minimum alignment cost using dynamic programming.
    
    OPT(i, j) = min(
        OPT(i-1, j-1) + alpha_ij,  # match/mismatch
        OPT(i-1, j) + gap,          # gap in str2
        OPT(i, j-1) + gap           # gap in str1
    )
    """
    m = len(str1)
    n = len(str2)
    
    # Initialize DP table
    # dp[i][j] represents the minimum cost to align str1[0:i] with str2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases: aligning empty strings
    # dp[0][0] = 0 (already initialized)
    for i in range(1, m + 1):
        dp[i][0] = i * gap  # gap in str2
    for j in range(1, n + 1):
        dp[0][j] = j * gap  # gap in str1
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Option 1: Match/mismatch str1[i-1] with str2[j-1]
            match_cost = dp[i-1][j-1] + get_alpha(str1[i-1], str2[j-1])
            
            # Option 2: Gap in str2 (skip str1[i-1])
            gap_str2 = dp[i-1][j] + gap
            
            # Option 3: Gap in str1 (skip str2[j-1])
            gap_str1 = dp[i][j-1] + gap
            
            # Take the minimum
            dp[i][j] = min(match_cost, gap_str2, gap_str1)
    
    return dp[m][n]


# ============================================================================
# Memory-Efficient Alignment (Hirschberg's Algorithm)
# ============================================================================

    # Call the main function to execute the program
    main()
    
    # Ensure proper termination of the script
    sys.exit(0)


