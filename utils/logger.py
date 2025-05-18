import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("tgconnect.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
