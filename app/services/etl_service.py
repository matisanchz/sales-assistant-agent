import logging

from app.etl import users_etl

logger = logging.getLogger(__name__)

class EtlService():

    async def load_users_data(self):
        try:
            await users_etl.run()
        except Exception as e:
            logger.error("An error occur during etl process for users")
            raise e
        
    async def load_documents(self):
        try:
            #await documents_etl.run()
            pass
        except Exception as e:
            logger.error("An error occur during etl process for documents")
            raise e