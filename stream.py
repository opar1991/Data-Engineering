from kafka import KafkaAdminClient

try:
    admin = KafkaAdminClient(
        bootstrap_servers="localhost:9092",
        request_timeout_ms=5000
    )

    print("Connected to Apache Kafka!")
    print("Topics:", admin.list_topics())

    admin.close()

except Exception as e:
    print("Kafka connection failed:", e)