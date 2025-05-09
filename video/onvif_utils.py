import os

def get_rtsp_from_onvif(ip, port, user, password):
    """
    Retorna a URL RTSP da câmera ONVIF, ou simula com um vídeo local se USE_ONVIF=false.

    :param ip: Endereço IP da câmera
    :param port: Porta ONVIF (geralmente 80)
    :param user: Usuário da câmera
    :param password: Senha da câmera
    :return: URI RTSP ou caminho para vídeo simulado
    """
    use_onvif = os.getenv("USE_ONVIF", "false").strip().lower() == "true"

    if not use_onvif:
        print("[MOCK] ONVIF desativado. Usando vídeo simulado.")
        return "video.mp4"  # caminho local para vídeo de teste

    try:
        from onvif import ONVIFCamera

        print(f"[ONVIF] Conectando à câmera ONVIF em {ip}:{port}...")
        cam = ONVIFCamera(ip, port, user, password)

        media_service = cam.create_media_service()
        profiles = media_service.GetProfiles()
        profile = profiles[0]

        stream_uri = media_service.GetStreamUri({
            'StreamSetup': {
                'Stream': 'RTP-Unicast',
                'Transport': {'Protocol': 'RTSP'}
            },
            'ProfileToken': profile.token
        })

        print(f"[ONVIF] RTSP obtido com sucesso: {stream_uri.Uri}")
        return stream_uri.Uri

    except Exception as e:
        print(f"[ERRO] Falha ao obter RTSP via ONVIF: {e}")
        print("[FALLBACK] Usando vídeo local simulado.")
        return "video.mp4"