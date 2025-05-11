import base64
import cv2
import time
import uuid
import logging
from datetime import datetime, timezone
from confluent_kafka import Producer
from models.frame_message import FrameMessage
from config.settings import KAFKA_BROKER, KAFKA_TOPIC, FPS

logger = logging.getLogger(__name__)

class FrameProducerService:

    def __init__(self, camera_id, video_capture, exibir_janela=False, source_type="webcam", encoding="jpeg"):
        self.camera_id = camera_id
        self.cap = video_capture
        self.exibir_janela = exibir_janela
        self.source_type = source_type
        self.encoding = encoding
        self.producer = Producer({'bootstrap.servers': KAFKA_BROKER})

    def delivery_report(self, err, msg):
        if err:
            logger.error(f"Kafka: {err}")
        else:
            logger.info(f"Frame entregue: tópico {msg.topic()} - partição {msg.partition()}")

    def start(self):
        if not self.cap.isOpened():
            logger.error("Fonte de vídeo indisponível.")
            return

        logger.info(f"Streaming iniciado de '{self.camera_id}' → tópico '{KAFKA_TOPIC}'...")

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    logger.error("Falha na leitura do frame.")
                    break

                _, buffer = cv2.imencode('.jpg', frame)
                frame_b64 = base64.b64encode(buffer).decode('utf-8')

                message = FrameMessage(
                    frame_id=str(uuid.uuid4()),
                    camera_id=self.camera_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    frame_base64=frame_b64,
                    source_type=self.source_type,
                    encoding=self.encoding
                )

                self.producer.produce(
                    KAFKA_TOPIC,
                    value=message.to_json(),
                    callback=self.delivery_report
                )
                self.producer.poll(0)

                if self.exibir_janela:
                    cv2.imshow(f"Camera - {self.camera_id}", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        logger.info("Tecla 'q' pressionada. Encerrando...")
                        break

                time.sleep(1 / FPS)

        except KeyboardInterrupt:
            logger.info("Interrompido pelo usuário.")

        finally:
            self.cap.release()
            self.producer.flush()
            if self.exibir_janela:
                cv2.destroyAllWindows()
            logger.info("Produtor encerrado.")