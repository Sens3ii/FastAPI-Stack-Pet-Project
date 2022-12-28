from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, reviews, order, account

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(order.router, prefix="/orders", tags=["orders"])
api_router.include_router(account.router, prefix="/accounts", tags=["accounts"])
