# 03/07/22
# grammar.py
from __future__ import annotations

from collections import deque
from dataclasses import dataclass

"""
Grammar:

Lisp
    Stmnt => If
            | Let
            | Macro
            | Function
            | Expr => Const
                    | Ident
                    | Call
                    | BinOp
"""

__all__ = (
    "Lisp", "Stmnt", "Expr", "If",
    "Let", "Macro", "Function",
    "Expr", "Const", "Ident", "Call",
    "BinOp", "Stmnts", "Exprs"
)

def lispcls(cls):
    # Helper function to make all dataclasses iterable.
    cls = dataclass(cls)
    def __iter__(self):
        return iter(dataclasses.astuple(self))
    cls.__iter__ = __iter__
    return cls

class Lisp:
    pass

class Stmnt(Lisp):
    pass

class Expr(Stmnt):
    pass

# Statements
@lispcls
class If(Stmnt):
    clause: BinOp
    action: Expr
    orelse: Expr | None = None

@lispcls
class Let(Stmnt):
    target: Ident
    body: Expr

@lispcls
class Macro(Stmnt):
    macro: Ident
    definition: Lisp

@lispcls
class Function(Stmnt):
    args: list[Ident]
    body: Expr

# Expressions
@lispcls
class Const(Expr):
    value: int | float

@lispcls
class Ident(Expr):
    id: str

@lispcls
class Call(Expr):
    func: Expr
    args: Expr

@lispcls
class BinOp(Expr):
    op: Expr
    left: Expr
    right: Expr

@lispcls
class Vector(Expr):
    items: tuple[Expr]

Stmnts = (
    If, Let, Macro, Function, Expr
)

Exprs = (
    Const, Ident,
    Call, BinOp
)
