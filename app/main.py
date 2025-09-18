# app/main.py
import os
import json
import clickhouse_connect
from datetime import datetime
from kafka import KafkaConsumer
import time
import threading
from flask import Flask, render_template

# --- Flask App for Dashboard and Health Checks ---
app = Flask(__name__)

# --- Configuration ---
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME", "logs")
CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = int(os.environ.get("CLICKHOUSE_PORT", 8123))
CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER", "admin")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD", "password")
db_client = None

def get_clickhouse_client(retries=5, delay=5):
    """Initializes and returns a ClickHouse client with retry logic."""
    global db_client
    if db_client:
        try:
            db_client.command("SELECT 1")
            return db_client
        except Exception:
            db_client = None # Stale connection, force reconnect
    
    for i in range(retries):
        try:
            client = clickhouse_connect.get_client(
                host=CLICKHOUSE_HOST,
                port=CLICKHOUSE_PORT,
                username=CLICKHOUSE_USER,
                password=CLICKHOUSE_PASSWORD,
                connect_timeout=10
            )
            client.command("SELECT 1")
            db_client = client
            return db_client
        except Exception as e:
            print(f"ClickHouse connection failed: {e}")
            if i < retries - 1:
                time.sleep(delay)
            else:
                return None

@app.route('/')
def dashboard():
    """Renders the main dashboard page."""
    logs = []
    client = get_clickhouse_client()
    if client:
        try:
            result = client.query(
                'SELECT timestamp, log_level, service, message FROM logs ORDER BY timestamp DESC LIMIT 50'
            )
            logs = result.result_rows
        except Exception as e:
            print(f"Error querying ClickHouse: {e}")
    # The render_template function looks for the file in the 'templates' folder
    return render_template('index.html', logs=logs)

@app.route('/healthz')
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

def run_web_server():
    """Runs the Flask web server."""
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# (The Kafka consumer and ClickHouse insert logic remains the same)
def consume_messages():
    """Consumes messages from Kafka and inserts them into ClickHouse in batches."""
    consumer = None
    for i in range(5):
        try:
            consumer = KafkaConsumer(
                TOPIC_NAME,
                bootstrap_servers=KAFKA_BROKER_URL,
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                consumer_timeout_ms=10000
            )
            break
        except Exception as e:
            print(f"Kafka connection failed: {e}, retrying in 5s...")
            time.sleep(5)
    
    if not consumer:
        print("Could not connect to Kafka after multiple retries. Exiting consumer thread.")
        return

    client = get_clickhouse_client()
    if not client:
        print("Could not connect to ClickHouse. Exiting consumer thread.")
        return

    batch = []; batch_size = 100; last_insert_time = time.time()
    print(f"Consumer is now listening for messages on topic '{TOPIC_NAME}'...")
    for message in consumer:
        if message:
            log_entry = message.value
            batch.append(log_entry)
        
        current_time = time.time()
        if len(batch) >= batch_size or (batch and current_time - last_insert_time > 5):
            insert_batch_to_clickhouse(client, batch)
            batch = []; last_insert_time = time.time()

def insert_batch_to_clickhouse(client, batch):
    if not batch: return
    try:
        columns = ['timestamp', 'log_level', 'service', 'message', 'trace_id', 'user_id']
        data_to_insert = []
        for log_data in batch:
            log_data['timestamp'] = datetime.fromtimestamp(log_data['timestamp'])
            row = [log_data.get(col) for col in columns]
            data_to_insert.append(row)
        client.insert('logs', data_to_insert, column_names=columns)
        print(f"Inserted batch of {len(batch)} logs into ClickHouse.")
    except Exception as e:
        print(f"Error inserting into ClickHouse: {e}")
        # Attempt to reconnect on next insert
        global db_client
        db_client = None

if __name__ == "__main__":
    # The Kafka consumer runs in a background thread
    consumer_thread = threading.Thread(target=consume_messages, daemon=True)
    consumer_thread.start()
    
    # The main thread runs the Flask web server
    run_web_server()