import pandas as pd
import os
from db_setup import engine

def import_operadoras():
    """Importa o cadastro da ANS tratando os nomes de colunas e datas."""
    file = 'Relatorio_cadop.csv'
    if os.path.exists(file):
        print(f"Importando {file}...")
        df = pd.read_csv(file, sep=';', encoding='utf-8', dtype={'CNPJ': str}) # cnpj convertido pra str

        
        # Mapeamento do arquivo oficial para o seu Model
        mapping = {
            'REGISTRO_OPERADORA': 'registro_ans',
            'CNPJ': 'cnpj',
            'Razao_Social': 'razao_social',
            'Nome_Fantasia': 'nome_fantasia',
            'Modalidade': 'modalidade',
            'Logradouro': 'logradouro',
            'Numero': 'numero',
            'Complemento': 'complemento',
            'Bairro': 'bairro',
            'Cidade': 'cidade',
            'UF': 'uf',
            'CEP': 'cep',
            'DDD': 'ddd',
            'Telefone': 'telefone',
            'Fax': 'fax',
            'Endereco_eletronico': 'email',
            'Representante': 'representante',
            'Cargo_Representante': 'cargo_representante',
            'Regiao_de_Comercializacao': 'regiao_comercializacao',
            'Data_Registro_ANS': 'data_registro_ans'
        }
        df = df.rename(columns=mapping)
        df['data_registro_ans'] = pd.to_datetime(df['data_registro_ans'], errors='coerce')
        df = df.drop_duplicates(subset=['registro_ans'])

        df.columns = df.columns.str.lower()
        
        df.to_sql('operadoras', engine, if_exists='append', index=False)
        print(f"{len(df)} registros inseridos em 'operadoras'.")
    else:
        print(f"Arquivo {file} não encontrado.")

def import_despesas_consolidadas():
    """Importa o arquivo de despesas brutas."""
    file = 'consolidado_despesas.csv'
    if os.path.exists(file):
        print(f"Importando {file}...")
        df = pd.read_csv(file, sep=';', encoding='utf-8', dtype={'CNPJ': str})

        mapping = {
            'CNPJ': 'cnpj',
            'RazaoSocial': 'razao_social',
            'Ano': 'ano',
            'Trimestre': 'trimestre',
            'ValorDespesas': 'valor_despesas'
        }
        
        df = df.rename(columns=mapping)

        df.to_sql('despesas_consolidadas', engine, if_exists='append', index=False)
        print(f"{len(df)} registros inseridos em 'despesas_consolidadas'.")
    else:
        print(f"Arquivo {file} não encontrado.")

def import_despesas_agregadas():

    file = 'despesas_agregadas.csv'
    if os.path.exists(file):
        print(f"Importando {file}...")
        df = pd.read_csv(file, sep=';', encoding='utf-8', dtype={'CNPJ': str})

        mapping = {
            'UF': 'uf',
            'Modalidade': 'modalidade',
            'RazaoSocial': 'razao_social',
            'RegistroANS': 'registro_ans',
            'Total_Despesas': 'total_despesas',
            'Media_Trimestral': 'media_trimestral',
            'Desvio_Padrao': 'desvio_padrao'
        }
        
        df = df.rename(columns=mapping)

        
        df.to_sql('despesas_agregadas', engine, if_exists='append', index=False)
        print(f"{len(df)} registros inseridos em 'despesas_agregadas'.")
    else:
        print(f"Arquivo {file} não encontrado.")