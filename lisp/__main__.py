# 03/08/22
# __main__.py
import sys
import operator as op
import lisp
from parser import AST

"""
Flexible lisp interpreter built in python.
"""

builtins = {
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "**": op.pow,
    "/": op.truediv,
    "//": op.floordiv,
    "%": op.mod,

    "&": lambda a, b: a & b,
    "^": lambda a, b: a ^ b,
    "|": lambda a, b: a | b,
    "~": lambda n: ~n,

    "==": op.eq,
    "!=": op.ne,
    "<": op.lt,
    "<=": op.le,
    ">": op.gt,
    ">=": op.ge,

    "or": lambda a, b: a or b,
    "and": lambda a, b: a and b,
    "xor": lambda a, b: bool(a) ^ bool(b),
    "not": lambda p: not p,

    "max": max,
    "min": min,

    "print": print,
    "tuple": lambda *args: tuple(i if isinstance(i, tuple) else i for i in args)
}

with open(sys.argv[1]) as file:
    source = file.read()

ast = AST.parse(source, sys.argv[1])
lisp.eval(ast.ast, builtins.copy())
