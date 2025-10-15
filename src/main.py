from services.validation import ensure_float, ensure_str, ensure_opcao
from services.io_text_json import load_json, save_json, append_log, find_index_by_key
from algorithms import calc_perda_percentual, kpis_perdas, is_outlier_zscore, iqr_bounds
from models import RegistroColheita
import os, datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
REG_PATH = os.path.join(DATA_DIR, 'harvest_records.json')
LOG_PATH = os.path.join(DATA_DIR, 'logs.txt')

def cadastrar_registro():
    print('\n== Novo Registro de Colheita ==')
    talhao = ensure_str('Talhão (ex: T-01): ')
    data = ensure_str('Data (YYYY-MM-DD): ')
    equip = ensure_str('Equipamento (ex: Colhedora-01): ')
    while True:
        pre = ensure_float('Massa pré-colheita (kg/ha): ')
        pos = ensure_float('Massa pós-colheita (kg/ha): ')
        if pre <= 0:
            print('A massa pré-colheita deve ser maior que zero.')
            continue
        if pos > pre:
            print('A massa pós-colheita não pode ser maior que a massa pré-colheita. Tente novamente.')
            continue
        break
    tec = ensure_opcao('Tecnologia (baixa/média/alta): ', ['baixa','média','alta'])

    perda = calc_perda_percentual(pre, pos)
    reg = RegistroColheita(talhao, data, equip, pre, pos, perda, tec)

    registros = load_json(REG_PATH, default=[])
    registros.append(reg.__dict__)
    save_json(REG_PATH, registros)

    append_log(LOG_PATH, f"{datetime.datetime.now().isoformat()} | novo registro {talhao} perda={perda}% (local)")

    print(f'Registro salvo. Perda calculada: {perda}%.')

def listar_kpis():
    registros = load_json(REG_PATH, default=[])
    k = kpis_perdas(registros)
    print('\n== KPIs de Perdas (base local) ==')
    print(f"Média: {k['media']}% | Mediana: {k['mediana']}% | DP: {k['dp']} | Q1: {k['q1']} | Q3: {k['q3']}")

def detectar_outliers_menu():
    registros = load_json(REG_PATH, default=[])
    if not registros:
        print('Sem registros.'); return

    print('\n== Detectar Outliers ==')
    print('[1] Z-score (configurar Z)')
    print('[2] IQR (boxplot)')
    opc = input('Escolha: ').strip()

    if opc == '1':
        try:
            z = float(input('Informe o valor Z (ex.: 2.0, 2.5, 3.0): ').replace(',','.'))
        except ValueError:
            z = 2.5
        perdas = [r['perda_percentual'] for r in registros]
        if not perdas:
            print('Sem perdas calculadas.'); return
        media = sum(perdas)/len(perdas)
        dp = (sum((p-media)**2 for p in perdas)/len(perdas))**0.5
        outls = [r for r in registros if is_outlier_zscore(r['perda_percentual'], media, dp, z=z)]
        print(f'\n== Outliers de Perda (Z-score>|{z}|) ==')
        if outls:
            for r in outls:
                print(f"{r['talhao_id']} {r['data']} perda={r['perda_percentual']}% equip={r['equipamento']}")
        else:
            print('Nenhum outlier.')
        return

    elif opc == '2':
        perdas = sorted([r['perda_percentual'] for r in registros])
        q1, q3, low, high = iqr_bounds(perdas)
        print(f'\n== Outliers de Perda (IQR) ==')
        print(f'Q1={round(q1,2)} | Q3={round(q3,2)} | Limites: ({round(low,2)}, {round(high,2)})')
        outls = [r for r in registros if r['perda_percentual'] < low or r['perda_percentual'] > high]
        if outls:
            for r in outls:
                print(f"{r['talhao_id']} {r['data']} perda={r['perda_percentual']}% equip={r['equipamento']}")
        else:
            print('Nenhum outlier.')
        return

    else:
        print('Opção inválida.')

def listar_registros():
    registros = load_json(REG_PATH, default=[])
    if not registros:
        print('Sem registros.'); return
    print('\n== Registros (primeiros 20) ==')
    for r in registros[:20]:
        print(f"{r['talhao_id']} | {r['data']} | equip={r['equipamento']} | pre={r['massa_pre']} | pos={r['massa_pos']} | perda={r['perda_percentual']}% | tec={r['tecnologia']}")
    if len(registros) > 20:
        print(f"... (+{len(registros)-20} registros)")

def atualizar_registro():
    registros = load_json(REG_PATH, default=[])
    if not registros:
        print('Sem registros para atualizar.'); return

    print('\n== Atualizar Registro ==')
    talhao = ensure_str('Informe o Talhão do registro a atualizar: ')
    data = ensure_str('Informe a Data (YYYY-MM-DD) do registro a atualizar: ')

    idx = find_index_by_key(registros, talhao, data)
    if idx < 0:
        print('Registro não encontrado.'); return

    atual = registros[idx]
    print('Registro atual:')
    print(f"{atual['talhao_id']} | {atual['data']} | equip={atual['equipamento']} | pre={atual['massa_pre']} | pos={atual['massa_pos']} | perda={atual['perda_percentual']}% | tec={atual['tecnologia']}")

    # campos editáveis (opcional manter o atual digitando Enter)
    novo_equip = input(f"Equipamento [{atual['equipamento']}]: ").strip() or atual['equipamento']
    while True:
        s_pre = input(f"Massa pré-colheita (kg/ha) [{atual['massa_pre']}]: ").strip()
        s_pos = input(f"Massa pós-colheita (kg/ha)  [{atual['massa_pos']}]: ").strip()
        pre = float(s_pre.replace(',','.')) if s_pre else float(atual['massa_pre'])
        pos = float(s_pos.replace(',','.')) if s_pos else float(atual['massa_pos'])
        if pre <= 0:
            print('A massa pré-colheita deve ser maior que zero.'); continue
        if pos > pre:
            print('A massa pós não pode ser maior que a massa pré.'); continue
        break
    tec = input(f"Tecnologia (baixa/média/alta) [{atual['tecnologia']}]: ").strip().lower() or atual['tecnologia']
    while tec not in ['baixa','média','alta']:
        tec = input('Valor inválido. Informe baixa/média/alta: ').strip().lower()

    perda = calc_perda_percentual(pre, pos)
    # atualiza
    atual.update({
        'equipamento': novo_equip,
        'massa_pre': pre,
        'massa_pos': pos,
        'perda_percentual': perda,
        'tecnologia': tec
    })
    registros[idx] = atual
    save_json(REG_PATH, registros)
    append_log(LOG_PATH, f"{datetime.datetime.now().isoformat()} | update {talhao} perda={perda}% (local)")
    print('Registro atualizado com sucesso.')

def menu():
    while True:
        print('\nCanaSmart — Modo Local (JSON) — v2')
        print('[1] Cadastrar registro')
        print('[2] Ver KPIs de perda')
        print('[3] Detectar outliers (Z-score/IQR)')
        print('[4] Atualizar registro existente')
        print('[5] Listar registros')
        print('[6] Sair')
        op = input('Escolha: ').strip()
        if op=='1': cadastrar_registro()
        elif op=='2': listar_kpis()
        elif op=='3': detectar_outliers_menu()
        elif op=='4': atualizar_registro()
        elif op=='5': listar_registros()
        elif op=='6': break
        else: print('Opção inválida.')

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(REG_PATH):
        save_json(REG_PATH, [])
    menu()
