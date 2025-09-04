# Kafka + Airflow Streaming Pipeline

## Pré-requisitos

- Docker
- Docker Compose

## Guia de Instalação

### 1. Clone o repositório
```bash
git clone <repository-url>
cd kafka_airflow
```

### 2. Execute o pipeline
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

Este projeto implementa um pipeline de streaming em tempo real usando Kafka como message broker e Airflow para orquestração.

### Componentes:

1. **Apache Kafka**: Message broker para streaming de dados
2. **Zookeeper**: Coordenação do cluster Kafka
3. **Kafka UI**: Interface web para monitoramento do Kafka
4. **Apache Airflow**: Orquestração dos pipelines
5. **PostgreSQL**: Banco de dados do Airflow e armazenamento dos dados

### Fluxo de Dados:

```
JSONPlaceholder API → Kafka Producer → Kafka Topic (3 partições) → Kafka Consumer → PostgreSQL
```

### Configuração Kafka:
- **Tópico:** `streaming_data`
- **Partições:** 3 (para distribuição de carga)
- **Replication Factor:** 1

### Tabela de Dados:
- **Nome:** `tb_streaming_raw`
- **Banco:** `customer_streaming`

## Como Usar

### 1. Iniciar o ambiente
Execute o script de inicialização que:
- Sobe todos os containers Docker
- Cria o banco `customer_streaming`
- Cria o tópico Kafka com 3 partições

```bash
./start_pipeline.sh
```

### 2. Executar streaming contínuo
No Airflow (http://localhost:8081), a DAG `continuous_streaming_consumer` executa automaticamente a cada 3 minutos:
- **Producer**: Busca dados da API JSONPlaceholder e envia para Kafka
- **Consumer**: Consome mensagens do Kafka e armazena no PostgreSQL
- **Duração**: 3 minutos por execução (aproximadamente 18 posts)

### 3. Monitorar o pipeline
- **Airflow**: http://localhost:8081 - Monitorar execução das DAGs
- **Kafka UI**: http://localhost:8090 - Visualizar tópicos e mensagens

## Portas de Acesso

- **Airflow**: http://localhost:8081
- **Kafka UI**: http://localhost:8090
- **PostgreSQL (Airflow)**: localhost:5432
- **PostgreSQL (Data)**: localhost:5433
- **Kafka**: localhost:9092
- **Zookeeper**: localhost:2181

## Estrutura dos Dados

```json
{
  "userId": 1,
  "id": 1,
  "title": "Post title",
  "body": "Post content",
  "timestamp": "2024-09-04T02:57:02",
  "source": "jsonplaceholder_api"
}
```

## Configurações

As configurações do pipeline estão em `dags/parameters_continuous_streaming.yaml`:
- **Frequência**: A cada 3 minutos
- **Delay entre posts**: 10 segundos
- **Timeout do consumer**: 15 segundos
- **Duração por execução**: 180 segundos

## Limpeza (Importante)

⚠️ **Os containers ocupam espaço em disco. Execute a limpeza após o uso:**

```bash
./clean_docker_full.sh
```

## Tecnologias Utilizadas

- **Apache Kafka**: Message broker para streaming
- **Apache Airflow**: Orquestração de pipelines
- **PostgreSQL**: Armazenamento de dados
- **Docker**: Containerização
- **Python**: Kafka Producer/Consumer
