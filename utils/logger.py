import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s:[%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
