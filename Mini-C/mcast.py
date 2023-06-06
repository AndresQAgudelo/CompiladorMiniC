# mcast.py
'''
Este archivo define un modelo de datos para los programas MiniC.

Básicamente, el modelo es una gran estructura de datos que representa
el contenido de un programa como objetos, no como texto.  A veces, 
esta estructura se conoce como "árbol de sintaxis abstracta" o AST.
Sin embargo, no está necesariamente ligado directamente a la sintaxis 
real del lenguaje.  Por lo tanto, preferimos pensar en ello como un 
modelo de datos más genérico.

Para hacer esto, necesita identificar los diferentes "elementos" que 
componen un programa y codificarlos en clases.  Para hacer esto, puede 
ser útil "pensar poco" el problema.  Para ilustrar, suponga que desea 
codificar la idea de "asignar un valor".  La asignación implica una 
ubicación (el lado izquierdo) y un valor como este:

	location = expression;

Para representar esto, haz una clase con solo esas partes:

	@dataclass
	class Assignment:
		location: Expression
		expr    : Expression

Ahora bien, ¿qué son "location" y "expr"?  ¿Importa?  Tal vez no.  
Todo lo que sabe es que un operador de asignación requiere ambas 
partes.  NO LO PIENSE DEMASIADO.  Se irán completando más detalles 
a medida que evolucione el proyecto.

Este archivo está dividido en secciones que describen parte de la 
especificación del lenguaje MiniC en los comentarios.  Deberá adaptar
esto al código real.

Comenzando, recomendaría no hacer este archivo demasiado elegante.  
Simplemente use definiciones de clases básicas de Python.  Puede 
agregar mejoras de usabilidad más adelante.
'''
from dataclasses import dataclass, field
from multimethod import multimeta
from typing      import List, Any



# ----------------------------------------------------------------------
# Clases Abstractas
# ----------------------------------------------------------------------
@dataclass
class Visitor(metaclass=multimeta):
    pass


@dataclass
class Node:
    '''
    Representa cualquier nodo del AST
    '''
    def accept(self, v:Visitor, *args, **kwargs):
        return v.visit(self, *args, **kwargs)


@dataclass
class Statement(Node):
    '''
    '''
    pass


@dataclass
class Expression(Node):
    '''
    '''
    pass

@dataclass
class Literal(Expression):
    pass


@dataclass
class Declaration(Statement):
    '''
    Declaraciones de funciones/variables/constantes
    '''
    pass


# ----------------------------------------------------------------------
# Clases Concretas
# ----------------------------------------------------------------------

# Declaraciones
@dataclass
class Return(Statement):
  expr: List[Expression] = field(default_factory=list)

@dataclass
class ID(Node):
    name : str
    lineno: int = 0

@dataclass
class INUMBER(Node):
    name : str

@dataclass
class FNUMBER(Node):
    name : str

@dataclass
class CONST(Node):
    name : str

@dataclass
class CHARACTER(Node):
    name : str

@dataclass
class string_literal(Node):
    name : str


@dataclass
class IfStmt(Statement):
    cond   : Expression
    cons   : List [Statement]=field(default_factory=list)
    altr   : List [Statement]=field(default_factory=list)

@dataclass
class WhileStmt(Statement):
	cond: Expression
	body: List[Statement]=field(default_factory=list)


@dataclass
class For(Statement):
  init : Statement
  expr : Expression
  post : Statement
  stmts: List[Statement]=field(default_factory=list)

@dataclass
class Continue(Statement):
	lineno: int = 0

@dataclass
class Break(Statement):
	lineno: int = 0
	
@dataclass
class CompoundStmt(Statement):
	stmts: List[Statement]=field(default_factory=list)
	
@dataclass
class NullStmt(Statement):
	name: str=';'


@dataclass
class Parameter(Declaration):
  int : str
  name: str
#------------------------------------------------------------
#Expression
#------------------------------------------------------------

@dataclass
class Unary(Expression):
	op: str
	expr: Expression
	
@dataclass
class Binary(Expression):
	left : Expression
	op   : str
	right: Expression


@dataclass
class Return(Statement):
    expr: Expression = None
    lineno: int = 0
	
@dataclass
class Literal(Expression):
	value: Any

	
@dataclass
class Variable(Literal):
    name: str
    
@dataclass
class Call(Expression):
	func: str
	args: List[Expression] = field(default_factory=list)
	
@dataclass
class Array(Expression):
  expr : Expression
  index: Expression
	
	

#------------------------------------------------------------
#Declaration
#------------------------------------------------------------

@dataclass
class FuncDeclaration(Declaration):
	name: str
	params: List[Expression]=field(default_factory=list)
	body: List[Statement]=field(default_factory=list)
	Static:bool=False
	lineno: int = 0

@dataclass
class VarDeclaration(Declaration):
	name: str
	expr: Expression
	Ext:bool=False
	Static : bool = False
	lineno: int = 0

@dataclass
class ConstDeclaration(Declaration):
    name: str
    value: Expression
    
@dataclass
class TypeDeclaration(Statement):
    Type: str
    body: Statement
    lineno: int = 0

@dataclass
class FuncDeclarationStmt(Statement):
	name: str
	body: List[Statement]=field(default_factory=list)

@dataclass
class TranslationUnit(Statement):
	decls : List[Statement]

@dataclass
class Parameter_declaration(Statement):
	decls : List[Statement]



@dataclass
class ParamList(Declaration):
    params  : List[Parameter]
    ellipsis: bool = False
