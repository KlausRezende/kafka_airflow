#!/usr/bin/env python3
import psycopg2
import sys

def clean_streaming_table():
    connection_configs = [
        {"host": "localhost", "port": 5433, "database": "customer_streaming"},
        {"host": "postgres_simple", "port": 5432, "database": "customer_streaming"}
    ]
    
    conn = None
    for config in connection_configs:
        try:
            conn = psycopg2.connect(
                host=config["host"],
                port=config["port"],
                database=config["database"],
                user="airflow",
                password="airflow"
            )
            print(f"✅ Connected to {config['host']}:{config['port']}")
            break
        except Exception as e:
            print(f"❌ Failed to connect to {config['host']}:{config['port']} - {e}")
            continue
    
    if not conn:
        print("❌ Could not connect to database. Make sure Docker containers are running.")
        sys.exit(1)
    
    cursor = conn.cursor()
    
    # Check current count
    cursor.execute("SELECT COUNT(*) FROM tb_streaming_raw;")
    count_before = cursor.fetchone()[0]
    print(f"📊 Records before cleanup: {count_before}")
    
    # Clean the table
    try:
        cursor.execute("TRUNCATE TABLE tb_streaming_raw CASCADE;")
        print("✅ Cleaned table: tb_streaming_raw")
    except Exception as e:
        print(f"❌ Error cleaning tb_streaming_raw: {e}")
        conn.close()
        sys.exit(1)
    
    # Verify cleanup
    cursor.execute("SELECT COUNT(*) FROM tb_streaming_raw;")
    count_after = cursor.fetchone()[0]
    print(f"📊 Records after cleanup: {count_after}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("🧹 Streaming table cleaned successfully!")

if __name__ == "__main__":
    clean_streaming_table()
