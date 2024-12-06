# Computing Algorithms - Dynamic Programming - Pay in Coins
# Designed and developed by Kobi Chambers - Griffith University

# Import packages and modules
try:
    import os
    import sys
    import math
    import time
    # import tkinter as tk
    # from tkinter import filedialog
except ImportError as e:
    print(f"Error importing module: {e}")
    print(f"Please ensure that required modules are installed...\n")
    sys.exit(1)

# Create set of primes & track the largest integer input n
prime_set = set()
largest_n = 0

##################################
### INPUT PROCESSING FUNCTIONS ###
##################################


def process_input_file(input_file_path):
    """
    Process the input file and return the input lines.

    Parameters:
    input_file_path (str): The path to the input file.

    Returns:
    input_lines (list): A list of input lines.
    """
    try:
        # Reading input file not included in algorithm time
        with open(input_file_path, 'r') as f:
            # Initialise empty array for input lines
            input_lines = []
            for line in f:
                # Initialise empty list for each row
                row = []
                for integers in line.split():
                    row.append(int(integers))

                # Create input array from rows
                input_lines.append(row)

    # Handle file error
    except:
        sys.exit("Error occured while opening the file. Closing program...")

    return input_lines


def get_input_file():
    """
    Get the input file path from the command line arguments.

    Returns:
    str: The input file path.
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python pay_in_coins.py [input_file_path]")

    input_file_path = sys.argv[1]

    return input_file_path

####################################
### UTILITY AND HELPER FUNCTIONS ###
####################################


def timer(function_name):
    """
    Decorator function to measure the execution time of another function.

    Parameters:
    function_name (function): The function to time.

    Returns:
    function: A wrapper function that times the execution of the input function and returns the result and the time taken.
    """
    def wrapper(*args, **kwargs):
        # Time and execute function
        start_time = time.perf_counter()
        result = function_name(*args, **kwargs)
        end_time = time.perf_counter()

        # Elapsed time calculated in seconds
        elapsed_time = (end_time - start_time)
        return result, elapsed_time

    return wrapper


def check_prime(n):
    """
    Check if a number is prime.

    Parameters:
    n (int): The number to check.

    Returns:
    n (int): If n is prime.
    1 (int): If n is not prime.
    """
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return 1

    return n


def find_primes(payout):
    """
    Find prime numbers up to a given value.

    Parameters:
    payout (int): The payout value.

    Returns:
    prime_set (set): A set of prime numbers up to the payout value.
    """
    global largest_n
    global prime_set

    # Check if find_primes has been run before
    if not prime_set:
        # Loop up to first integer value in line, and find primes
        for n in range(1, payout + 1):
            prime_set.add(check_prime(n))
            # Set largest_n as payout
            largest_n = payout
        return prime_set

    # If payout == largest_n, we already know the prime set
    elif payout == largest_n:
        return prime_set

    # Check if integer value > largest value in the prime set
    elif payout > largest_n:
        # Loop starts from largest value of n that find_primes has already found
        for n in range(largest_n, payout + 1):
            prime_set.add(check_prime(n))

        # Set new largest n and Union the sets
        largest_n = payout
        return prime_set

    # Else we already have the number of primes up to payout value, and simply need to find the set of primes lower than payout value
    else:
        lower_prime_set = set()
        lower_prime_set = {i for i in prime_set if i <= payout}
        return lower_prime_set


def ways_to_sum(payout, coin_options, max_coins, i=0, sums_list=[], results=[]):
    """
    Find all the ways to sum the coins to the payout value using recursion.

    Parameters:
    payout (int): The payout value.
    coin_options (list): A list of coin options.
    max_coins (tuple): A tuple containing the minimum and maximum number of coins allowed.
    i (int): The index used for recursion.
    sums_list (list): The current list of sums.
    results (list): The list to store the results.

    Returns:
    results (list): The list of all possible ways to sum the coins to the payout value.
    """
    # Check if current sum has reached the payout value exactly, and if coins are within the bounds of input
    if payout == 0 and len(sums_list) >= max_coins[0] and len(sums_list) <= max_coins[1]:
        results.append(sums_list)
        return results

    # Check if number of coins used has reached the upper limit without summing to the payout value
    if len(sums_list) >= max_coins[1]:
        return

    # Loop through range(i, len(coin_options), each recursive call changes the size of the range due to i value being updated by j in for loop
    for j in range(i, len(coin_options)):
        if coin_options[j] > payout:
            continue
        ways_to_sum(payout - coin_options[j], coin_options,
                    max_coins, j, sums_list + [coin_options[j]], results)

    return results

#####################################
### ALGORITHM EXECUTION FUNCTIONS ###
#####################################


@timer
def execute_algorithms(input_lines):
    """
    Run through input lines and execute each algorithm when needed.

    Parameters:
    input_lines (list): A list of input lines.

    Returns:
    results_dict (dict): A dictionary with the number of ways to pay in coins and the execution time for each input.
    """

    @timer
    def one_integer(line):
        """
        Calculate the number of ways to pay in coins with one input.

        Parameters:
        line (list): The input line.

        Returns:
        results (int): The number of ways to pay in coins for the given input.
        """
        # Set line values
        payout = line[0]

        # Find set of primes up to payout value
        new_prime_set = find_primes(payout)

        # Create list of coins we can use
        if payout in new_prime_set:
            coin_options = list(new_prime_set)
        else:
            coin_options = list(new_prime_set) + [payout]

        # Set range of coins we can use
        max_coins = (1, payout)

        # Find how many ways we can sum the coins given the input
        results = len(ways_to_sum(payout, coin_options,
                      max_coins, 0, sums_list=[], results=[]))

        return results

    @timer
    def two_integers(line):
        """
        Calculate the number of ways to pay in coins with two inputs.

        Parameters:
        line (list): The input line.

        Returns:
        results (int): The number of ways to pay in coins for the given input.
        """
        # Set line values
        payout = line[0]
        number_coins = line[1]

        # Find set of primes up to payout value
        new_prime_set = find_primes(payout)

        # Create list of coins we can use
        if payout in new_prime_set:
            coin_options = list(new_prime_set)
        else:
            coin_options = list(new_prime_set) + [payout]

        # Set range of coins we can use
        max_coins = (number_coins, number_coins)

        # Find how many ways we can sum the coins given the input
        results = len(ways_to_sum(payout, coin_options,
                      max_coins, 0, sums_list=[], results=[]))

        return results

    @timer
    def three_integers(line):
        """
        Calculate the number of ways to pay in coins with three inputs.

        Parameters:
        line (list): The input line.

        Returns:
        results (int): The number of ways to pay in coins for the given input.
        """
        # Set line values
        payout = line[0]
        low_num_coins = line[1]
        high_num_coins = line[2]

        # Find set of primes up to payout value
        new_prime_set = find_primes(payout)

        # Create list of coins we can use
        if payout in new_prime_set:
            coin_options = list(new_prime_set)
        else:
            coin_options = list(new_prime_set) + [payout]

        # Set range of coins we can use
        max_coins = (low_num_coins, high_num_coins)

        # Find how many ways we can sum the coins given the input
        results = len(ways_to_sum(payout, coin_options,
                      max_coins, 0, sums_list=[], results=[]))

        return results

    # Loop through each input line, match length of line and call function depending on calculation required.
    for line in input_lines:
        line_size = len(line)
        match line_size:
            case 1:
                result, elapsed_time = one_integer(line)
                results_dict[elapsed_time] = [result]

            case 2:
                result, elapsed_time = two_integers(line)
                results_dict[elapsed_time] = [result]

            case 3:
                result, elapsed_time = three_integers(line)
                results_dict[elapsed_time] = [result]

            case _:
                print(
                    f"Skipping current line with contents: {line}, check that there are 1, 2 or 3 ints per line.\n")
                print("Moving to next line...\n")
                continue

    # Return the result dictionary
    return results_dict


def write_output_file(program_folder, results_dict):
    """
    Write the results found to an output file.

    Parameters:
    program_folder (str): The absolute path of the program folder.
    results_dict (dict): A dictionary with the number of ways to pay in coins and the execution time for each input.
    """
    # Set output path name
    output_path = os.path.join(program_folder, 'output.txt')

    # Write the results to output file
    try:
        with open(output_path, 'w') as f:
            # Write each dictionary value to a new line
            for i in results_dict.values():
                f.write('\n'.join(map(str, i)))
                f.write('\n')

        print(f"Results have been written to:\n{output_path}\n")

    except:
        sys.exit("Error writing to output file. Exiting program...\n")

##############
### DRIVER ###
##############


if __name__ == '__main__':
    # Get the absolute path of the folder containing the program file
    program_folder = os.path.dirname(os.path.abspath(__file__))

    # Get the input file path from command line arguments
    input_file_path = get_input_file()
    # Get input lines
    input_lines = process_input_file(input_file_path)

    # Initialise empty dictionary to store input lines, and their associated result and exection time
    results_dict = dict()
    # Execute algorithms for each input line
    results_dict, total_time = execute_algorithms(input_lines)

    # Display individual execution times for each input line, then total execution time
    print('')
    for line, elapsed_time in zip(input_lines, results_dict.keys()):
        print(
            f"Execution time for input line: {line} - {elapsed_time:.6f} seconds")

    print(f"\nTotal time to process input file: {total_time:.2f} seconds\n")

    # Parse program folder location and results to write_output function
    write_output_file(program_folder, results_dict)
