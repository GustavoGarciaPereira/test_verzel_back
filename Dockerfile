# Use uma imagem oficial do Python como imagem de base
FROM python:3.10

# Defina o diretório de trabalho dentro do container
WORKDIR /code

# Copie o 'requirements.txt' para o diretório de trabalho atual
COPY ./requirements.txt /code/requirements.txt

# Instale as dependências do Python
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copie o conteúdo do diretório local para o diretório de trabalho no container
COPY ./app /code/app
EXPOSE 80
# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
