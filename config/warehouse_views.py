import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def warehouse_check_api(request, book_id):
    logger.info(f"[ProjectB - Warehouse] Checking stock for book_id: {book_id}")
    
    # Проста імітація складу
    if book_id % 2 == 0:
        data = {"book_id": book_id, "available": True, "stock": 42}
    else:
        data = {"book_id": book_id, "available": False, "stock": 0}
        
    return JsonResponse(data, status=200)