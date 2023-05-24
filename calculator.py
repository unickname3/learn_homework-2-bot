def is_math_expression(expression: str) -> bool:
    good_symbols = "0123456789+*/- .()"
    for c in expression:
        if c not in good_symbols:
            return False
    return True


def my_calculator(expression):
    pass


def calculate(expression):
    if not is_math_expression(expression):
        return "Не могу рассчитать это выражение."

    # TODO: Добавить кастомный калькулятор
    try:
        result = eval(expression)
    except ZeroDivisionError:
        return "На ноль делить нельзя!"
    except SyntaxError:
        return "Исправьте синтаксическую ошибку в выражении."
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
