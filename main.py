from itertools import permutations

def has_unique_values(mapping):
    """Check if all values in the mapping are unique."""
    return len(mapping.values()) == len(set(mapping.values()))

def find_all_solutions(num1, num2, operation, result, fixed_assignments):
    # Create a mapping of characters to their counts and fixed assignments
    char_count = {}
    char_to_digit = {}

    # Process fixed assignments
    for char, digit in fixed_assignments.items():
        char_to_digit[char] = digit

    # Count characters in num1, num2, and result
    for char in num1 + num2 + result:
        if char not in char_to_digit:  # Only count if not already fixed
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1

    unique_chars = list(char_count.keys())
    
    if len(unique_chars) + len(char_to_digit) > 10:
        return "Too many unique chars; cannot assign digits."

    digits = list(range(10))
    chars_permutation = permutations(digits, len(unique_chars))

    all_solutions = []

    for perm in chars_permutation:
        # Create a mapping from character to digit
        current_mapping = char_to_digit.copy()
        for i, char in enumerate(unique_chars):
            current_mapping[char] = perm[i]

        # Skip if leading character is zero
        if current_mapping[num1[0]] == 0 or current_mapping[num2[0]] == 0 or current_mapping[result[0]] == 0:
            continue

        try:
            n1 = int(''.join(str(current_mapping[ch]) for ch in num1))
            n2 = int(''.join(str(current_mapping[ch]) for ch in num2))
            res = int(''.join(str(current_mapping[ch]) for ch in result))
        except KeyError:
            continue

        # Check arithmetic operation
        if (operation == '+' and n1 + n2 == res) or \
           (operation == '-' and n1 - n2 == res) or \
           (operation == '*' and n1 * n2 == res) or \
           (operation == '/' and n2 != 0 and n1 / n2 == res):
            all_solutions.append((n1, n2, res, current_mapping))

    return all_solutions or "No solution found."

if __name__ == "__main__":
    print('Enter the inputs for the puzzle solver.')
    
    # Example of fixed assignments: {'A': 5}
    fixed_assignments_input = input('Enter fixed assignments (e.g., A=5,B=3): ')
    fixed_assignments = {}
    
    if fixed_assignments_input.strip():
        pairs = fixed_assignments_input.split(',')
        for pair in pairs:
            char, digit = pair.split('=')
            fixed_assignments[char.strip().lower()] = int(digit.strip())

    num1 = input('Enter the first number in alphabet form (eg. AB): ').lower()
    num2 = input('Enter the second number in alphabet form (eg. BC): ').lower()
    operation = input('Enter the operation (+,-,*,/): ')
    result = input('Enter the result in alphabet form (eg. DBEB): ').lower()

    solutions = find_all_solutions(num1, num2, operation, result, fixed_assignments)

    if isinstance(solutions, str):
        print(solutions)
    else:
        print(f"\nFound {len(solutions)} solutions:\n")
        
        # Print all solutions
        for sol in solutions:
            n1, n2, res, mapping = sol
            print(f"Solved! {num1.upper()} = {n1}, {num2.upper()} = {n2}, {result.upper()} = {res}")
            print(f"Mapping: {mapping}\n")

        # Filter solutions to only include those with unique attribute values
        unique_solutions = [sol for sol in solutions if has_unique_values(sol[3])]
        
        if unique_solutions:
            print(f"\nUnique attribute solutions ({len(unique_solutions)} found):\n")
            for sol in unique_solutions:
                n1, n2, res, mapping = sol
                print(f"Solved! {num1.upper()} = {n1}, {num2.upper()} = {n2}, {result.upper()} = {res}")
                print(f"Mapping: {mapping}\n")
        else:
            print("No unique attribute solutions found.")
