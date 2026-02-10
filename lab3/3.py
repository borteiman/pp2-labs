import re

def solve():
    s = input().strip()
    
    # Словари для перевода
    word_to_digit = {
        'ONE': '1', 'TWO': '2', 'THR': '3', 'FOU': '4', 'FIV': '5',
        'SIX': '6', 'SEV': '7', 'EIG': '8', 'NIN': '9', 'ZER': '0'
    }
    digit_to_word = {v: k for k, v in word_to_digit.items()}

    # Функция для превращения строки триплетов в число
    def decode(triplets):
        digits = ""
        for i in range(0, len(triplets), 3):
            digits += word_to_digit[triplets[i:i+3]]
        return int(digits)

    # Функция для превращения числа обратно в строку триплетов
    def encode(number):
        if number == 0:
            return "ZER"
        res = ""
        for d in str(number):
            res += digit_to_word[d]
        return res

    # Разделение выражения на части
    match = re.search(r'([+-/*])', s)
    op = match.group(1)
    parts = s.split(op)
    
    val1 = decode(parts[0])
    val2 = decode(parts[1])

    # Вычисление
    if op == '+':
        result = val1 + val2
    elif op == '-':
        result = val1 - val2
    elif op == '*':
        result = val1 * val2
    else: # деление
        result = val1 // val2

    print(encode(result))

solve()