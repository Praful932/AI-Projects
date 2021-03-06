from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# A is a knight if (what a says) is true
# A is a knave if (what a says) is false

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Biconditional(AKnight,And(AKnight,AKnave)),
    Implication(Not(AKnight),AKnave),
    Implication(Not(AKnave),AKnight)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(AKnight,And(AKnave,BKnave)),
    Implication(Not(AKnight),AKnave),
    Implication(Not(AKnave),AKnight),
    Implication(AKnave,Not(BKnave)),
    Implication(Not(BKnight),BKnave),
    Implication(Not(BKnave),BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnight,Biconditional(AKnight,BKnight)),
    Biconditional(BKnight,AKnave),
    Implication(Not(AKnight),AKnave),
    Implication(Not(BKnight),BKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight,Not(And(AKnight,AKnave))),
    Biconditional(BKnight,Biconditional(AKnight,AKnave)),
    Biconditional(BKnight,Biconditional(CKnight,CKnave)),
    Biconditional(CKnight,Biconditional(AKnight,AKnight)),
    Implication(Not(AKnave),AKnight),
    Implication(Not(BKnight),BKnave),
    Implication(Not(CKnave),CKnight)
)


def main():
    # print(knowledge0.symbols())
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
