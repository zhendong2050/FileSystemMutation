from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
sys.path.extend(['.', '..'])

import pycparser_fake_libc

from pycparser import c_parser, c_ast, parse_file, c_generator
import ast_modifier
from enum import Enum

includes=''
## pairs of a target function name and its handler name
instrument_func_dict = {'fopen' : 'fopen_handler'}

class FuncCallInstrumentor(ast_modifier.AstModifier):
    def __init__(self, debug):
        ast_modifier.AstModifier.__init__(self, debug)


    def visit_FuncCall(self, node):
        if node.name.name in instrument_func_dict :
           # print('%s called at %s' % (node.name.name, node.name.coord))
            self.instrument(node)
        if node.args:
            self.visit(node.args)


    def instrument(self, node):
        if node.name.name == 'fopen':
            self.insert_node_before(c_ast.FuncCall(c_ast.ID(instrument_func_dict[node.name.name]), c_ast.ExprList([node.args.exprs[0], node.args.exprs[1], c_ast.Constant('char*', '"'+str(node.name.coord)+'"')])),'Compound')


def ast_file(ast):
    print(includes)
    generator = c_generator.CGenerator()
    src=generator.visit(ast)
    lines = src.splitlines()
    for line in lines:
        if line.startswith('typedef '):
            continue
        print(line)


def parse_file_ast(filename):
    fake_libc_arg = "-I" + pycparser_fake_libc.directory
    ast = parse_file(filename, use_cpp=True, cpp_args=fake_libc_arg)
    return ast


def extract_includes(filename):
    f=open(filename, 'r')
    global includes
    for line in f.readlines():
        if line.startswith('#include '):
            includes=includes+line
    f.close()

# testing
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please provide the parsed file name")
    else:
        filename = sys.argv[1]
        extract_includes(filename)
        ast = parse_file_ast(filename)
        visitor= FuncCallInstrumentor(True)
        visitor.visit(ast)
        ast_file(ast)
