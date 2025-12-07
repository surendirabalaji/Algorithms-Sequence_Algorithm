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

def space_efficient_alignment(str1: str, str2: str) -> List[int]:
    """
    Compute the last column of the DP table using O(n) space.
    
    Returns a list where result[j] = minimum cost to align str1 with str2[0:j]
    """
    m, n = len(str1), len(str2)
    
    # We only need two columns: previous and current
    prev = [j * DELTA for j in range(n + 1)]
    
    for i in range(1, m + 1):
        curr = [i * DELTA]  # First element: cost of aligning str1[0:i] with empty string
        
        for j in range(1, n + 1):
            # Three choices:
            # 1. Match/mismatch str1[i-1] with str2[j-1]
            match_cost = prev[j - 1] + get_alpha(str1[i - 1], str2[j - 1])
            # 2. Insert gap in str1 (delete from str2)
            delete_cost = prev[j] + DELTA
            # 3. Insert gap in str2 (delete from str1)
            insert_cost = curr[j - 1] + DELTA
            
            curr.append(min(match_cost, delete_cost, insert_cost))
        
        prev = curr
    
    return prev


def basic_alignment(str1: str, str2: str) -> Tuple[str, str, int]:
    """
    Basic DP alignment for small cases. Returns (aligned_str1, aligned_str2, cost).
    """
    m, n = len(str1), len(str2)
    
    # DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i * DELTA
    for j in range(n + 1):
        dp[0][j] = j * DELTA
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_cost = dp[i-1][j-1] + get_alpha(str1[i-1], str2[j-1])
            delete_cost = dp[i-1][j] + DELTA
            insert_cost = dp[i][j-1] + DELTA
            dp[i][j] = min(match_cost, delete_cost, insert_cost)
    
    # Backtrack to find alignment
    aligned_str1 = ""
    aligned_str2 = ""
    i, j = m, n
    
    while i > 0 or j > 0:
        if i == 0:
            aligned_str1 = '_' + aligned_str1
            aligned_str2 = str2[j-1] + aligned_str2
            j -= 1
        elif j == 0:
            aligned_str1 = str1[i-1] + aligned_str1
            aligned_str2 = '_' + aligned_str2
            i -= 1
        else:
            current = dp[i][j]
            match_cost = dp[i-1][j-1] + get_alpha(str1[i-1], str2[j-1])
            delete_cost = dp[i-1][j] + DELTA
            insert_cost = dp[i][j-1] + DELTA
            
            if current == match_cost:
                aligned_str1 = str1[i-1] + aligned_str1
                aligned_str2 = str2[j-1] + aligned_str2
                i -= 1
                j -= 1
            elif current == delete_cost:
                aligned_str1 = str1[i-1] + aligned_str1
                aligned_str2 = '_' + aligned_str2
                i -= 1
            else:
                aligned_str1 = '_' + aligned_str1
                aligned_str2 = str2[j-1] + aligned_str2
                j -= 1
    
    return aligned_str1, aligned_str2, dp[m][n]


def hirschberg_alignment(str1: str, str2: str) -> Tuple[str, str, int]:
    """
    Hirschberg's algorithm for memory-efficient sequence alignment.
    
    Returns: (aligned_str1, aligned_str2, cost)
    """
    m, n = len(str1), len(str2)
    
    # Base cases
    if m == 0:
        return '_' * n, str2, n * DELTA
    if n == 0:
        return str1, '_' * m, m * DELTA
    if m == 1 or n == 1:
        # Use basic DP for small cases
        return basic_alignment(str1, str2)
    
    # Divide str1 in half
    mid = m // 2
    str1_left = str1[:mid]
    str1_right = str1[mid:]
    
    # Compute costs for left half: str1_left vs all prefixes of str2
    score_left = space_efficient_alignment(str1_left, str2)
    
    # Compute costs for right half: str1_right (reversed) vs all suffixes of str2 (reversed)
    score_right = space_efficient_alignment(str1_right[::-1], str2[::-1])
    score_right.reverse()
    
    # Find the optimal split point in str2
    min_cost = float('inf')
    split_idx = 0
    
    for k in range(n + 1):
        total_cost = score_left[k] + score_right[k]
        if total_cost < min_cost:
            min_cost = total_cost
            split_idx = k
    
    # Recursively solve left and right parts
    str2_left = str2[:split_idx]
    str2_right = str2[split_idx:]
    
    left_align_str1, left_align_str2, left_cost = hirschberg_alignment(str1_left, str2_left)
    right_align_str1, right_align_str2, right_cost = hirschberg_alignment(str1_right, str2_right)
    
    # Combine results
    aligned_str1 = left_align_str1 + right_align_str1
    aligned_str2 = left_align_str2 + right_align_str2
    total_cost = left_cost + right_cost
    
    return aligned_str1, aligned_str2, total_cost


def calculate_alignment_cost(aligned_str1: str, aligned_str2: str) -> int:
    """
    Calculate the total alignment cost from aligned sequences.
    """
    if len(aligned_str1) != len(aligned_str2):
        raise ValueError("Aligned sequences must have same length")
    
    cost = 0
    for i in range(len(aligned_str1)):
        if aligned_str1[i] == '_' or aligned_str2[i] == '_':
            cost += DELTA
        else:
            cost += get_alpha(aligned_str1[i], aligned_str2[i])
    
    return cost


# ============================================================================
# Main Function
# ============================================================================

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 basic.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read input file
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Generate augmented input strings from the input file
    try:
        str1, str2 = generate_input_strings(input_file)
    except Exception as e:
        print(f"Error parsing input file: {e}")
        sys.exit(1)
    
    if not str1 or not str2:
        print("Error: Failed to generate input strings from file.")
        sys.exit(1)
    
    # Use default gap penalty
    gap_penalty = GAP
    
    # Measure time
    start_time = time.time()
    
    # Compute minimum alignment cost using basic DP
    min_cost = sequence_alignment(str1, str2, gap_penalty)
    
    end_time = time.time()
    
    # Calculate time taken
    time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Write output file (create if doesn't exist)
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, 'w') as f:
        f.write(str(min_cost) + '\n')
    
    print(f"Minimum alignment cost: {min_cost}")
    print(f"Time taken: {time_taken:.2f} ms")
    print(f"Result written to {output_file}")


def main_efficient():
    """
    Main function using memory-efficient Hirschberg algorithm.
    This can be called separately or used as an alternative to main().
    """
    if len(sys.argv) != 3:
        print("Usage: python3 basic.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read input file
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Generate augmented input strings from the input file
    try:
        str1, str2 = generate_input_strings(input_file)
    except Exception as e:
        print(f"Error parsing input file: {e}")
        sys.exit(1)
    
    if not str1 or not str2:
        print("Error: Failed to generate input strings from file.")
        sys.exit(1)
    
    # Measure time
    start_time = time.time()
    
    # Run memory-efficient alignment
    aligned_str1, aligned_str2, cost = hirschberg_alignment(str1, str2)
    
    end_time = time.time()
    
    # Calculate time taken
    time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Verify cost calculation
    calculated_cost = calculate_alignment_cost(aligned_str1, aligned_str2)
    
    # Write output file
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, 'w') as f:
        f.write(f"{calculated_cost}\n")
        f.write(f"{aligned_str1}\n")
        f.write(f"{aligned_str2}\n")
        f.write(f"{time_taken:.2f}\n")
    
    print(f"Minimum alignment cost: {calculated_cost}")
    print(f"Time taken: {time_taken:.2f} ms")
    print(f"Alignment length: {len(aligned_str1)}")
    print(f"Result written to {output_file}")


if __name__ == "__main__":
    main()


