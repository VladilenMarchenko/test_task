import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from api.vectors.service import VectorService
from core.config import settings


async def consume():
    consumer = AIOKafkaConsumer(
        'embedder',
        bootstrap_servers=settings.kafka.endpoint,
        group_id="my-group")

    print("Consumer started")
    await consumer.start()

    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.timestamp)
            try:
                payload = json.loads(msg.value.decode("utf-8"))

                file_url = payload.get("file_url")
                filename = payload.get("filename")

                if not file_url or not filename:
                    print("Empty file_url or filename in Kafka message")
                    continue

                vectored_file = await VectorService.vectorize_from_url(file_url=file_url)

                saved = await VectorService.save_vector_to_elasticsearch(
                    original_filename=filename,
                    file_url=file_url,
                    vector=vectored_file.vector
                )
                print(f"Vector saved to ES with id: {saved}")

            except Exception as e:
                print("Error processing message:", e)


    finally:
        await consumer.stop()


async def send_one(file_url: str, filename: str):
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka.endpoint)

    await producer.start()
    try:
        payload = {
            "file_url": file_url,
            "filename": filename
        }
        message_bytes = json.dumps(payload).encode("utf-8")
        await producer.send_and_wait("embedder", message_bytes)
    finally:
        await producer.stop()



