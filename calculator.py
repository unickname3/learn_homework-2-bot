def eval_calc(expression):
    try:
        result = eval(expression)
    except:
        result = "ERR"
    return result


def calculate(expression):
    return eval_calc(expression)


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
    ]
    for exp in expressions:
        print(f"{exp} = {calculate(exp)}")
