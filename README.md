# Password Strength Analyzer

A Python desktop application for a Discrete Structures course. It demonstrates
character-set counting, permutations, inclusion-exclusion, entropy, and an
illustrative average guessing-time calculation.

## Project structure

- `main.py`: application entry point
- `analyzer/alphabet.py`: detects character classes and alphabet size
- `analyzer/counting.py`: rule of product, permutations, combinations,
  inclusion-exclusion, and a small brute-force verification
- `analyzer/security.py`: entropy, estimated cracking time, formatting,
  strength category, and baseline score
- `analyzer/dataset.py`: demonstration password examples and report
- `analyzer/graph.py`: optional entropy graph
- `analyzer/gui.py`: Tkinter interface

## Requirements

- Python 3
- Tkinter (usually included with standard Python on Windows)
- matplotlib
- numpy

## Setup on Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Notes

The guessing rates in the application are illustrative assumptions, not
predictions of real-world cracking time. The sample passwords are demonstration
data, not a downloaded or verified RockYou/SecLists dataset. Do not enter a
real password that you currently use.
