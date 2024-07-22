# Database

## Docker Run

Tenha certeza que a porta 27017 não está sendo usada.

Execute o comando abaixo no prompt de comando:

`
docker run -d -h mongo --name mongo -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=secret -p 27017:27017 mongo:latest
`

# Backend

## Docker Build

Abra o prompt de comando e navegue até a pasta onde o arquivo Dockerfile está localizado. Execute o comando abaixo:

`
docker build . -t fastapi:latest
`

## Docker Run

Tenha certeza que a porta 8000 não está sendo usada e que o container para o banco de dados esteja rodando e funcionando normalmente.

Execute o comando abaixo no prompt de comando:

`
docker inspect mongo
`

Use o valor localizado em IPAddress para o próximo comando.
![alt text](image.png)

Como o valor no exemplo é 172.17.0.2, o comando seria:

`
docker run -d -e MONGODB_URL="mongodb://mongoadmin:secret@172.17.0.2:27017/" -e FRONTEND_URL=localhost:3000 --name api -p 8000:8000 fastapi:latest
`

## Extras

Para inserir cursos no banco de dados, abra o navegador e acesse:

`
http://127.0.0.1:8000/docs#/
`

Use a seguinte opção para inserir cursos:

![alt text](image-1.png)

#### Alguns exemplos para mockup de cursos estão listados no arquivo `MOCK_DATA.json`