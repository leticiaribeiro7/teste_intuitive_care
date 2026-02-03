import os
import zipfile
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO
import re

from validations import validated_data
from db_setup import engine, create_database, setup_database
from db_import import import_operadoras, import_despesas_consolidadas, import_despesas_agregadas

# --- CONFIGURAÇÕES ---

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
CADASTRO_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
FINAL_CSV = "consolidado_despesas.csv"



def get_mapeamento_operadoras():
    print("-> Obtendo base cadastral...")
    res = requests.get(CADASTRO_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    csv_link = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.csv')][-1]
    
    df_cad = pd.read_csv(CADASTRO_URL + csv_link, sep=';', engine='python', encoding='utf-8')
    df_cad.columns = [c.strip().upper() for c in df_cad.columns]

    # Identifica colunas dinamicamente
    col_reg = next(c for c in df_cad.columns if 'REGISTRO' in c)
    col_cnpj = next(c for c in df_cad.columns if 'CNPJ' in c)
    col_razao = next(c for c in df_cad.columns if 'RAZAO' in c)
    col_mod = next(c for c in df_cad.columns if 'MODALIDADE' in c)
    col_uf = next(c for c in df_cad.columns if 'UF' in c)

    # Padroniza nomes para o merge funcionar
    df_cad = df_cad[[col_reg, col_cnpj, col_razao, col_mod, col_uf]].copy()
    df_cad.rename(columns={col_reg: 'RegistroANS', col_cnpj: 'CNPJ', col_razao: 'RazaoSocial', col_mod: 'Modalidade', col_uf: 'UF'}, inplace=True)

    df_cad['RegistroANS'] = df_cad['RegistroANS'].astype(str).str.strip()
    df_cad['CNPJ'] = df_cad['CNPJ'].astype(str).str.strip()

    print(df_cad.head())
    return df_cad

def download_files(arquivos_alvo):
    df_lista = []
    padrao = r'despesas\s*com\s*eventos\s*/?\s*sinistros'

    for tri_path in arquivos_alvo:
        print(f"Lendo: {tri_path}")
        try:
            r = requests.get(BASE_URL + tri_path)
            with zipfile.ZipFile(BytesIO(r.content)) as z:
                for file_name in z.namelist():
                    if not file_name.lower().endswith(('.csv', '.txt')): continue
                    
                    with z.open(file_name) as f:
                        df = pd.read_csv(f, sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')
                        
                    df.columns = [str(c).strip().upper() for c in df.columns]
                    
                    col_reg = next((c for c in df.columns if 'REG' in c), None)
                    col_valor_inicial = next((c for c in df.columns if 'SALDO_INICIAL' in c), None)
                    col_valor_final = next((c for c in df.columns if 'SALDO_FINAL' in c), None)
                    

                    if 'DESCRICAO' in df.columns and col_reg and col_valor_inicial and col_valor_final:
                        # Filtro Regex
                        mask = df['DESCRICAO'].astype(str).str.contains(padrao, case=False, regex=True, na=False)
                        df_filtrado = df[mask].copy()
                        

                        df_filtrado[col_reg] = df_filtrado[col_reg].astype(str).str.strip()
                        df_filtrado.rename(columns={col_reg: 'RegistroANS'}, inplace=True)
                    
                        
                        # Cálculo (Saldo Inicial - Saldo Final geralmente indica despesa)
                        df_filtrado['ValorDespesas'] = pd.to_numeric(df_filtrado[col_valor_final], errors='coerce').fillna(0) - pd.to_numeric(df_filtrado[col_valor_inicial], errors='coerce').fillna(0)

                        df_filtrado = df_filtrado[df_filtrado['ValorDespesas'] != 0].copy()
                        df_filtrado['Ano'] = tri_path.split('/')[0]
                        df_filtrado['Trimestre'] = tri_path.split('/')[-1].replace('.zip', '')[0]

                        df_lista.append(df_filtrado)
        except Exception as e:
            print(f"Erro ao processar {tri_path}: {e}")

    return df_lista 


def identify_trimestre():
    print("-> Identificando trimestres...")
    res = requests.get(BASE_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    # Pega pastas de anos
    anos = sorted([a['href'] for a in soup.find_all('a', href=True) if re.match(r'^\d{4}/', a['href'])], reverse=True)

    arquivos_alvo = []
    for ano in anos:
        res_ano = requests.get(BASE_URL + ano)
        soup_ano = BeautifulSoup(res_ano.text, 'html.parser')
        zips = sorted([ano + a['href'] for a in soup_ano.find_all('a', href=True) if a['href'].endswith('.zip')], reverse=True)
        
        for z in zips:
            if len(arquivos_alvo) < 3:
                arquivos_alvo.append(z)
    return arquivos_alvo


def get_demonstracoes_contabeis():
    mapa = get_mapeamento_operadoras()
    arquivos_alvo = identify_trimestre()
    print(f"Arquivos selecionados: {arquivos_alvo}")
    
    df_lista = download_files(arquivos_alvo)

    if df_lista:
        df_final = pd.concat(df_lista, ignore_index=True)
        df_final = df_final.merge(mapa, on='RegistroANS', how='left') #join pelo registro_ans ja que nao tem cnpj

        df_final = df_final.groupby(['CNPJ', 'RazaoSocial', 'Ano', 'Trimestre'], as_index=False)['ValorDespesas'].sum()
        
        
        df_final.to_csv(FINAL_CSV, index=False, sep=';', encoding='utf-8')
        print(f"\n--- SUCESSO ---\nArquivo {FINAL_CSV} gerado.")
    else:
        print("\nErro: Nenhum dado processado.")





def add_new_columns():
    df_despesas = pd.read_csv(FINAL_CSV, sep=';', engine='python', encoding='utf-8')
    df_validado = validated_data(df_despesas)
    
    operadoras = get_mapeamento_operadoras()

    df_validado['CNPJ'] = df_validado['CNPJ'].astype(str).str.strip()

    # colunas que quero do df de operadoras
    colunas_interesse = ['CNPJ', 'RegistroANS', 'Modalidade', 'UF'] 
    operadoras_filtrado = operadoras[colunas_interesse]

    df_validado = df_validado.merge(operadoras_filtrado, on='CNPJ', how='left')

    # outras colunas inclusas no group by para que todas apareçam no csv final
    # faz o calculo de total por operadora/UF, calcula a media de cada trimestre e desvio padrao
    df_validado = df_validado.groupby(['RegistroANS',  'RazaoSocial', 'Modalidade', 'UF'], as_index=False)['ValorDespesas'].agg(
        Total_Despesas='sum',
        Media_Trimestral='mean',
        Desvio_Padrao='std'
    )
    
    df_validado = df_validado.sort_values(by='Total_Despesas', ascending=False)

    df_validado.to_csv("despesas_agregadas.csv", index=False, sep=';', encoding='utf-8')
    print(f"\n--- SUCESSO ---\nArquivo despesas_agregadas.csv gerado.")






if __name__ == "__main__":
    get_demonstracoes_contabeis()
    add_new_columns()
    create_database()
    setup_database()
    import_operadoras()
    import_despesas_consolidadas()
    import_despesas_agregadas()