import pandas as pd
from Vendedor import Vendedor, GerenciarVendedor


manager = GerenciarVendedor()

def criar_atualizar_em_lotes():

    df = pd.read_excel("planilha_vendedores.xlsx")
    vendedores = []
    for indice, linha in df.iterrows():
        print("Nome:", linha['Nome'])
        print("CPF:", linha['CPF'])
        print("Data de Nascimento:", linha['Data de Nascimento'])
        print("Email:", linha['Email'])
        print("Estado:", linha['Estado'])
        print()

    for index, row in df.iterrows():
        vendedor = Vendedor(row['Nome'], row['CPF'], row['Data de Nascimento'], row['Email'], row['Estado'])
        existing_vendedor = manager.read_vendedor(vendedor.cpf)
        vendedores.append(vendedor)
        if existing_vendedor:
            manager.update_vendedor(vendedor)
        else:
            manager.create_vendedor(vendedor)

    return vendedores

