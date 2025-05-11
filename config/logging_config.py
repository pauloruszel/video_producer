import logging

def configurar_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Troque para INFO em produção
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )