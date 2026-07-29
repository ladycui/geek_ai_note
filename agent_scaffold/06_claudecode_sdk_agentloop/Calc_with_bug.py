def divide(a, b):
    # bug: 没有处理除数为 0 的情况，会直接抛出未捕获的异常
    return a / b


def average(numbers):
    # bug: 空列表时会除以 0
    total = sum(numbers)
    return total / len(numbers)


if __name__ == "__main__":
    print(divide(10, 2))
    print(average([1, 2, 3]))