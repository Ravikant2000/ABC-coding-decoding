from itertools import permutations

def has_unique_solution(mapping):
    return len(mapping.values()) == len(set(mapping.values()))

def find_all_solutions(num1, num2, operation, result, fixed_assignments):
    char_count = {}
    char_to_digit = {}

    for char, digit in fixed_assignments.items():
        char_to_digit[char] = digit

    for char in num1 + num2 + result:
        if char not in char_to_digit:
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1

    unique_chars = list(char_count.keys())

    if len(unique_chars) + len(char_to_digit) > 10:
        print('Too many attributes: Cannot assign digits')
        return "Too many attributes: Cannot assign digits"

    digits = list(range(10))
    char_permutations = permutations(digits, len(unique_chars))

    all_solutions = []

    for perm in char_permutations:
        current_mapping = char_to_digit.copy()
        for i, char in enumerate(unique_chars):
            current_mapping[char] = perm[i]

        try:
            n1 = int(''.join(str(current_mapping[ch]) for ch in num1))
            n2 = int(''.join(str(current_mapping[ch]) for ch in num2))
            res = int(''.join(str(current_mapping[ch]) for ch in result))
        except KeyError:
            continue

        if (operation == '+' and n1 + n2 == res) or \
           (operation == '-' and n1 - n2 == res) or \
           (operation == '*' and n1 * n2 == res) or \
           (operation == '/' and n2 != 0 and n1 / n2 == res):
            all_solutions.append((n1, n2, res, current_mapping))

    return all_solutions or "No Solutions Found"

if __name__ == "__main__":
    while True:
        print("_________Welcome to Cryptarithm Solver__________")
        fixed_assignments_input = input('Enter the fixed assignments (e.g., A=1,B=2): ').strip()
        fixed_assignments = {}

        # Validate and parse fixed assignments
        if fixed_assignments_input:
            try:
                pairs = fixed_assignments_input.split(',')
                for pair in pairs:
                    char, digit = pair.split('=')
                    fixed_assignments[char.strip().upper()] = int(digit.strip())
            except ValueError:
                print("Invalid format for fixed assignments. Please use the format A=1,B=2.")
                continue

        num1 = input('Enter the first number: ').upper().strip()
        num2 = input('Enter the second number: ').upper().strip()
        operation = input('Enter the operation (+, -, *, /): ').strip()
        result = input('Enter the result: ').upper().strip()

        # Solve the puzzle
        solutions = find_all_solutions(num1, num2, operation, result, fixed_assignments)

        if solutions == "Too many attributes: Cannot assign digits":
            continue  # Restart the loop if the problem can't be solved due to too many attributes
        elif isinstance(solutions, str):
            print(solutions)
        else:
            print(f"\nFound {len(solutions)} solutions:\n")
            for sol in solutions:
                n1, n2, res, mapping = sol
                print(f"Solved! {num1} = {n1}, {num2} = {n2}, {result} = {res}")
                print(f"Mapping: {mapping}\n")

            unique_solutions = [sol for sol in solutions if has_unique_solution(sol[3])]

            if unique_solutions:
                print(f"\nFound {len(unique_solutions)} unique solutions:\n")
                for sol in unique_solutions:
                    n1, n2, res, mapping = sol
                    print(f"Unique Solution: {num1} = {n1}, {num2} = {n2}, {result} = {res}")
                    print(f"Mapping: {mapping}\n")
            else:
                print("No unique solution found.\n")

        # Ask the user to retry or quit
        retry = input("Would you like to solve another puzzle? (yes/no): ").strip().lower()
        if retry != 'yes':
            print("Thank you for using Cryptarithm Solver. Goodbye!")
            break
