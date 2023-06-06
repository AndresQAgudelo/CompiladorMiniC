from mcast import *
import graphviz as gpv

from mclex import *
from mcparse import *
from rich import print

class RenderAST(Visitor):
    node_default = {
        'shape' : 'box',
        'color' : 'deepskyblue',
        'style' : 'filled',
    }
    edge_default = {
        'arrowhead' : 'none'
    }

    def __init__(self):
        self.dot = gpv.Digraph('AST', comment='AST')
        self.dot.attr('node', **self.node_default)
        self.dot.attr('edge', **self.edge_default)
        self.seq = 0
    
    def __repr__(self):
        return self.dot.source

    def __str__(self):
        return self.dot.source
    
    def name(self):
        self.seq += 1
        return f'n{self.seq:02d}'

    @classmethod
    def render(cls, n:Node):
        dot = cls()
        n.accept(dot)
        return dot.dot
    
    def visit(self, n:TranslationUnit):
        name = self.name()
        self.dot.node(name, label='Funcion')
        for i in n.decls:
            self.dot.edge(name, i.accept(self))

    def visit(self, n:FuncDeclaration):
        name = self.name()
        self.dot.node(name, label=f"Func Declaration\ntype:{n.name} \nexternal:{n.Static}\n")
        self.dot.edge(name, n.params.accept(self))
        for i in n.body:
            self.dot.edge(name, i.accept(self))
        return name
    def visit(self, n:FuncDeclarationStmt):
        name = self.name()
        self.dot.node(name, label=f"Funcion \nname:{n.name} \n")
        for i in n.body:
            self.dot.edge(name, i.accept(self))
        return name
    def visit(self, n:TypeDeclaration):
        name = self.name()
        if type(n.body) != str:
            self.dot.node(name, label=f"Param\nType:{n.Type} \n")
            self.dot.edge(name, n.body.accept(self))
        else: 
             self.dot.node(name, label=f"Param\nType:{n.Type} \n name:{n.body}")
        return name
    
    def visit(self, n:Parameter_declaration):
        name = self.name()
        self.dot.node(name, label='ParamDeclaracion')
        for i in n.decls:
            self.dot.edge(name, i.accept(self))
    
    def visit(self, n:VarDeclaration):
        name = self.name()
        if type(n.expr ) != str: 
            self.dot.node(name, label=f'Var declaration\ntype: {n.name}')
            self.dot.edge(name, n.expr.accept(self))
        else: 
            self.dot.node(name, label=f'Var declaration\ntype: {n.name}\nname: {n.expr}')
        return name
    
    def visit(self, n:WhileStmt):
        name = self.name()
        self.dot.node(name, label=f'while\cond: ')
       
        self.dot.edge(name, n.cond.accept(self))
        for i in n.body:
            self.dot.edge(name, i.accept(self))
        
        return name
    
    def visit(self, n:For):
        name = self.name()
        self.dot.node(name, label=f'For\cond: ')
       
        self.dot.edge(name, n.init.accept(self))
        self.dot.edge(name, n.expr.accept(self))
        self.dot.edge(name, n.post.accept(self))
        for i in n.stmts:
            self.dot.edge(name, i.accept(self))
        
        return name
     
    def visit(self, n:IfStmt):
        name = self.name()
        self.dot.node(name, label=f'If\cond: ')
        self.dot.edge(name, n.cond.accept(self))
        for i in n.cons:
            self.dot.edge(name, i.accept(self))

        for i in n.altr:
            self.dot.edge(name, i.accept(self),label=f'Else:')
        
        return name


    def visit(self, n:Unary):
        name = self.name()
        self.dot.node(name, label=f"Unary\\nop={n.op}")
        self.dot.edge(name, n.expr.accept(self))
        return name
    
    def visit(self, n:Binary):
        name = self.name()
        self.dot.node(name, label=f"Binary\\nop:{n.op}")
        self.dot.edge(name, n.left.accept(self))
        self.dot.edge(name, n.right.accept(self))
        return name

    def visit(self, n:Variable):
        name = self.name()
        self.dot.node(name, label=f"Ident\\nname={n.name}")
        return name
    
    def visit(self, n:Break):
        name = self.name()
        self.dot.node(name, label=f"Break")
        return name
    
    def visit(self, n:Continue):
        name = self.name()
        self.dot.node(name, label=f"Continue")
        return name
    
    def visit(self, n:ID):
        name = self.name()
        self.dot.node(name, label=f"ID={n.name}")
        return name
    
    def visit(self, n:INUMBER):
        name = self.name()
        self.dot.node(name, label=f"INUMBER={n.name}")
        return name
    
    def visit(self, n:FNUMBER):
        name = self.name()
        self.dot.node(name, label=f"FNUMBER={n.name}")
        return name
    
    def visit(self, n:CONST):
        name = self.name()
        self.dot.node(name, label=f"CONST={n.name}")
        return name
    
    def visit(self, n:CHARACTER):
        name = self.name()
        self.dot.node(name, label=f"CHARACTER={n.name}")
        return name
    
    def visit(self, n:string_literal):
        name = self.name()
        self.dot.node(name, label=f"string literal={n.name}")
        return name
    
    def visit(self, n:Return):
        name = self.name()
        self.dot.node(name, label=f"Return:")
        if n.expr:
            self.dot.edge(name, n.expr.accept(self))
        return name
    
    def visit(self, n:Call):
        name = self.name()
        self.dot.node(name, label=f"Call")
        self.dot.edge(name, n.func.accept(self))
        for i in n.args:
            self.dot.edge(name, i.accept(self))
        return name
    
    def visit(self, n:Array):
        name = self.name()
        self.dot.node(name, label=f"Array")
        self.dot.edge(name, n.expr.accept(self))
        self.dot.edge(name, n.index.accept(self))
        
        return name

    
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} [ fname1 [ fname2 ... ] ]   --ast")
        exit(1)
    

    l = Lexer()
    p = Parser()
    
    data = open(sys.argv[1], encoding='utf-8').read()

    ast = p.parse(l.tokenize(data))
    dot = RenderAST.render(ast)
    #dot = RenderAST()
    #ast.accept(dot)

    print(dot)
    dot.save("AST.dot")
    