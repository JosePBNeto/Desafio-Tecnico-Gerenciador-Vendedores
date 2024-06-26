import pandas as pd
from Vendedor import Vendedor, GerenciarVendedor

manager = GerenciarVendedor()
VALOR_DA_COMISSAO = 0.10
COMISSAO_DE_MARKETING = 0.20
VALOR_VENDAS_PARA_COMISSAO_DESTINADA_GERENTE = 1000
COMISSAO_GERENTE = 0.10


def criar_atualizar_em_lotes(file_path):
    df = pd.read_excel(file_path)
    vendedores = []

    for index, row in df.iterrows():
        vendedor = Vendedor(row['Nome'], row['CPF'], row['Data de Nascimento'], row['Email'], row['Estado'])
        existing_vendedor = manager.read_vendedor(vendedor.cpf)
        vendedores.append(vendedor)
        if existing_vendedor:
            manager.update_vendedor(vendedor)
        else:
            manager.create_vendedor(vendedor)

    return vendedores

def formatar_moeda(value):
    if isinstance(value, str):
        return float(value.replace('R$', '').replace('.', '').replace(',', '.').strip())
    return value

def salvar_dataframe_em_excel(dataframe, file_path, sheet_name, index=False):
    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
        dataframe.to_excel(writer, sheet_name=sheet_name, index=index)

def calcular_comissoes(file_path):
    vendas_df = pd.read_excel(file_path, sheet_name='Vendas')

    vendas_df['Valor da Venda'] = vendas_df['Valor da Venda'].apply(formatar_moeda)
    vendas_df['Custo da Venda'] = vendas_df['Custo da Venda'].apply(formatar_moeda)

    vendas_df['Comissao Final'] = vendas_df['Valor da Venda'] * VALOR_DA_COMISSAO
    vendas_df['Comissao Bruta'] = vendas_df['Valor da Venda'] * VALOR_DA_COMISSAO

    vendas_df['Comissao Marketing'] = vendas_df.apply(
        lambda row: row['Comissao Final'] * COMISSAO_DE_MARKETING if row['Canal de Venda'] == 'Online' else 0, axis=1
    )

    vendas_df.loc[vendas_df['Canal de Venda'] == 'Online', 'Comissao Final'] = vendas_df['Comissao Final'] - vendas_df[
        'Comissao Final'] * COMISSAO_DE_MARKETING

    vendas_df['Comissao Gerente'] = vendas_df.apply(
        lambda row: row['Comissao Final'] * COMISSAO_GERENTE if row[ 'Comissao Final'] >= VALOR_VENDAS_PARA_COMISSAO_DESTINADA_GERENTE else 0, axis=1
    )

    vendas_df.loc[vendas_df['Comissao Final'] >= VALOR_VENDAS_PARA_COMISSAO_DESTINADA_GERENTE, 'Comissao Final'] = \
    vendas_df['Comissao Final'] - vendas_df['Comissao Final'] * COMISSAO_GERENTE


    comissao_total = vendas_df.groupby('Nome do Vendedor')[
        ['Comissao Bruta', 'Comissao Marketing', 'Comissao Gerente', 'Comissao Final']].sum().reset_index()

    salvar_dataframe_em_excel(comissao_total, file_path, 'Comissões Calculadas')

def calcular_volume_e_media_vendas(file_path):
    vendas_df = pd.read_excel(file_path, sheet_name='Vendas')

    vendas_df['Valor da Venda'] = vendas_df['Valor da Venda'].apply(formatar_moeda)

    volume_vendas = vendas_df.groupby(['Nome do Vendedor', 'Canal de Venda']).size().reset_index(name='Volume de Vendas')

    media_vendas = vendas_df.groupby(['Nome do Vendedor', 'Canal de Venda'])['Valor da Venda'].mean().reset_index(name='Média de Vendas')

    media_vendas['Média de Vendas'] = media_vendas['Média de Vendas'].round(2)

    resultado = pd.merge(volume_vendas, media_vendas, on=['Nome do Vendedor', 'Canal de Venda'])

    salvar_dataframe_em_excel(resultado, file_path, 'Volume de Vendas e média')

