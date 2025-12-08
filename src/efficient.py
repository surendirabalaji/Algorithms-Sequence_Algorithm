import sys
import os
import time
from typing import Tuple, List

# Import string generation functions from basic.py
from basic import generate_string, parse_input_file, generate_input_strings, DELTA, GAP, ALPHA, get_alpha


# =========================================================================
# Memory-Efficient Alignment (Hirschberg's Algorithm)
# =========================================================================

def space_efficient_alignment(str1: str, str2: str) -> List[int]:
    m, n = len(str1), len(str2)
    prev = [j * DELTA for j in range(n + 1)]
    for i in range(1, m + 1):
        curr = [i * DELTA]
        for j in range(1, n + 1):
            match_cost = prev[j - 1] + get_alpha(str1[i - 1], str2[j - 1])
            delete_cost = prev[j] + DELTA
            insert_cost = curr[j - 1] + DELTA
            curr.append(min(match_cost, delete_cost, insert_cost))
        prev = curr
    return prev

def basic_alignment(str1: str, str2: str) -> Tuple[str, str, int]:
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i * DELTA
    for j in range(n + 1):
        dp[0][j] = j * DELTA
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_cost = dp[i-1][j-1] + get_alpha(str1[i-1], str2[j-1])
            delete_cost = dp[i-1][j] + DELTA
            insert_cost = dp[i][j-1] + DELTA
            dp[i][j] = min(match_cost, delete_cost, insert_cost)
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
    m, n = len(str1), len(str2)
    if m == 0:
        return '_' * n, str2, n * DELTA
    if n == 0:
        return str1, '_' * m, m * DELTA
    if m == 1 or n == 1:
        return basic_alignment(str1, str2)
    mid = m // 2
    str1_left = str1[:mid]
    str1_right = str1[mid:]
    score_left = space_efficient_alignment(str1_left, str2)
    score_right = space_efficient_alignment(str1_right[::-1], str2[::-1])
    score_right.reverse()
    min_cost = float('inf')
    split_idx = 0
    for k in range(n + 1):
        total_cost = score_left[k] + score_right[k]
        if total_cost < min_cost:
            min_cost = total_cost
            split_idx = k
    str2_left = str2[:split_idx]
    str2_right = str2[split_idx:]
    left_align_str1, left_align_str2, left_cost = hirschberg_alignment(str1_left, str2_left)
    right_align_str1, right_align_str2, right_cost = hirschberg_alignment(str1_right, str2_right)
    aligned_str1 = left_align_str1 + right_align_str1
    aligned_str2 = left_align_str2 + right_align_str2
    total_cost = left_cost + right_cost
    return aligned_str1, aligned_str2, total_cost

def calculate_alignment_cost(aligned_str1: str, aligned_str2: str) -> int:
    if len(aligned_str1) != len(aligned_str2):
        raise ValueError("Aligned sequences must have same length")
    cost = 0
    for i in range(len(aligned_str1)):
        if aligned_str1[i] == '_' or aligned_str2[i] == '_':
            cost += DELTA
        else:
            cost += get_alpha(aligned_str1[i], aligned_str2[i])
    return cost

# =========================================================================
# Main Function for Efficient Algorithm
# =========================================================================

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 efficient.py input.txt output.txt")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    try:
        str1, str2 = generate_input_strings(input_file)
    except Exception as e:
        print(f"Error parsing input file: {e}")
        sys.exit(1)
    if not str1 or not str2:
        print("Error: Failed to generate input strings from file.")
        sys.exit(1)
    start_time = time.time()
    aligned_str1, aligned_str2, cost = hirschberg_alignment(str1, str2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    calculated_cost = calculate_alignment_cost(aligned_str1, aligned_str2)
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
