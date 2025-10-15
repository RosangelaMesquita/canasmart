from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class RegistroColheita:
    talhao_id: str
    data: str
    equipamento: str
    massa_pre: float
    massa_pos: float
    perda_percentual: float
    tecnologia: str

def to_table(registros: List[RegistroColheita]) -> List[Dict]:
    return [asdict(r) for r in registros]
