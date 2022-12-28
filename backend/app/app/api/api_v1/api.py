from fastapi import APIRouter
from fastapi_pagination import add_pagination

from app.api.api_v1.endpoints import items, login, users, utils, reviews, order, account, deposit, transaction, \
    item_category, payment_category, payment

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(account.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(deposit.router, prefix="/deposits", tags=["deposits"])
api_router.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(order.router, prefix="/orders", tags=["orders"])
api_router.include_router(item_category.router, prefix="/item-categories", tags=["item-categories"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(payment_category.router, prefix="/payment-categories", tags=["payment-categories"])
api_router.include_router(payment.router, prefix="/payments", tags=["payments"])

add_pagination(api_router)
