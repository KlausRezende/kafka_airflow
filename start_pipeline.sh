#!/bin/bash

echo "🚀 Starting Docker containers..."
docker compose -f docker-compose.yaml up -d

echo "⏳ Waiting for services to be ready..."
sleep 30

echo "🗄️ Creating customer_streaming database..."
docker exec postgres_simple psql -U airflow -d postgres -c "CREATE DATABASE customer_streaming;" 2>/dev/null || echo "Database already exists"

echo "📡 Creating Kafka topic with partitions..."
docker exec kafka kafka-topics --create --topic streaming_data --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1 --if-not-exists

echo "📋 Topic details:"
docker exec kafka kafka-topics --describe --topic streaming_data --bootstrap-server localhost:9092

echo "✅ Pipeline setup complete!"
echo "📊 Access Airflow at: http://localhost:8081 (admin/admin)"
echo "🔍 Access Kafka UI at: http://localhost:8090"
echo "🗄️ PostgreSQL available at: localhost:5433"
