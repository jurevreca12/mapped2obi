from dataclasses import dataclass
from forastero import BaseTransaction

@dataclass(kw_only=True)
class ObiChATrans(BaseTransaction):
    addr: int = 0
    wdata: int = 0
    we: bool = True
    be: int = 0

@dataclass(kw_only=True)
class ObiChRTrans(BaseTransaction):
    rdata: int = 0

@dataclass(kw_only=True)
class ObiChRBackpressureTrans(BaseTransaction):
    cycles: int = 1
    ready: bool = False
