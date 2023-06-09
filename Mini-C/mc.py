'''
mc.py

Angel Augusto Agudelo Z
Compilador MiniC en Python - Front-end

Este es el programa principal para el compilador, que
simplemente analiza las opciones de la línea de comandos,
determina qué archivos fuente leer y escribir, e invoca
las diferentes etapas del compilador propiamente dicho.
'''

import argparse
from contextlib  import redirect_stdout
from dataclasses import dataclass
from rich        import print
import sys
from subprocess import check_call

from mclex import Lexer
from mcast import *
from mcparse import Parser
from checker import *
from render import RenderAST
# from mclex       import print_lexer
# from mcparse     import Parser
# from mcast       import *


def parse_args():
    '''
    Configuracion command line interfase
    '''
    cli = argparse.ArgumentParser(
    prog='mc.py',
    description='Compiler for MiniC programs')

    cli.add_argument(
    '-v', 
    '--version',
    action='version',
    version='0.8')

    fgroup = cli.add_argument_group('Formatting options')

    fgroup.add_argument(
    'files',
    type=str,
    nargs='+',
    help='MiniC program file to compile')

    mutex = fgroup.add_mutually_exclusive_group()

    mutex.add_argument(
    '-l', 
    '--lex',
    action='store_true',
    default=False,
    help='Store output of lexer')

    mutex.add_argument(
    '-d',
    '--dot',
    action='store_true',
    default=False,
    help='Generate AST graph as DOT format')

    mutex.add_argument(
    '-p',
    '--par',
    action='store_true',
    help='Generate AST graph as png format')

    mutex.add_argument(
    '--sym',
    action='store_true',
    help='Dump the symbol table')

    return cli.parse_args()

if __name__ == '__main__':
    args = parse_args()
    # print(args)
    
    l = Lexer()
    p = Parser()

    for i in args.files:
        
        txt = open(i, encoding='utf-8').read()
        tokens = l.tokenize(txt)

        if args.lex:
            print(f"{i}, --------------------- LEXER ----------------------")
            for token in tokens: 
                print(token)
        
        ast = p.parse(l.tokenize(txt))
        dot = RenderAST.render(ast)

        if args.dot: 
            print(f"{i}, --------------------- DOT ----------------------")
            f = open(f'{i}.dot','w')
            f.write(str(dot))
            f.close()

        if args.par:
            print(f"{i}, --------------------- PARSER ----------------------")
            print(ast)

        checker = Checker().check(ast, symtable = args.sym)


    # print("Archivo minic.txt creado con exito")
    # print(ast)
