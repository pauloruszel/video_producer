import cv2
import os
from .onvif_utils import get_rtsp_from_onvif


def open_video_source(source_type="auto", source_path=None, onvif_config=None):
    """
    Abre a fonte de vídeo com base na configuração:
    - "webcam": usa a câmera local
    - "video": usa um arquivo de vídeo local
    - "onvif": força ONVIF
    - "auto": tenta ONVIF se ativado, senão webcam
    """
    if source_type == "video":
        return cv2.VideoCapture(source_path)

    if source_type == "webcam":
        print("[Fonte] Usando webcam local (cv2.VideoCapture(0))")
        return cv2.VideoCapture(0)

    if source_type == "onvif" or source_type == "auto":
        use_onvif = os.getenv("USE_ONVIF", "false").strip().lower() == "true"

        if use_onvif and onvif_config:
            try:
                rtsp_url = get_rtsp_from_onvif(
                    onvif_config['ip'],
                    onvif_config.get('port', 80),
                    onvif_config['user'],
                    onvif_config['password']
                )
                print(f"[ONVIF] Conectando via RTSP: {rtsp_url}")
                return cv2.VideoCapture(rtsp_url)
            except Exception as e:
                print(f"[FALHA ONVIF] {e}")
                print("[Fallback] ONVIF falhou. Usando webcam.")
                return cv2.VideoCapture(0)

    # fallback final
    return cv2.VideoCapture(0)