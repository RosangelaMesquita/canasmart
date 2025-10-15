from typing import List, Dict, Tuple
import statistics

def calc_perda_percentual(massa_pre_colheita_kg: float, massa_pos_colheita_kg: float) -> float:
    try:
        if massa_pre_colheita_kg <= 0:
            return 0.0
        perda = (massa_pre_colheita_kg - massa_pos_colheita_kg) / massa_pre_colheita_kg * 100.0
        return round(max(0.0, perda), 2)
    except Exception:
        return 0.0

def kpis_perdas(registros: List[Dict]) -> Dict[str, float]:
    perdas = [r.get('perda_percentual', 0) for r in registros if r.get('perda_percentual') is not None]
    if not perdas:
        return {'media':0,'mediana':0,'dp':0,'q1':0,'q3':0}
    perdas_sorted = sorted(perdas)
    q = statistics.quantiles(perdas_sorted, n=4, method='inclusive')
    q1, q3 = q[0], q[2]
    return {
        'media': round(statistics.mean(perdas_sorted), 2),
        'mediana': round(statistics.median(perdas_sorted), 2),
        'dp': round(statistics.pstdev(perdas_sorted), 2),
        'q1': round(q1, 2),
        'q3': round(q3, 2),
    }

def classificar_nivel_tecnologia(indices: Tuple[bool,bool,bool]) -> str:
    score = sum(1 for v in indices if v)
    return ('baixa','média','alta')[min(score,2)]

def is_outlier_zscore(valor: float, media: float, dp: float, z: float = 2.5) -> bool:
    if dp == 0:
        return False
    return abs((valor - media)/dp) > z

def iqr_bounds(perdas_sorted: List[float]) -> Tuple[float,float,float,float]:
    import statistics
    if len(perdas_sorted) < 4:
        return (0.0, 0.0, float("-inf"), float("inf"))
    q = statistics.quantiles(perdas_sorted, n=4, method='inclusive')
    q1, q3 = q[0], q[2]
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    return (q1, q3, low, high)
