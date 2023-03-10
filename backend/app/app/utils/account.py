import random


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def calculate_luhn(partial_card_number):
    check_digit = luhn_checksum(int(partial_card_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit


def generate_card_number(prefix):
    # Generate the rest of the card number as random digits
    rest = "".join([str(random.randint(0, 9)) for _ in range(11)])

    # Calculate the check digit
    check_digit = calculate_luhn(prefix + rest)

    # Return the card number as a string
    print("!"*100)
    print(prefix + rest + str(check_digit))
    return prefix + rest + str(check_digit)
