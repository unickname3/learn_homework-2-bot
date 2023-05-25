"""
Shunting yard algorithm
https://habr.com/ru/articles/273253/
"""

# =================== copied code begin =================================

OPERATORS = {
    "+": (1, lambda x, y: x + y),
    "-": (1, lambda x, y: x - y),
    "*": (2, lambda x, y: x * y),
    "/": (2, lambda x, y: x / y),
}


def parse(formula_string):
    number = ""
    for s in formula_string:
        if s in "1234567890.":  # если символ - цифра, то собираем число
            number += s
        elif (
            number
        ):  # если символ не цифра, то выдаём собранное число и начинаем собирать заново
            yield float(number)
            number = ""
        if (
            s in OPERATORS or s in "()"
        ):  # если символ - оператор или скобка, то выдаём как есть
            yield s
    if number:  # если в конце строки есть число, выдаём его
        yield float(number)


def shunting_yard(parsed_formula):
    stack = []  # в качестве стэка используем список
    for token in parsed_formula:
        # если элемент - оператор, то отправляем дальше все операторы из стека,
        # чей приоритет больше или равен пришедшему,
        # до открывающей скобки или опустошения стека.
        # здесь мы пользуемся тем, что все операторы право-ассоциативны
        if token in OPERATORS:
            while (
                stack
                and stack[-1] != "("
                and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]
            ):
                yield stack.pop()
            stack.append(token)
        elif token == ")":
            # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
            # а открывающую скобку выкидываем из стека.
            while stack:
                x = stack.pop()
                if x == "(":
                    break
                yield x
        elif token == "(":
            # если элемент - открывающая скобка, просто положим её в стек
            stack.append(token)
        else:
            # если элемент - число, отправим его сразу на выход
            yield token
    while stack:
        yield stack.pop()


def shunting_calc(expression):
    polish = shunting_yard(parse(expression))
    stack = []
    for token in polish:
        if token in OPERATORS:  # если приходящий элемент - оператор,
            y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
            stack.append(
                OPERATORS[token][1](x, y)
            )  # вычисляем оператор, возвращаем в стек
        else:
            stack.append(token)
    return stack[0]  # результат вычисления - единственный элемент в стеке


# =================== copied code end =================================


def is_math_expression(expression: str) -> bool:
    good_symbols = "0123456789+*/-.()"
    for c in expression:
        if c not in good_symbols:
            return False
    return True


simple_calc = eval  # probably unsafe, but fast to implement


def calculate(expression, calculate_function=shunting_calc):
    expression = expression.replace(" ", "")
    if not is_math_expression(expression):
        return "Не могу рассчитать это выражение."
    try:
        result = calculate_function(expression)
    except ZeroDivisionError:
        return "На ноль делить нельзя!"
    except (SyntaxError, IndexError, ValueError):
        return "Выражение написано некорректно."
    return result


if __name__ == "__main__":
    expressions = [
        "test",
        "42",
        "1+1",
        "2*4",
        "17/0",
        "12 - 5",
        "23 + 6*8",
        "2 * (5+11)",
        "5 + 2 * )",
        "7.1 + 8.1 - ..",
        "(5.2 + 0.8) / 6",
        "0.1 + 0.2",
    ]
    for exp in expressions:
        print(f"{exp} = {calculate(exp)}")
