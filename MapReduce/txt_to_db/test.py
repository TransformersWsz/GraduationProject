def read_file(filename: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("read {0}...".format(filename))
            print("before...")
            for i in range(5):
                func(*args)
            print("after...")
        return wrapper
    return decorator

@read_file("myfolder")
def test(s: str):
    print(s)

if __name__ == "__main__":
    test("this is test...")

