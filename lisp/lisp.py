# 03/08/22
# lisp.py
from typing import Iterable
from collections import ChainMap
from grammar import *

class Procedure:
    def __init__(self, signature, body, env):
        self.signature, self.body, self.local = [i.id for i in signature], body, env

    def __call__(self, args, *a):
        if not isinstance(args, Iterable):
            local = ChainMap({self.signature[0]: args}, self.local)
        else:
            local = ChainMap(dict(zip(self.signature, args), self.local))
        return eval(self.body, local)

def eval_stmnt(stmnt, env):
    match stmnt:
        case Let(_, _):
            env[stmnt.target.id] = eval(stmnt.body, env)
        case If(_, _, _):
            if eval(stmnt.clause, env):
                return eval(stmnt.action, env)
            else:
                return eval(stmnt.orelse, env)
        case Function(_, _):
            return Procedure(stmnt.args, stmnt.body, env)
        case Macro(_, _):
            raise NotImplementedError("Macros are not implemented.")
        case _:
            raise ValueError(f"Invalid statement: {stmnt}")

def eval_expr(expr, env):
    match expr:
        case Const(_):
            return expr.value
        case Ident(_):
            if expr.id not in env:
                raise NameError(f"Variable {expr.id} is undefined")
            return env[expr.id]
        case Call(_, _):
            args = eval(expr.args, env)
            func = eval(expr.func, env)
            if isinstance(args, Iterable):
                return func(*args)
            return func(args)
        case BinOp(_, _, _):
            binop = eval(expr.op, env)
            left = eval(expr.left, env)
            right = eval(expr.right, env)
            return binop(left, right)
        case _:
            raise ValueError(f"Invalid expression: {expr}")
    return

def eval(lisp, env):
    match lisp:
        case None | []:
            return
        case str(_):
            if lisp not in env:
                raise NameError(f"Variable {lisp} is undefined")
            return env[lisp]
        case _ if isinstance(lisp, Exprs):
            return eval_expr(lisp, env)
        case _ if isinstance(lisp, Stmnts):
            return eval_stmnt(lisp, env)
        case [_]:
            return eval(lisp[0], env)
        case [_, *_]:
            return [eval(lisp[0], env), eval(lisp[1:], env)]
        case _:
            raise ValueError(f"Invalid expression or statement: {lisp}")
