import os
from video.source_factory import open_video_source
from kafka_client.producer_service import FrameProducerService


if __name__ == "__main__":
    print("[DEBUG] Variáveis de ambiente:")
    for key in ["KAFKA_BROKER", "USE_ONVIF"]:
        print(f"  {key} = {os.environ.get(key)}")

    cap = open_video_source(source_type="auto", onvif_config={
        "ip": "192.168.1.101",
        "user": "admin",
        "password": "senha"
    })

    producer = FrameProducerService("CAM_FLEX", cap, exibir_janela=True)
    producer.start()