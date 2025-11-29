# string_generator.py
#author: Jingyi Wu
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
    
    Supports two formats:
    1. Explicit counts (s0, j, indices..., t0, k, indices...)
    2. Implicit lists (s0, indices..., t0, indices...)
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

    # Try Format 1: Explicit counts
    try:
        s0 = lines[0]
        j = int(lines[1])
        
        # Check if file has enough lines for this format
        # We need at least: 1 (s0) + 1 (j) + j (indices) + 1 (t0) + 1 (k)
        if len(lines) < 2 + j + 2:
            raise IndexError("File too short for Format 1")

        t0_line_index = 2 + j
        t0 = lines[t0_line_index]
        k = int(lines[t0_line_index + 1])
        
        # Verify we have enough lines for t_indices
        if len(lines) < t0_line_index + 2 + k:
             raise IndexError("File too short for Format 1 t_indices")

        s_indices = [int(lines[2 + i]) for i in range(j)]
        t_indices = [int(lines[t0_line_index + 2 + i]) for i in range(k)]

        return s0, s_indices, t0, t_indices
    except (ValueError, IndexError):
        # Fallback to Format 2
        pass

    # Format 2: Implicit lists
    try:
        s0 = lines[0]
        s_indices = []
        idx = 1
        while idx < len(lines) and is_int(lines[idx]):
            s_indices.append(int(lines[idx]))
            idx += 1
            
        if idx < len(lines):
            t0 = lines[idx]
            idx += 1
            t_indices = []
            while idx < len(lines) and is_int(lines[idx]):
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


# Optional usage example when running directly
if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) != 2:
        print("Usage: python3 string_generator.py <input_file_or_directory>")
        exit(1)

    input_path = sys.argv[1]

    def process_file(file_path):
        try:
            s, t = generate_input_strings(file_path)
            print(f"--- Results for {os.path.basename(file_path)} ---")
            print("Generated s_j:\n", s)
            print("Generated t_k:\n", t)
            print("="*40)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    if os.path.isdir(input_path):
        # Process all .txt files in the directory
        files = [f for f in os.listdir(input_path) if f.endswith('.txt')]
        files.sort() 
        
        for filename in files:
            process_file(os.path.join(input_path, filename))
    elif os.path.isfile(input_path):
        process_file(input_path)
    else:
        print(f"Error: Path '{input_path}' does not exist.")
