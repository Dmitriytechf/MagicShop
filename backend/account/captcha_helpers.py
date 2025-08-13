from random import randint

from captcha.helpers import math_challenge


def custom_math_challenge():
    a = randint(5, 10)
    b = randint(5, 15)
    result = a * b

    return f"{a} * {b} = ", str(result)
