from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

items = [
    {
        "title": "Item 1",
        "description": "This is the first item in the list",
        "price": 10,
    },
    {
        "title": "Item 2",
        "description": "This is the second item in the list",
        "price": 20
    },
    {
        "title": "Item 3",
        "description": "This is the third item in the list",
        "price": 30
    },
    {
        "title": "Item 4",
        "description": "This is the fourth item in the list",
        "price": 40
    },
    {
        "title": "Item 5",
        "description": "This is the fifth item in the list",
        "price": 50
    },
    {
        "title": "Item 6",
        "description": "This is the sixth item in the list",
        "price": 60
    },
    {
        "title": "Item 7",
        "description": "This is the seventh item in the list",
        "price": 70
    },
    {
        "title": "Item 8",
        "description": "This is the eighth item in the list",
        "price": 80
    },
    {
        "title": "Item 9",
        "description": "This is the ninth item in the list",
        "price": 90
    },
    {
        "title": "Item 10",
        "description": "This is the tenth item in the list",
        "price": 100
    }
]

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
        "avatar_url":  "https://i.imgur.com/BN1WW4d_d.webp?maxwidth=520&shape=thumb&fidelity=high"
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
            user_obj = crud.user.create(db, obj_in=schemas.UserCreate(**user))
        # Create items
        if user["role_code"] in ['admin', 'seller']:
            for item in items:
                crud.item.create_with_owner(db, obj_in=schemas.ItemCreate(**item), owner_id=user_obj.id)
