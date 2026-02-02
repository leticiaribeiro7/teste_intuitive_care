import re
from turtle import pd
import requests

from main import get_cadastro_operadoras


CONSOLIDATED_CSV = "consolidado_despesas.csv"



def validar_cnpj(cnpj: str) -> bool:
    if not cnpj:
        return False

    # remove tudo que não for número
    cnpj = re.sub(r'\D', '', str(cnpj))

    # deve ter 14 dígitos
    if len(cnpj) != 14:
        return False

    # elimina sequências inválidas
    if cnpj == cnpj[0] * 14:
        return False

    def calc_digito(cnpj, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos_1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos_2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]

    dig1 = calc_digito(cnpj[:12], pesos_1)
    dig2 = calc_digito(cnpj[:12] + dig1, pesos_2)

    return cnpj[-2:] == dig1 + dig2



def validated_data():
    
    df = pd.read_csv(
        CONSOLIDATED_CSV,
        sep=';',
        encoding='utf-8'
    )
     # filtro de cnpj valido
    df['StatusCNPJ'] = df['CNPJ'].apply(validar_cnpj).map({True: 'Válido', False: 'Inválido'})
    df = df[df['ValorDespesas'] > 0].copy() # mantêm só os valores positivos
    df = df[df['RazaoSocial'].notna() & df['RazaoSocial'].str.strip().ne('')].copy() # mantêm só os que tem razão social


    return df



