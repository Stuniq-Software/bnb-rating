from fastapi import APIRouter, Request, Response
from dtypes import APIResponse, HttpStatus
from repository import RatingsRepository
from util import Database, RedisSession


router = APIRouter(prefix="/api/v1/ratings", tags=["Ratings"])
rating_service = RatingsRepository(
    db_session=Database(),
    redis_session=RedisSession()
)


@router.get("/{uid}")
async def get_ratings(uid: str, response: Response, id_type: str = "rating"):
    try:
        if id_type not in ["rating", "stay", "user"]:
            response.status_code = 400
            return APIResponse(status=HttpStatus.BAD_REQUEST, message="Invalid id_type", data=None)
        
        success, data = False, None

        if id_type == "rating":
            success, data = rating_service.get_rating_by_id(uid)
        elif id_type == "stay":
            success, data = rating_service.get_ratings_by_stay(uid)
        elif id_type == "user":
            success, data = rating_service.get_ratings_by_user(uid)
        
        if not success:
            response.status_code = 404
            return APIResponse(status=HttpStatus.NOT_FOUND, message="Rating not found", data=None)
        return APIResponse(status=HttpStatus.OK, message="Rating retrieved", data=data)
    except Exception as e:
        response.status_code = 500
        return APIResponse(status=HttpStatus.INTERNAL_SERVER_ERROR, message=str(e), data=None)


@router.post("/")
async def create_rating(request: Request, response: Response):
    try:
        data = await request.json()
        user_id = data.get("user_id")
        stay_id = data.get("stay_id")
        rating = data.get("rating")
        title = data.get("title")
        comment = data.get("comment")
        
        if not user_id or not stay_id or not rating or not title or not comment:
            response.status_code = 400
            return APIResponse(status=HttpStatus.BAD_REQUEST, message="Missing required fields")
        
        success, err = rating_service.create_rating(user_id, stay_id, rating, title, comment)
        if not success:
            response.status_code = 500
            return APIResponse(status=HttpStatus.INTERNAL_SERVER_ERROR, message=err, data=None)
        return APIResponse(status=HttpStatus.OK, message="Rating created", data=None)
    except Exception as e:
        response.status_code = 500
        return APIResponse(status=HttpStatus.INTERNAL_SERVER_ERROR, message=str(e), data=None)