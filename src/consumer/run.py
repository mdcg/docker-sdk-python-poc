import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter( 
    logging.Formatter(
        fmt="[consumer] %(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
)
logger.addHandler(handler)

if __name__ == "__main__":
    while True:
        logger.info("Hello, World!")
        time.sleep(1)
