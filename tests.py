from functions.get_files_content import get_file_content

def test():
    result = get_file_content("calculator", "lorem.txt")
    print("Result for current directory:")
    print(result)
    print("")

test()

if __name__ == "__main__":
    test()