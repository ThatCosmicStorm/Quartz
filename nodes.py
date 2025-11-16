
from dataclasses import dataclass
from tokendef import Tag


@dataclass
class Node:
    pass


@dataclass
class Stmt(Node):
    pass


@dataclass
class Expr(Node):
    pass


@dataclass
class ExprStmt(Expr, Stmt):
    pass


@dataclass
class Identifier(Expr):
    name: str


@dataclass
class Program:
    body: list[Stmt]


@dataclass
class Boolean(Expr):
    value: bool


@dataclass
class Integer(Expr):
    value: int


@dataclass
class Float(Expr):
    value: float


@dataclass
class String(Expr):
    value: str


@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str | Tag
    right: Expr


@dataclass
class UnaryOp(Expr):
    op: str | Tag
    operand: Expr


@dataclass
class Initialization(Stmt):
    name: Identifier
    value: Expr
    alias: Identifier | None = None
    type_: str | None = None
    immutable: bool = False


@dataclass
class Alias(Stmt):
    name: Identifier
    alias_of: Identifier


@dataclass
class Construct(Stmt):
    name: Identifier
    alias: Identifier | None = None


@dataclass
class Assignment(Stmt):
    target: Identifier
    op: str | Tag
    value: Expr


@dataclass
class CallParameter:
    value: Expr
    argument: str | None = None


@dataclass
class FuncCall(ExprStmt):
    name: Identifier
    args: list[CallParameter]


@dataclass
class MethodCall(ExprStmt):
    object_: Identifier
    call: FuncCall


@dataclass
class Parameter:
    name: Identifier
    type_: str | None = None
    preset: Expr | None = None


@dataclass
class PipelineStage:
    func: Identifier
    params: list[Parameter] | Expr
    self_: bool = False
    object_: Identifier | None = None


@dataclass
class Pipeline(ExprStmt):
    source: Expr
    stages: list[PipelineStage]


@dataclass
class BasicImport(Stmt):
    module: Identifier
    alias: Identifier


@dataclass
class SelectiveImport(Stmt):
    origin: Identifier
    all_: bool = False
    imports: list[list[Identifier]] | None = None


@dataclass
class Return(Stmt):
    value: Expr


@dataclass
class IfBranch:
    condition: Expr
    body: list[Stmt]


@dataclass
class IfStmt(Stmt):
    branches: list[IfBranch]
    else_body: list[Stmt] | None = None


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: list[Stmt]
    until: bool = False


@dataclass
class ForStmt(Stmt):
    range_: list[Identifier | Tag]
    var: Identifier | None
    body: list[Stmt]


@dataclass
class FuncDef(Stmt):
    name: Identifier
    parameters: list[Parameter]
    body: list[Stmt]
    returns: list[str]
