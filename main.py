from itertools import permutations


def find_all_solutions(num1, num2, operation, result):
    unique_chars = set(num1 + num2 + result)
    if len(unique_chars) > 10:
        print("Too many unique chars cannot assign digits")

    digits = list(range(10))
    chars_permutation = permutations(digits, len(unique_chars))

    solutions = []

    for perm in chars_permutation:
        char_to_digit = dict(zip(unique_chars, perm))

        if char_to_digit[num1[0]] == 0 or char_to_digit[num2[0]] == 0 or char_to_digit[result[0]] == 0:
            continue

        try:
            n1 = int(''.join(str(char_to_digit[ch]) for ch in num1))
            n2 = int(''.join(str(char_to_digit[ch]) for ch in num2))
            res = int(''.join(str(char_to_digit[ch]) for ch in result))

        except KeyError:
            continue

        if operation == '+' and n1 + n2 == res:
            solutions.append((n1, n2, res, char_to_digit))
        elif operation == '-' and n1 - n2 == res:
            solutions.append((n1, n2, res, char_to_digit))
        elif operation == '*' and n1 * n2 == res:
            solutions.append((n1, n2, res, char_to_digit))
        elif operation == '/' and n2 != 0 and n1 / n2 == res:
            solutions.append((n1, n2, res, char_to_digit))

    if not solutions:
        return "No solution found."
    return solutions


if __name__ == "__main__":
    print('Enter the inputs for the puzzle solver.')
    num1 = input('Enter the first number in alphabet form (eg. ABC):').lower()
    num2 = input('Enter the second number in alpbabet form (eg.DEF):').lower()
    operation = input('Enter the operation (+,-,*,/): ')
    result = input('Enter the result in alphabet form (eg. GHI): ').lower()

    solutions = find_all_solutions(num1, num2, operation, result)

    if isinstance(solutions, str):
        print(solutions)
    else:
        print(f"\nFound {len(solutions)} solutions:\n")
        for sol in solutions:
            n1, n2, res, mapping = sol
            print(f"Solved! {num1.upper()} = {n1}, {num2.upper()} = {n2}, {result.upper()} = {res}")
            print(f"Mapping: {mapping}\n")


















