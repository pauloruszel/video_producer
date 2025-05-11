import cv2
import os
import logging
from .onvif_utils import get_rtsp_from_onvif

logger = logging.getLogger(__name__)

def open_video_source(source_type="auto", source_path=None, onvif_config=None):
    """
    Abre a fonte de vídeo com base na configuração:
    - "webcam": usa a câmera local
    - "video": usa um arquivo de vídeo local
    - "onvif": força ONVIF
    - "auto": tenta ONVIF se ativado, senão webcam
    """
    if source_type == "video":
        logger.info(f"[Fonte] Usando vídeo local: {source_path}")
        return cv2.VideoCapture(source_path)

    if source_type == "webcam":
        logger.info("[Fonte] Usando webcam local (cv2.VideoCapture(0))")
        return cv2.VideoCapture(0)

    if source_type in ["onvif", "auto"]:
        use_onvif = os.getenv("USE_ONVIF", "false").strip().lower() == "true"

        if use_onvif and onvif_config:
            try:
                rtsp_url = get_rtsp_from_onvif(
                    onvif_config['ip'],
                    onvif_config.get('port', 80),
                    onvif_config['user'],
                    onvif_config['password']
                )
                logger.info(f"[ONVIF] Conectando via RTSP: {rtsp_url}")
                return cv2.VideoCapture(rtsp_url)
            except Exception as e:
                logger.warning(f"[FALHA ONVIF] {e}")
                logger.info("[Fallback] ONVIF falhou. Usando webcam.")
                return cv2.VideoCapture(0)

    logger.info("[Fallback] Fonte padrão: webcam")
    return cv2.VideoCapture(0)