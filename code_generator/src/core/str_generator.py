import random


def generate_random_str(length: int = 8) -> str:
    """ Генерируем рендомную строку нужной длины"""
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    code = ''
    for i in range(length):
        code += random.choice(chars)
    return code
