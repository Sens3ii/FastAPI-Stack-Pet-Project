from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


roles = [
    {"name": "Admin", "codename": "admin"},
    {"name": "Seller", "codename": "seller"},
    {"name": "Client", "codename": "client"},
]

users = [
    {
        "email": settings.FIRST_SUPERUSER,
        "phone": "+77772821175",
        "first_name": "Daniil",
        "last_name": "Koilybayev",
        "gender": "MAN",
        "birth_date": "2001-10-23",
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "role_code": 'admin',
        "avatar_url": "https://i.imgur.com/BN1WW4d_d.webp?maxwidth=520&shape=thumb&fidelity=high"
    },
    {
        "email": "seller@jusan.com",
        "phone": "123-456-7891",
        "first_name": "Jane",
        "last_name": "Doe",
        "gender": "MAN",
        "birth_date": "1991-02-01",
        "password": "seller",
        "role_code": 'seller',
        "avatar_url": "https://phonoteka.org/uploads/posts/2021-07/1625636249_8-phonoteka-org-p-sidorovich-art-krasivo-8.jpg"
    },
    {
        "email": "client@jusan.com",
        "phone": "123-456-7895",
        "first_name": "MBAPPE",
        "last_name": "MBAPPE",
        "gender": "MAN",
        "birth_date": "1995-06-01",
        "password": "client",
        "role_code": 'client',
        "avatar_url": "https://footballhd.kz/uploads/posts/2022-12/1671630976_mbappe.jpg"
    },
    {
        "email": "client2@jusan.com",
        "phone": "123-456-7895",
        "first_name": "MESSI",
        "last_name": "MESSI",
        "gender": "MAN",
        "birth_date": "1995-06-01",
        "password": "client2",
        "role_code": 'client',
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg/250px-Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg"
    },
]

item_category = [
    {
        'title': "Electronics",
    },
    {
        'title': "Furniture",
    },
    {
        'title': "Books",
    },
]

items = [
    {
        "title": "iPhone 12",
        "description": "iPhone 12",
        "price": 100000,
        "image_url": "https://www.apple.com/v/iphone-14/d/images/overview/selfies/selfie_startframe__ex2suisayck2_large.jpg",
        "category_type": "Electronics",
    },
    {
        "title": "Стул",
        "description": "Стул",
        "price": 10000,
        "image_url": "https://i.imgur.com/1fqp78I_d.webp?maxwidth=520&shape=thumb&fidelity=high",
        "category_type": "Furniture",
    },
    {
        "title": "От нуля к единице. Как создать стартап, который изменит будущее",
        "description": "Книга «От нуля к единице» посвящена технологиям создания успешного стартапа, ведущего к образованию мощного монопольного бизнеса. Понимая конкуренцию как разрушительную силу, Питер Тиль предлагает своему читателю убедиться в действенности монополистических бизнес-стратегий на примере опыта огромного количества компаний, среди которых Facebook, Microsoft, eBay, Twitter и многие другие. Кроме того, книга содержит рассуждения о том, что такое стартапное мышление, и рекомендации по формированию сплоченной рабочей команды.",
        "price": 1000,
        "image_url": "https://cdn.f.kz/prod/479/478181_1000.jpg",
        "category_type": "Books",
    }
]


def init_db(db: Session) -> None:
    # Base.metadata.create_all(bind=engine)
    # creating roles
    for role in roles:
        role_obj = crud.role.get_by_codename(db, codename=role["codename"])
        if not role_obj:
            crud.role.create(db, obj_in=schemas.RoleCreate(**role))

    # create users
    for user in users:
        user_obj = crud.user.get_by_email(db, email=user["email"])
        if not user_obj:
            crud.user.create(db, obj_in=schemas.UserCreate(**user))

    for category in item_category:
        category_obj = crud.item_category.get_by_title(db, title=category["title"])
        if not category_obj:
            crud.item_category.create(db, obj_in=schemas.ItemCategoryCreate(**category))

    for item in items:
        item_obj = crud.item.get_by_title(db, title=item["title"])
        if not item_obj:
            category_id = crud.item_category.get_by_title(db, title=item["category_type"]).id
            seller_id = crud.user.get_by_email(db, email="seller@jusan.com").id
            del item["category_type"]
            item["category_id"] = category_id
            item["owner_id"] = seller_id
            crud.item.create(db, obj_in=schemas.ItemCreate(**item))
