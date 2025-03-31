import logging
from typing import Optional
from app.database.connection import get_database

logger = logging.getLogger(__name__)

# class DatabaseService:
#     def __init__(self):
#         self.db = None

#     async def connect(self):
#         '''Initialize database connection'''
#         try:
#             self.db = await get_database()
#             return self.db
#         except Exception as e:
#             logger.error(f'Error connecting to database: {str(e)}')
#             raise
    
#     async def get_collection(self, collection_name: str):
#         '''Get a collection'''
#         if not self.db:
#             await self.connect()
#         return self.db[collection_name]
    
#     async def get_all_attack_prompts(self):
#         '''Get all prompts that are attacks.
#         Returns a list of prompts with objectid converted to str
#         '''
#         try:
#             collection = await self.get_collection('prompts')
#             cursor = collection.find({'isAttack': True})
#             prompts = await cursor.to_list(length=None)

#             # Conver OjbectID to str
#             for prompt in prompts:
#                 if '_id' in prompt:
#                     prompt['id'] = str(prompt['_id'])
#             return prompts
#         except Exception as e:
#             logger.error(f'Error fetching attack prompts: {str(e)}')
#             raise

#     async def get_all_clean_prompts(self):
#         try:
#             collection = await self.get_collection('prompts')
#             cursor = collection.find({'isAttack': False})
#             prompts = await cursor.to_list(length=None)

#             # Conver OjbectID to str
#             for prompt in prompts:
#                 if '_id' in prompt:
#                     prompt['id'] = str(prompt['_id'])
#             return prompts
#         except Exception as e:
#             logger.error(f'Error fetching clean prompts: {str(e)}')
#             raise

#     async def get_all_prompts(self):
#         try:
#             collection = await self.get_collection('prompts')
#             cursor = collection.find()
#             prompts = await cursor.to_list(length=None)

#             # Conver OjbectID to str
#             for prompt in prompts:
#                 if '_id' in prompt:
#                     prompt['id'] = str(prompt['_id'])
#             return prompts
#         except Exception as e:
#             logger.error(f'Error fetching all prompts: {str(e)}')
#             raise

#      async def get_all_prompts(self):
#         try:
#             collection = await self.get_collection('prompts')
#             cursor = collection.find()
#             prompts = await cursor.to_list(length=None)

#             # Conver OjbectID to str
#             for prompt in prompts:
#                 if '_id' in prompt:
#                     prompt['id'] = str(prompt['_id'])
#             return prompts
#         except Exception as e:
#             logger.error(f'Error fetching all prompts: {str(e)}')
#             raise


async def get_db():
    """
    Dependency function to get database connection for routes
    Returns a database connection that can be used in route handlers
    """
    try:
        db = await get_database()
        return db
    except Exception as e:
        logger.error(f"Error getting database connection: {str(e)}")
        raise

