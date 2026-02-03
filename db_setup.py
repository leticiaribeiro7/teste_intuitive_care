
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()




def create_database():
    """Cria o banco de dados se não existir."""
    db_name = os.getenv('DB_NAME')
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
        if result.fetchone() is None:  # Ajuste aqui
            print(f"Criando o banco de dados '{db_name}'...")
            conn.execute(text(f"CREATE DATABASE {db_name}"))
        else:
            print("Banco de dados já existe.")

def setup_database():
    """Limpa o banco e recria as tabelas respeitando as dependências."""
    print("Fazendo setup do banco de dados...")

    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS despesas_agregadas CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS despesas_consolidadas CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS operadoras CASCADE;"))
        conn.commit()

    Base.metadata.create_all(engine)