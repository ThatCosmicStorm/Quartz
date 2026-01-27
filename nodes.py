"""*Carries `Node` and `BinaryOp`*."""

##############################
# IMPORTS
##############################

from typing import NamedTuple

from tokendef import Tag

##############################
# NODES
##############################


class Node(NamedTuple):
    """*All statements and almost all expressions*.

    Operations with two operands have their own Node.
    """

    name: str
    data: object


class BinaryOp(NamedTuple):
    """*Binary operation: two operands*.

    Can also store unary operations by setting `left=None`.
    """

    op: str | Tag
    left: object
    right: object


##############################
# END OF FILE
##############################
