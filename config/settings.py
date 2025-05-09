import os

print("[DEBUG] ENV:", dict(os.environ))

def rodando_em_container():
    return os.path.exists("/.dockerenv")

# Define o broker com base na variável de ambiente ou no ambiente de execução
KAFKA_BROKER = os.environ.get("KAFKA_BROKER")
if not KAFKA_BROKER:
    KAFKA_BROKER = "kafka:29092" if rodando_em_container() else "localhost:9092"

print(f"[DEBUG] Usando broker: {KAFKA_BROKER}")

# Permite sobrescrever o tópico via variável de ambiente, com fallback padrão
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "topic.frame.original")
FPS = int(os.environ.get("FPS", "10"))