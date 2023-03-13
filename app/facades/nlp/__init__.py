from app import config
from app.facades.nlp.cotoha import CotohaFacade
from app.utils.logging import logger

if config.cotoha_client_id != "" and config.cotoha_client_secret != "":
    logger.info(f"Use Cotoha NLP API")
    cotoha = CotohaFacade(config.cotoha_client_id, config.cotoha_client_secret)
else:
    logger.info(f"Dont Use Cotoha NLP API")
    cotoha = None
