from functions.run_python_file import run_python_file


def test():
    print("First Test:")
    result = run_python_file("calculator", "main.py")
    print(result)

    print("Second Test:")
    result = run_python_file("calculator", "tests.py")
    print(result)

    print("Third Test:")
    result = run_python_file("calculator", "../main.py")
    print(result)

    print("Fourth Test:")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)


if __name__ == "__main__":
    test()