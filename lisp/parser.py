# 03/07/22
# parser.py
from typing import NamedTuple
from collections import deque
import re

import lexer
from grammar import *

class Node(deque):
    # TODO:
    """Replace deque in AST body with a node subclass with line and column
    information for better tracebacks"""

class BaseAST:
    def __init__(self, tokens):
        self.ast = []
        self.tokens =  tokens
        self.exception        = self.exception_traceback(Exception)
        self.value_error      = self.exception_traceback(ValueError, "Invalid code block or argument count")
        self.type_error       = self.exception_traceback(TypeError)
        self.syntax_error     = self.exception_traceback(SyntaxError)
        self.unexpected_token = self.exception_traceback(SyntaxError, "Unexpected token")
        self.unexpected_eof   = self.exception_traceback(SyntaxError, "Unexpected EOF")

    def _keyword(self, token):
        """Used for parsing keywords:

        @macro      =>
        def         let
        if          else
        and         or """
        tokens = self.tokens
        match token.token:
            case "@macro":
                raise self.exception(token, f"Macros are not yet supported '{token.token}'")
            case "=>":
                args = []
                while tokens[0].token != "(":
                    args.append(self.parse_tree())
                body = []
                while tokens[0].token != ")":
                    body.append(self.parse_tree())
                if not all(isinstance(arg, Ident) for arg in args):
                    raise self.type_error(token,
                        "Invalid argument signature - expected a single identifier or a block of identifiers:",
                        f"args: {args}", f"body: {body}")
                return Function(args, body)
            case "let":
                target = self.parse_tree()
                body =  self.parse_tree()
                if not isinstance(target, Ident):
                    raise self.type_error(token,
                            f"Invalid identifier for let binding: {target}, expected 'ident'")
                return Let(target, body)
            case "if":
                clause = self.parse_tree()
                action = self.parse_tree()
                if tokens[0].token != ")":
                    return If(clause, action, self.parse_tree())
                return If(clause, action)
            case "else":
                return self.parse_tree()
            case "and" | "or":
                left = self.parse_tree()
                right = self.parse_tree()
                return BinOp(Ident(token.token), left, right)
        raise self.type_error(token, f"'{token.token}' is not a keyword.")

    def parse_tree(self):
        tokens = self.tokens
        if len(tokens) == 0:
            raise self.unexpected_eof(None, "Unexpected EOF")
        token = tokens.popleft()
        if token.token == ")":
            raise self.unexpected_token(token)
        match token.type:
            case "PARENTHESES":
                node = []
                if tokens[0].type == "IDENTIFIER":
                    head = tokens.popleft()
                else:
                    head = None
                try:
                    while tokens[0].token != ")":
                        node.append(self.parse_tree())
                    tokens.popleft()
                except IndexError:
                    raise self.unexpected_eof(token)
                return node if head is None else Call(head.token.id, node)
            case "CONSTANT" | "IDENTIFIER":
                return token.token
            case "KEYWORD":
                # def, let, if, @macro, ...
                return self._keyword(token)
            case _:
                raise self.unexpected_token(token, "Unknown token: {token.type}")

    def exception_traceback(self, error, default=""):
        "Function factory used to proved detailed traceback for errors during tokenization."
        def wrapper(token, *msg):
            details = "\n                ".join(map(str, msg))
            traceback = (
                f"{default}:\n  "
                f"{details}\n  "
                f"Token: {token}\n  "
                f"Next 2 tokens: {list(self.tokens)[:2]}")
            return error(traceback)
        return wrapper


class AST(BaseAST):
    def __init__(self, source, filename=None):
        self.source = source
        self.filename = filename
        super(self.__class__, self).__init__(lexer.tokenize(self.source))

    @classmethod
    def parse(cls, source, filename=None):
        source = re.sub(r";+.*(\n)", r"\1", source)
        ast = cls(source, filename=filename)
        while ast.tokens:
            ast.ast.append(ast.parse_tree())
        return ast

    def exception_traceback(self, error, default=""):
        "Provides more detailed tracebacks using the provided source file and file name."
        def wrapper(token, *msg):
            lines = re.split("\n", self.source)
            row = lines[token.row - 1]
            details = "" if not msg else "\n  " + "\n                ".join(map(str, msg))
            traceback = (
                f"File {self.filename}, line {token.row}\n  "
                f"{default}:\n\t"
                f"{row}\n\t"
                + " " * token.col + " ^^^"
                f"{details}\n  "
                f"Token: {token}\n  "
                f"Next 2 tokens: {list(self.tokens)[:2]}")
            return error(traceback)
        return wrapper

if __name__ == "__main__":
    import sys
    from pprint import pprint
    with open(sys.argv[1]) as file:
        source = file.read()
    ast = AST.parse(source, sys.argv[1])
    pprint(ast)
