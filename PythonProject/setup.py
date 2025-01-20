import logging

from dotenv import load_dotenv

logging.basicConfig(filename='errors.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()