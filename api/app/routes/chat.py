print('on hold')

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from app.services.llm_service import LLMService # send to LLM
# from app.services.prompt_detector import PromptDetectorService
# from app.services.db_service import DatabaseService
# import logging

# router = APIRouter(
#     prefix="/chat",
#     tags=["chat"]
# )

# logger = logging.getLogger(__name__)
# llm_service = LLMService()
# prompt_detector = PromptDetectorService()
# db_service = DatabaseService()

# class ChatRequest(BaseModel):
#     text: str

# class ChatResponse(BaseModel):
#     response: str

# class HealthCheckResponse(BaseModel):
#     status: str
#     message: str

# @router.get("/health", response_model=HealthCheckResponse)
# async def health_check():
#     """
#     Check the health of the LLM service connection
#     """
#     try:
#         result = await llm_service.health_check()
#         return HealthCheckResponse(**result)
#     except Exception as e:
#         logger.error(f"Health check failed: {str(e)}")
#         raise HTTPException(status_code=500, detail="Health check failed")

# @router.post("/prompt", response_model=ChatResponse)
# async def process_chat(request: ChatRequest):
#     """
#     Process a chat prompt and return the LLM response
#     """
#     try:

#         # Send it to the fake detector for now until the real one is build
#         is_safe, detection_result = await prompt_detector.analyze(request.text)

#         # Store the prompt in the db
#         await db_service.store_prompt(
#             prompt_text=request.text,
#             is_safe=is_safe,
#             detection_result=detection_result
#         )

#         # If the prompt is unsafe, return an error
#         if not is_safe:
#             logger.warning(f'Potentially unsafe prompt detected: {request.text[:30]}...')
#             raise HTTPException(
#                 status_code=400,
#                 detail="Request had unsafe content and we're not processing it."
#             )
        
#         # If safe, get the response from the LLM
        
#         logger.info(f'Processing safe prompt: {request.text[:30]}')
#         result = await llm_service.generate_response(request.text)
        
#         # Handle different response formats
#         if isinstance(result, dict):
#             # Handle direct dictionary response
#             response_text = result.get('generated_text', '')
#         elif isinstance(result, list) and len(result) > 0:
#             # Handle list of responses (take the first one)
#             if isinstance(result[0], dict):
#                 response_text = result[0].get('generated_text', '')
#             else:
#                 response_text = str(result[0])
#         else:
#             # If we get an unexpected format, convert to string
#             response_text = str(result) if result else "No response generated"
        
#         # Ensure we have some content to return
#         if not response_text:
#             response_text = "The model didn't generate a response. Please try again."
        
#         logger.info(f"Generated response for prompt: {request.text[:30]}...")
#         return ChatResponse(response=response_text)
        
#     except ValueError as ve:
#         logger.error(f"Validation error: {str(ve)}")
#         raise HTTPException(status_code=400, detail=str(ve))
#     except ConnectionError as ce:
#         logger.error(f"Connection error with LLM service: {str(ce)}")
#         raise HTTPException(status_code=503, detail="Unable to connect to LLM service")
#     except TimeoutError as te:
#         logger.error(f"Timeout error with LLM service: {str(te)}")
#         raise HTTPException(status_code=504, detail="LLM service request timed out")
#     except Exception as e:
#         logger.error(f"Error processing chat: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to process chat prompt")

