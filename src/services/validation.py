def ensure_float(msg: str) -> float:
    while True:
        try:
            val = float(input(msg).replace(',', '.'))
            return val
        except ValueError:
            print('Valor inválido. Digite um número.')

def ensure_str(msg: str, allow_empty=False) -> str:
    while True:
        s = input(msg).strip()
        if s or allow_empty:
            return s
        print('Campo obrigatório.')

def ensure_opcao(msg: str, opcoes):
    opcoes = [str(o).lower() for o in opcoes]
    while True:
        s = input(msg).strip().lower()
        if s in opcoes:
            return s
        print(f'Opção inválida. Escolha entre: {opcoes}')
