
from src.salomon.extraction import FunctionExtractor


def main():
    print("Hello from salomon!")

    extractor = FunctionExtractor()

    all_functions = extractor.from_repo("https://github.com/hackerman70000/salomon")
    for func in all_functions:
        print(func.file_path, func.name)

if __name__ == "__main__":
    main()
