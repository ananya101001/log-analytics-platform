import json
from kafka import KafkaProducer
import time
import random

# --- Kafka Configuration ---
KAFKA_BROKER_URL = '35.223.146.238:29092'
TOPIC_NAME = "logs"



if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    log_levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
    
    print("Sending 250 log messages to Kafka...")
    for i in range(250):
        test_log = {
            "timestamp": time.time(),
            "log_level": random.choice(log_levels),
            "service": "test-producer",
            "message": f"Log message number {i+1}",
            "trace_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "user_id": f"user-{random.randint(1, 10)}"
        }
        producer.send(TOPIC_NAME, value=test_log)
        time.sleep(0.01) # small delay

    producer.flush()
    print("All messages sent successfully. ✅")