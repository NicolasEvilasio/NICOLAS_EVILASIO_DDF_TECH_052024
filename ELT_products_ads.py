import os
import pandas as pd
from sqlalchemy import create_engine
from datasets import load_dataset
from dotenv import load_dotenv


load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env

# Carregando o dataset do Hugging Face
dataset = load_dataset("spacemanidol/product-search-corpus")

# Transformando em um DataFrame pandas
df = dataset['train'].to_pandas()


# Criando a conexão com o bd
def create_db_engine():
    # configure variáveis de ambiente no github actions ou crie um arquivo .env
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    database = os.environ.get('DB_DATABASE')

    engine = create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{database}"
    )
    return engine


# Os dados nas colunas title e text contém um caractere ASCII inválido (\x00) que é incompatível com o PostgreSQL
# Função para remover caracteres inválidos e substituir por uma string vazia
def remove_invalid_chars(text):
    cleaned_text = text.replace("\x00", '')
    return cleaned_text


# Chamando a função para remover caracteres inválidos
df['title'] = df['title'].apply(remove_invalid_chars)
df['text'] = df['text'].apply(remove_invalid_chars)

# Inserido os dados na tabela do banco de dados
df.to_sql('products_ads', con=create_db_engine(), if_exists='replace', index=False)

# Consultando os dados da tabela
result = pd.read_sql("""SELECT * FROM products_ads LIMIT 10""", con=create_db_engine())
print(result)
