def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b


def average(numbers):
    if len(numbers) == 0:
        raise ValueError("列表不能为空")
    total = sum(numbers)
    return total / len(numbers)


if __name__ == "__main__":
    print(divide(10, 2))
    print(average([1, 2, 3]))