import random


def read_random_lines(filename: str, count: int = 100):
    with open(filename, "rb") as file:
        lines = file.readlines()

    # Ensure num_lines doesn't exceed the number of lines in the file
    num_lines = min(count, len(lines))

    # Select num_lines random lines from the list
    selected_lines = [line.decode("utf-8").rstrip("\n") for line in random.sample(lines, num_lines)]
    random.shuffle(selected_lines)
    return selected_lines
