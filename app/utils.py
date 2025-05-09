def validate_cpf(cpf: str) -> str:
    invalid_cpf_message = "Invalid CPF."

    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    if len(set(numbers)) == 1:
        raise ValueError(invalid_cpf_message)

    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        raise ValueError(invalid_cpf_message)

    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        raise ValueError(invalid_cpf_message)

    return cpf
