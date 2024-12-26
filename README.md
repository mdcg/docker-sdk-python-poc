# docker-sdk-python-poc

Este projeto é uma Prova de Conceito (PoC) para testar a integração com a API Docker usando o SDK oficial do Docker para Python. Ele permite inicializar, listar e parar containers Docker diretamente via código Python.

## Pré-requisitos

Certifique-se de que os seguintes itens estão instalados no ambiente:

- **Python 3.7+**
- **Docker** instalado e em execução

## Instalação

1. Clone este repositório:
   ```bash
   git clone git@github.com:mdcg/docker-sdk-python-poc.git
   ```

2. Crie e inicializa uma virtualenv:

   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

## Funcionalidades

O código implementa as seguintes funcionalidades básicas:

1. **Inicializar um container:**
   - Com base em uma imagem local, inicializa um container.

2. **Listar containers:**
   - Lista todos os containers ativos e parados.

3. **Parar um container:**
   - Para um container ativo especificado pelo ID.

## Inicializando

Para facilitar a execução da POC, builde e inicialize os containers especificados no arquivo docker-compose.yml:

```
docker compose up
```

Com o comando acima serão executados: API do SDK do Docker, InfluxDB, RabbitMQ, Publisher e um Subscriber.

# Documentação da API

Esta API fornece uma interface para interagir com containers e imagens Docker usando Flask e o SDK Docker para Python. Abaixo estão detalhadas as rotas disponíveis na API.

## Rotas Disponíveis

### 1. **Listar Imagens**
- **Endpoint:** `/images`
- **Método:** `GET`
- **Descrição:** Retorna uma lista de imagens disponíveis no Docker.
- **Resposta:**
  - Status 200: Uma lista de imagens com os seguintes campos:
    - `id`: ID curto da imagem
    - `tags`: Tags associadas à imagem

#### Exemplo de Resposta:
```json
[
  {
    "id": "abc123",
    "tags": "influx:latest"
  },
  {
    "id": "def456",
    "tags": "rabbitmq:latest"
  }
]
```

### 2. **Listar Containers**
- **Endpoint:** `/containers`
- **Método:** `GET`
- **Descrição:** Retorna uma lista de containers ativos e inativos no Docker.
- **Resposta:**
  - Status 200: Uma lista de containers com os seguintes campos:
    - `id`: ID curto do container
    - `name`: Nome do container
    - `status`: Status atual do container

#### Exemplo de Resposta:
```json
[
  {
    "id": "xyz789",
    "name": "my_container",
    "status": "running"
  },
  {
    "id": "uvw123",
    "name": "test_container",
    "status": "exited"
  }
]
```

### 3. **Iniciar um Container**
- **Endpoint:** `/containers/run`
- **Método:** `POST`
- **Descrição:** Inicia um container específico.
- **Payload:**
  - `id` (obrigatório): ID do container a ser iniciado.
- **Resposta:**
  - Status 200: Confirmação de que o container foi iniciado.
  - Status 400: Falta o campo `id` no payload.
  - Status 404: Container com o ID especificado não foi encontrado.

#### Exemplo de Requisição:
```json
{
  "id": "xyz789"
}
```

#### Exemplo de Resposta:
```json
{
  "message": "Container started"
}
```

### 4. **Parar um Container**
- **Endpoint:** `/containers/stop`
- **Método:** `POST`
- **Descrição:** Para um container específico.
- **Payload:**
  - `id` (obrigatório): ID do container a ser parado.
- **Resposta:**
  - Status 200: Confirmação de que o container foi parado.
  - Status 400: Falta o campo `id` no payload.
  - Status 404: Container com o ID especificado não foi encontrado.

#### Exemplo de Requisição:
```json
{
  "id": "xyz789"
}
```

#### Exemplo de Resposta:
```json
{
  "message": "Container stopped"
}
```

## Observações
- Certifique-se de que o Docker está configurado e em execução no ambiente onde a API será utilizada.
- Os endpoints que utilizam o método `POST` requerem um payload no formato JSON.

## Considerações finais

Qualquer dúvida ou sugestão sinta-se a vontade para abrir uma issue. Além disso, sinta-se livre para fazer o que quiser com esse repositório! ;-)
