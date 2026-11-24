from pathlib import Path
from interpreter import execute_program


def main():
    program_file = Path(__file__).parent / "hello.easy"

    if not program_file.exists():
        print("EasyLang Error: hello.easy was not found.")
        return

    try:
        with open(program_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        print("Welcome to EasyLang!")
        print("--------------------")

        execute_program(lines)

        print("--------------------")
        print("EasyLang program finished.")

    except OSError as error:
        print(f"Could not read program: {error}")


if __name__ == "__main__":
    main()