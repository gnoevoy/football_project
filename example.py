import random

# select, copy to the end / start of line


def generate_numbers(count, start=1, end=100):
    """Generates a list of random numbers."""
    return [random.randint(start, end) for _ in range(count)]


def find_max(numbers):
    """Finds the maximum number in a list."""
    if not numbers:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num


def find_min(numbers):
    """Finds the minimum number in a list."""
    if not numbers:
        return None
    min_num = numbers[0]
    for num in numbers:
        if num < min_num:
            min_num = num
    return min_num


def main():
    numbers = generate_numbers(10)
    print("Generated Numbers:", numbers)
    print("Maximum:", find_max(numbers))
    print("Minimum:", find_min(numbers))


if __name__ == "__main__":
    main()

x = 1
y = 2
z = 3
