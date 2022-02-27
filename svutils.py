from enum import Enum, auto

def indent(s, length=2, spaceunit=" "):
    return "\n".join([spaceunit*length + i for i in s.split("\n")])


def strgen(lst):
    txt = "\n".join(lst)
    if len(lst) == 0:
        txt = "None"

    return txt 


def strStrgen(lst):
    return strgen(list(map(str, reversed(lst))))


def joinNone(lst, joinstr=", "):
    return str(None) if len(lst) == 0 else joinstr.join(lst)


class AssignType(Enum):
    BLOCK = auto()
    NONBLOCK = auto()


assigntypeTable = dict(zip(AssignType, ["=", "<="]))