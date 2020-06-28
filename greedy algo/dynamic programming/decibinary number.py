import math
import os

def decibinary_to_decimal(n_db):
    """
    Convert decibinary number to decimal. 
    Args:
        n_db (list of int): Decibinary number, e.g. [1, 0, 3]
    
    Returns:
        int: Decimal number
    """
    power = 0
    decimal = 0
    for digit in reversed(n_db):
        decimal += digit * 2**power
        power += 1
    return decimal
    

def increment_decibinary(n_db):
    """
    Increment decibinary number by one.
    Args:
        n_db (list of int): Decibinary number, e.g. [1, 0, 3]
    Returns:
        list of int: Incremented decibinary number. Return 
            None if we cannot increment last digit.
    """
    if int(n_db[-1]) < 9:
        n_db[-1] += 1
        return n_db
    else:
        return None


def find_decibinary_numbers_n_digits(n, prev, decimal):
    """
    Find decibinary numbers of n digits.
    Args:
        n (int): Number of digits
        prev (list of list of int): Decibinary representations
            of previous decimal number.  
        decimal (int): Decimal number to which current
            decibinary numbers correspond.
    """
    db_ns = list()
    for i, prev_db in enumerate(prev):
        inc_db = increment_decibinary(prev_db)
        if inc_db is not None:
            db_ns.append(inc_db)
    return None

# SECOND APPROACH: use nested dictionary to store 
# decimal number -> number of digits -> list of decibinary
# numbers.

# RECURRENCE RELATION: For new decibinary number, set first
# digit. Build remaining n-1 digits with memoized results
# for all decibinary numbers equaling x with <= n-1 digits.

def lookup_memo(val, n, memo):
    """
    Get all memoized decibinary representations with n
    digits corresponding to decimal value val..
    Args:
        val (int): Decimal value.
        n (int): Number of digits.
        memo (dict): Memoized decibinary representations.
    Returns:
        list of str if val and n available in nested 
            dictionary, else None
    Example:
        val=4 n=2 -> ['12', '20']
    """
    if val not in memo:
        return None
    if n not in memo[val]:
        return None
    return memo[val][n]


def update_dbin_numbers(first_digit, val_rem, n_rem, n, memo):
    """
    Update decibinary numbers with a new leftmost (first)
    digit.
    Args:
        first_digit (int): First digit in decibinary number.
        val_rem (int): Decimal value of "remaining" value 
            after subtracting the decimal value represented by
            the first digit.
        n_rem (int): Number of digits in "remaining" value.
        n (int): Number of digits in full decibinary representation.
        memo (dict): Memoized decibinary numbers.
    Returns:
        list of str: Decibinary numbers with new digit added.
    """
    dbin_rem = lookup_memo(val_rem, n_rem, memo)
    if dbin_rem is None:
        return []
    pad_zeros = '0'*(n-1-n_rem) 
    dbins = [str(first_digit) + pad_zeros + dbin_remi for dbin_remi in dbin_rem]
    return dbins


def get_dbin_n_digits(decimal, n, memo, dbin_list):
    """
    Get all n-digit decibinary representations of a decimal number.
    Args:
        decimal (int): Decimal number.
        n (int): Number of digits.
        memo (dict): Memoized decibinary numbers.
        dbin_list (list): Ordered list of decibinary numbers found 
            thus far.
    
    Returns:
        [memo, dbin_list] -> (dict, list of str). Updated with n-digit
            decibinary representations.
    """
    # If decimal not in dictionary, add it
    if decimal not in memo:
        memo[decimal] = dict()
    # Add (nested) key for number of digits
    memo[decimal][n] = []
  
    # Case n = 1: At most one decibinary representation,
    # the decimal itself as the only digit
    if n == 1:
        if decimal < 10:
            dbin_val = [str(decimal)]
            memo[decimal][n] = dbin_val
            dbin_list += dbin_val
        return [memo, dbin_list]

    # Start with one as a possible first digit
    first_digit = 1
    val_rem = decimal - first_digit * 2 **(n-1)
    # Iterate while "remaining" value non-negative
    while val_rem >= 0 and first_digit < 10:
        # Iterate over possible number of digits in remaining value
        for n_rem in range(1, n):
            # Use memoized decibinary values
            dbins = update_dbin_numbers(first_digit, val_rem, n_rem, n, memo)
            memo[decimal][n] += dbins
            dbin_list += dbins
        # Increment first digit and update remaining value
        first_digit += 1
        val_rem = decimal - first_digit * 2 **(n-1)
    return [memo, dbin_list]


def get_dbin_decimal(decimal, memo, dbin_list):
    """
    Get all decibinary values associated with decimal value.
    Args:
        decimal (int): Decimal number.
        memo (dict): Memoized decibinary numbers.
        dbin_list (list): Ordered list of decibinary numbers found
            thus far.
    """
    # Max value of n
    max_n = math.floor(math.log(decimal, 2)) + 1
    for n in range(1, max_n+1):
        [memo, dbin_list] = get_dbin_n_digits(decimal, n, memo, dbin_list)
    return [memo, dbin_list]


def initialize_memo():
    """
    Initialize memoization and ordered list of decibinary numbers. 
    """
    memo = dict()
    memo[0] = dict()
    memo[0][1] = ['0']
    memo[1] = dict()
    memo[1][1] = ['1']
    dbin_list = ['0', '1']
    return [memo, dbin_list]


def get_ith_decibinary_number(i, memo, dbin_list, max_decimal):

    if i < len(dbin_list):
        return [dbin_list[i-1], memo, dbin_list, max_decimal]
    while i > len(dbin_list):
        max_decimal += 1
        [memo, dbin_list] = get_dbin_decimal(max_decimal, memo, dbin_list)
    return [dbin_list[i-1], memo, dbin_list, max_decimal]

# Complete the decibinaryNumbers function below.
def decibinaryNumbers(x):
    pass

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    q = int(input())
    [memo, dbin_list] = initialize_memo()
    max_decimal = 1
    for q_itr in range(q):
        x = int(input())
        [result, memo, dbin_list, max_decimal] = get_ith_decibinary_number(x, memo, dbin_list, max_decimal)
        fptr.write(str(result) + '\n')
    fptr.close()