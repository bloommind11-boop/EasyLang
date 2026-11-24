# EasyLang

**Code in English. Think in Logic. Create with EasyLang.**

EasyLang is an experimental, beginner-friendly programming language that uses readable, English-style commands. This repository contains its Python interpreter and a small desktop code editor called **EasyLang Studio**.

> EasyLang is an early-stage learning project. Its syntax and behavior may change as the language develops.

## Features currently implemented

- Display text with `Show`
- Create variables with `Make`
- Basic arithmetic: `Add`, `Subtract`, `Multiply`, and `Divide`
- Conditional blocks using `If`, `Else`, and `End`
- `Repeat` loops
- `While` loops
- Define and call functions with parameters
- Ask the user for input with `Ask`
- Comments beginning with `#`
- Desktop editor with open, save, run, and an output panel

## Example

```easy
Make age = 18

If age is greater than 15
    Show You are eligible
Else
    Show You are not eligible
End
```

More examples are in the `examples/` folder. `hello.easy` demonstrates several currently supported features.

## Run EasyLang from Python

**Requirements:** Python 3.10 or newer. The desktop editor uses Python's built-in Tkinter library.

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run the sample program:

   ```bash
   python main.py
   ```

4. Open the desktop editor:

   ```bash
   python editor.py
   ```

In EasyLang Studio, open a `.easy` file and press **Run** (or F5).

## Build the Windows desktop application

PyInstaller is only needed to build the executable; it is not needed to run the source version.

```bash
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name EasyLangStudio editor.py
```

The generated executable is placed in the `dist/` folder.

## Repository structure

```text
EasyLang/
├── editor.py
├── interpreter.py
├── main.py
├── hello.easy
├── EasyLangStudio.spec
├── examples/
│   └── basics.easy
├── README.md
├── LICENSE
└── .gitignore
```

## Current limitations

EasyLang is a prototype, not yet a production-ready language. The current interpreter has a deliberately small syntax and does not yet provide features such as modules, classes, a package manager, or a browser-based runtime. Error handling and parsing will continue to improve.

## Contributing and feedback

Suggestions, bug reports, and beginner-friendly example programs are welcome. Please describe the EasyLang code you tried and what you expected to happen.

## License

This project is distributed under the MIT License. See `LICENSE`.
