# 📊 Consolidação de Despesas de Operadoras de Saúde (ANS)

Este projeto realiza o **download, processamento, validação e consolidação** das demonstrações contábeis das operadoras de planos de saúde disponibilizadas pela ANS, enriquecendo os dados com informações cadastrais oficiais das operadoras.



## Execução do projeto

### -> Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuração do .env (exemplo)
```bash
# Necessario ter o postgresql instalado e executando

DB_USER=postgres
DB_PASS=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=teste_intuitive_care
```

Caso o banco de dados e tabelas não existam, são criados ao executar o script:

```bash
python main.py
python api.py
```

### -> Frontend
```bash
cd operadoras-frontend
npm run dev
```


### Saídas geradas

* `consolidado_despesas.csv`
* `despesas_agregadas.zip`
* Importação dos dados em csv para o banco de dados PostgreSQL.
* Acesso ao front-end em localhost:5173 e api no backend em localhost:8000



## Arquitetura e fluxo do processamento

### 1. Base cadastral das operadoras

* Download automático do CSV de **Operadoras Ativas** da ANS
* Padronização de colunas
* Utilização do **Registro ANS** como chave primária

### 2. Demonstrações contábeis

* Download automático dos **3 últimos trimestres disponíveis** identificados através da ferramenta **BeautifulSoup**, que lê e processa o html da página. Cada arquivo é processado diretamente na memória devido ao tamanho ser ~60MB.

* Leitura de arquivos nos formatos:

  * CSV
  * TXT
  * XLS / XLSX
* Padronização dos nomes de colunas
* Filtro por:

  * *Despesas com eventos / sinistros*

Toda manipulação e processamento dos dados foi feita usando a biblioteca Pandas devido à sua facilidade no tratamento de dados estruturados como excel e CSV.


## Decisões técnicas e trade-offs

### Uso do Registro ANS como chave

As demonstrações contábeis **não possuem CNPJ**. Para adicionar o CNPJ no consolidado de despesas como solicitado, foi feito o "join" usando o arquivo de cadastro das operadoras usando o Registro ANS como chave. Para executar o "join" foi utilizada a função **merge** do Pandas.



### Integridade dos dados e não exclusão de registros

* **CNPJs inválidos não são removidos**
* Os dados são preservados integralmente e sinalizados com "Válido" ou "Inválido" através de nova coluna no CSV final.

Motivos:

* Manter integridade histórica
* Possibilitar auditoria
* Permitir correções futuras (ex.: erro de digitação)



### Escolha do FastAPI

* Simples e direto
* Alta performance
* **Documentação automática**

A API gera automaticamente documentação interativa via Swagger/OpenAPI:

```
/docs
```

Nenhuma configuração extra é necessária.

---

### Paginação


Em listas de operadoras, é comum que o usuário queira:

* Ir direto para a **página 5**
* Ir para a **última página**

Offset pagination permite isso nativamente.


### Cache de estatísticas

* Estatísticas agregadas utilizam cache de 1 hora, devido aos dados da ANS não mudarem com tanta frequência

---

## Modelagem e remoção de redundâncias

* Redundâncias foram removidas das tabelas derivadas
* Cadastro de operadoras: Mantido igual ao original da ANS
* O consolidado e despesas agregadas contém apenas os campos solicitados ou necessários para análise.

---

## Tecnologias utilizadas

* Python
* Pandas
* Requests
* BeautifulSoup
* FastAPI
* Uvicorn
* Vue
* SQL Alchemy

---