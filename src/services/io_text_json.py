import json, os
from typing import Any, List, Dict

def load_json(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def append_log(path: str, message: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def find_index_by_key(registros: List[Dict], talhao_id: str, data: str) -> int:
    for i, r in enumerate(registros):
        if r.get('talhao_id') == talhao_id and r.get('data') == data:
            return i
    return -1
