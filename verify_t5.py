import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.mitigate import mitigate_bias

def test():
    sentences = [
        "Women are terrible at programming.",
        "Old people cannot use computers.",
        "Black people are extremely dangerous.",
        "Men are always so emotional.",
        "Boys are bad at math.",
        "Girls are usually bad drivers.",
        "Asian people are bad at money.",
        "Hispanic people are loud.",
        "Young people are lazy.",
        "Millennials ruined the world."
    ]
    for s in sentences:
        print(f"[{s}] -> {mitigate_bias(s)['mitigated_sentence']}")

if __name__ == '__main__':
    test()
