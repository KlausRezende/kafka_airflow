import json
import requests
import psycopg2
import time
from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime, timedelta
import threading
import yaml

def continuous_producer_consumer():
    # Load parameters from YAML
    with open('/opt/airflow/dags/parameters_continuous_streaming.yaml', 'r') as f:
        params = yaml.safe_load(f)
    
    def producer_loop():
        producer = KafkaProducer(
            bootstrap_servers=[params['streaming']['kafka']['bootstrap_servers']],
            key_serializer=lambda k: str(k).encode('utf-8'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Get all posts once
        response = requests.get(params['streaming']['api']['url'])
        all_posts = response.json()
        post_index = 0
        
        while True:
            try:
                # Cycle through different posts
                post = all_posts[post_index % len(all_posts)].copy()
                
                # UTC-3 (Brasília timezone)
                utc_now = datetime.utcnow()
                brasilia_time = utc_now - timedelta(hours=3)
                post['timestamp'] = brasilia_time.isoformat()
                post['source'] = 'jsonplaceholder_api'
                
                producer.send(
                    params['streaming']['kafka']['topic'], 
                    key=post['userId'],  # Use userId as partition key
                    value=post
                )
                producer.flush()
                print(f"Produced post {post['id']}: {post['title'][:30]}...")
                
                post_index += 1
                time.sleep(params['streaming']['api']['producer_delay_seconds'])
                
            except Exception as e:
                print(f"Producer error: {e}")
                time.sleep(30)
    
    def consumer_loop():
        # Setup PostgreSQL
        conn = psycopg2.connect(
            host=params['streaming']['postgres']['host'],
            database=params['streaming']['postgres']['database'],
            user=params['streaming']['postgres']['user'],
            password=params['streaming']['postgres']['password']
        )
        cursor = conn.cursor()
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {params['streaming']['postgres']['table']} (
                userId INTEGER,
                id INTEGER,
                title TEXT,
                body TEXT,
                timestamp VARCHAR(50),
                source VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        # Setup Kafka consumer
        consumer = KafkaConsumer(
            params['streaming']['kafka']['topic'],
            bootstrap_servers=[params['streaming']['kafka']['bootstrap_servers']],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            consumer_timeout_ms=params['streaming']['kafka']['consumer_timeout_ms'],
            auto_offset_reset='latest'
        )
        
        for message in consumer:
            try:
                data = message.value
                partition = message.partition
                key = message.key.decode('utf-8') if message.key else None
                
                cursor.execute(f"""
                    INSERT INTO {params['streaming']['postgres']['table']} 
                    (userId, id, title, body, timestamp, source) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (data['userId'], data['id'], data['title'], data['body'], data['timestamp'], data['source']))
                
                conn.commit()
                print(f"Consumed from partition {partition}, key {key}: {data['title'][:30]}...")
                
            except Exception as e:
                print(f"Consumer error: {e}")
                conn.rollback()
    
    # Start producer and consumer in parallel
    producer_thread = threading.Thread(target=producer_loop, daemon=True)
    consumer_thread = threading.Thread(target=consumer_loop, daemon=True)
    
    producer_thread.start()
    consumer_thread.start()
    
    # Keep running for configured duration
    time.sleep(params['streaming']['runtime']['continuous_duration_seconds'])
    print("Continuous task completed - will restart automatically")
