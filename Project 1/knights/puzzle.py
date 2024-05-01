from logic import *

# Define symbols
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Base knowledge for any environment
KNOWLEDGE = And(
    Not(And(AKnight, AKnave)),  # A cannot be both a knight and a knave
    Not(And(BKnight, BKnave)),  # B cannot be both a knight and a knave
    Not(And(CKnight, CKnave)),  # C cannot be both a knight and a knave
    Biconditional(AKnight, Not(AKnave)),  # A is a knight if and only if A is not a knave
    Biconditional(BKnight, Not(BKnave)),  # B is a knight if and only if B is not a knave
    Biconditional(CKnight, Not(CKnave))   # C is a knight if and only if C is not a knave
)

# Puzzle 0: A says "I am both a knight and a knave."
knowledge0 = And(
    KNOWLEDGE,
    Implication(AKnight, And(AKnight, AKnave))  # If A is a knight, then A's statement is true
)

# Puzzle 1: A says "We are both knaves." B says nothing.
knowledge1 = And(
    KNOWLEDGE,
    Biconditional(AKnight, And(AKnave, BKnave))  # A is a knight if and only if both are knaves
)

# Puzzle 2: A says "We are the same kind." B says "We are of different kinds."
knowledge2 = And(
    KNOWLEDGE,
    Biconditional(Or(And(AKnave, BKnave), And(AKnight, BKnight)), AKnight),
    Biconditional(Not(Or(And(AKnave, BKnave), And(AKnight, BKnight))), BKnight)
)

# Puzzle 3: Complex scenario involving statements by A, B, and C
knowledge3 = And(
    KNOWLEDGE,
    Biconditional(CKnave, BKnight),
    Biconditional(AKnight, CKnight),
    Biconditional(And(AKnight, AKnave), BKnight)  # This line might need revisiting for logic accuracy
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        for symbol in symbols:
            if model_check(knowledge, symbol):
                print(f"    {symbol}")

if __name__ == "__main__":
    main()
