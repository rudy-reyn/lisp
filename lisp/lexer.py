# 03/02/22
# lexer.py
import re
from collections import deque
from typing import NamedTuple

from grammar import Const, Ident

types = {
    "PARENTHESES", "CONSTANT",
    "KEYWORD", "IDENTIFIER", "SYMBOL"
}

keywords = {
   "@macro", "=>",
   "def", "let",
   "if", "else",
   "and", "or"
}

class Token(NamedTuple):
    token: str | Const
    type: str
    row: int
    col: int
    keyword = keywords

    @staticmethod
    def isnum(token):
        try:
            return int(token)
        except ValueError:
            pass
        try:
            return float(token)
        except ValueError:
            pass

    @staticmethod
    def isident(token,
        # Used to compile the regex only on the first function call.
        pattern=re.compile(r"([+-.*/<=>!?:$%_&~a-zA-Z^]+)([0-9]|\1)*")):
        return token not in keywords and bool(pattern.match(token))

    @classmethod
    def parse(cls, token, row, col):
        if token in "()":
            return cls(token, "PARENTHESES", row, col)
        elif token in keywords:
            return cls(token, "KEYWORD", row, col)
        elif (num := Token.isnum(token)) is not None:
            return cls(Const(num), "CONSTANT", row, col)
        elif Token.isident(token):
            return cls(Ident(token), "IDENTIFIER", row, col)
        return cls(token, "SYMBOL", row, col)

def tokenize(source, tokens="()"):
    tokenized = deque()
#     source = re.sub(r";+.*(\n)", r"\1", source)
    for row, line in enumerate(re.split("\n", source), start=1):
        if not line.strip():
            continue
        chars = [i for i in re.split(f"([{tokens}\s+])", line) if i]
        for col, token in enumerate(chars):
            if not token.isspace():
                tokenized.append(Token.parse(token, row, col))
    return tokenized

if __name__ == "__main__":
    import sys
    from pprint import pprint
    with open(sys.argv[1]) as file:
        source = file.read()
    pprint(tokenize(source))
