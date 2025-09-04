# Streaming Projects

## Pré-requisitos

- Docker
- Docker Compose

## Guia de Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/KlausRezende/streaming.git
```

### 2. Navegue para o diretório
```bash
cd streaming
```

### 3. Execute o pipeline
```bash
./start_pipeline.sh
```

## Credenciais de Acesso

### Airflow
- **Usuário:** admin
- **Senha:** admin

### Kafka UI
- **URL:** http://localhost:8090
- **Sem autenticação necessária**

## Arquitetura de Streaming

Este projeto implementa uma arquitetura simplificada de streaming com Apache Kafka como fonte de dados e processamento apenas na camada Bronze.

### Componentes:

1. **Apache Kafka**: Message broker para streaming de dados
2. **Zookeeper**: Coordenação do cluster Kafka
3. **Kafka UI**: Interface web para monitoramento do Kafka
4. **Apache Airflow**: Orquestração dos pipelines
5. **Apache Spark**: Processamento dos dados do Kafka
6. **PostgreSQL**: Armazenamento dos dados (customer_streaming)

### Fluxo de Dados:

```
JSONPlaceholder API → Kafka Producer → Kafka Topic → Spark Streaming → PostgreSQL
```

### Tópico Kafka:
- `streaming_data`: Dados de posts da API JSONPlaceholder

### Tabela Bronze:
- `tb_bz_streaming_data`: Dados brutos de posts do Kafka

## Como Usar

### 1. Executar setup inicial
No Airflow (http://localhost:8081), execute a DAG `streaming_complete_pipeline` que:
- Cria o tópico Kafka
- Inicia o producer da API
- Inicia o consumer

### 2. Executar streaming contínuo
Execute a DAG `streaming_pipeline` manualmente - ela rodará infinitamente processando dados em tempo real.

### 3. Monitorar Kafka
Acesse http://localhost:8090 para visualizar os tópicos e mensagens no Kafka UI.

## Portas de Acesso

- **Airflow**: http://localhost:8081
- **Kafka UI**: http://localhost:8090
- **PostgreSQL**: localhost:5433
- **Kafka**: localhost:9092
- **Zookeeper**: localhost:2181

## Estrutura dos Dados

```json
{
  "userId": 1,
  "id": 1,
  "title": "Post title",
  "body": "Post content",
  "timestamp": "2024-01-01T10:00:00",
  "source": "jsonplaceholder_api"
}
```

## Limpeza (Importante)

⚠️ **Os containers ocupam espaço em disco. Execute a limpeza após o uso:**

```bash
./clean_docker_full.sh
```

## Tecnologias Utilizadas

- **Apache Kafka**: Streaming de dados
- **Apache Spark**: Processamento de dados
- **Apache Airflow**: Orquestração
- **PostgreSQL**: Armazenamento
- **Docker**: Containerização
