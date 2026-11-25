# Password Strength Analyzer

A collaborative Password Strength Analyzer project developed by a team of 5 members for a Discrete Structures course.

This Python desktop application demonstrates password analysis using concepts from discrete mathematics, including character-set counting, permutations, combinations, inclusion-exclusion, entropy, and an illustrative average guessing-time calculation.

## Project Features

- Detects uppercase letters, lowercase letters, digits, and special characters.
- Calculates the possible character alphabet size.
- Demonstrates the rule of product.
- Performs permutations and combinations calculations.
- Demonstrates the inclusion-exclusion principle.
- Calculates password entropy.
- Estimates illustrative password guessing time.
- Provides password strength categories.
- Displays demonstration password examples.
- Includes a desktop GUI using Tkinter.
- Supports optional entropy visualization.

## Project Structure

```text
password_strength_analyzer/
│
├── analyzer/
│   ├── __init__.py
│   ├── alphabet.py
│   ├── counting.py
│   ├── dataset.py
│   ├── graph.py
│   ├── gui.py
│   └── security.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3
- Tkinter
- matplotlib
- numpy

## Installation on Windows

1. Clone the repository:

```bash
git clone https://github.com/Qalandar424/password-analyzer.git
```

2. Open the project folder:

```bash
cd password-analyzer
```

3. Create a virtual environment:

```bash
python -m venv env
```

4. Activate the virtual environment:

```powershell
env\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
python main.py
```

## Team Project

This project is collaboratively developed by 5 team members using Git and GitHub.

Each member contributes to the project through individual development work and version control.

## Important Notes

- Guessing rates are illustrative assumptions, not predictions of real-world password cracking time.
- Sample passwords are demonstration data, not a downloaded or verified RockYou/SecLists dataset.
- Never enter a real password that you currently use.

## License

This project is developed for educational purposes.