from pathlib import Path
import sys


x = Path(__file__).resolve().parent.parent
print(type(x), x)
