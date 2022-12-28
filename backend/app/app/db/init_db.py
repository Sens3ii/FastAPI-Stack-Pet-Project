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

payment_category = [
    {
        'title': "Ads sites",
    },
    {
        'title': "Mobile connection",
    },
    {
        'title': "Bookmakers",
    },
]

payments = [
    {
        'title': "OLX",
        'category_type': "Ads sites",
    },
    {
        'title': "Kolesa",
        'category_type': "Ads sites",
    },
    {
        'title': "Krisha",
        'category_type': "Ads sites",
    },
    {
        'title': "1Fit",
        'category_type': "Bookmakers",
    },
    {
        'title': "1xbet",
        'category_type': "Bookmakers",
    },
    {
        'title': "PariMatch",
        'category_type': "Bookmakers",
    },
    {
        'title': "Beeline",
        'category_type': "Mobile connection",
    },
    {
        'title': "Active/Kcell",
        'category_type': "Mobile connection",
    },
    {
        'title': "Tele2",
        'category_type': "Mobile connection",
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
    },
    {
        "title": "WD 2TB Elements Portable External Hard Drive - USB 3.0 ",
        "description": "WD 2TB Elements Portable ",
        "price": 10000,
        "image_url": "https://fakestoreapi.com/img/61IBBVJvSDL._AC_SY879_.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "Canon EOS 70D Digital SLR Camera",
        "description": "Canon EOS 70D",
        "price": 230000,
        "image_url": "https://m.media-amazon.com/images/I/81U00AkAUWL._AC_SL1500_.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "Lenovo 2022 Ideapad 3 Laptop, 15.6",
        "description": "Lenovo 2022 Ideapad",
        "price": 120000,
        "image_url": "https://m.media-amazon.com/images/I/61QGMX0Qy6L._AC_SL1352_.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "Acer 2022 15inch HD IPS Chromebook",
        "description": "Acer 2022 15inch",
        "price": 170000,
        "image_url": "https://m.media-amazon.com/images/I/71-QYvMpwGL._AC_SL1498_.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "Acer Aspire 5 A515-56-32DK Slim Laptop - 15.6",
        "description": "Acer Aspire 5 A515-56-32DK",
        "price": 210000,
        "image_url": "https://m.media-amazon.com/images/I/71pvhTrmZDL._AC_SL1500_.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "LG C2 77-inch evo OLED TV",
        "description": "LG C2 77-inch evo OLED TV",
        "price": 380000,
        "image_url": "https://www.lg.com/us/images/tvs/md08001966/gallery/DZ_01.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "LG B1 77 inch Class 4K Smart OLED TV w/AI ThinQ",
        "description": "LG B1 77",
        "price": 410000,
        "image_url": "https://www.lg.com/us/images/tvs/md07521464/gallery/Z-01.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "45'' UltraGear™ OLED Curved Gaming Monitor WQHD with 240Hz Refresh Rate",
        "description": "45'' UltraGear™ OLED Curved Gaming Monitor ",
        "price": 200000,
        "image_url": "https://www.lg.com/us/images/monitors/md08003490/gallery/DZ-1_v1.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "WD 4TB Gaming Drive Works with Playstation 4 Portable External Hard Drive",
        "description": "WD 4TB Gaming Drive Works",
        "price": 17000,
        "image_url": "https://fakestoreapi.com/img/61mtL65D4cL._AC_SX679_.jpg",
        "category_type": "Electronics"
    },
    {
        "title": "How Far the Light Reaches: A Life in Ten Sea Creatures",
        "description": "Sabrina Imbler",
        "price": 30,
        "image_url": "https://images-us.bookshop.org/ingram/9780316540537.jpg?height=500&v=v2-d7128781895581d128a991039b3ed97c",
        "category_type": "Books"
    },

    {
        "title": "The January 6th Report",
        "description": "Celadon Books and The New Yorker present the report by the Select Committee to Investigate the Jan 6 Attack on the United States Capitol.",
        "price": 27,
        "image_url": "https://images-us.bookshop.org/ingram/9781250877529.jpg?height=500&v=v2-711ab7f6188e10e9d4a0a328811811a6",
        "category_type": "Books"
    },

    {
        "title": "The Bequest: A Dark Academia Thriller",
        "description": "The Bequest: A Dark Academia Thriller",
        "price": 40,
        "image_url": "https://images-us.bookshop.org/ingram/9781613163443.jpg?height=500&v=v2-2d6e5663244b0afc2fc77d2c72575069",
        "category_type": "Books"
    },

    {
        "title": "The Light We Carry: Overcoming in Uncertain Times",
        "description": "The Light We Carry: Overcoming in Uncertain Times",
        "price": 50,
        "image_url": "https://images-us.bookshop.org/ingram/9780593237465.jpg?height=500&v=v2-f56e0f3e94dd8bc08850b6cd43693503",
        "category_type": "Books"
    },

    {
        "title": "Demon Copperhead",
        "description": "An Oprah's Book Club Selection - An Instant New York Times Bestseller",
        "price": 31,
        "image_url": "https://images-us.bookshop.org/ingram/9780063251922.jpg?height=500&v=v2-2a0401d1fca1ac218ec13add00000000",
        "category_type": "Books"
    },

    {
        "title": "Braiding Sweetgrass",
        "description": "Named a Best Essay Collection of the Decade by Literary Hub",
        "price": 38,
        "image_url": "Named a Best Essay Collection of the Decade by Literary Hub",
        "category_type": "Books"
    },

    {
        "title": "Tomorrow, and Tomorrow, and Tomorrow",
        "description": "NEW YORK TIMES BEST SELLER",
        "price": 45,
        "image_url": "https://images-us.bookshop.org/ingram/9780593321201.jpg?height=500&v=v2-3559920d7919523c7314f5f676233858",
        "category_type": "Books"
    },

    {
        "title": "A Heart That Works",
        "description": "People Fall Must Read pick * 2022 BuzzFeed Fall Reading pick * Time 100 Must-Read Books of 2022A visceral",
        "price": 39,
        "image_url": "https://images-us.bookshop.org/ingram/9781954118317.jpg?height=500&v=v2-0c7b5e7919bc61a78291741b5426a3af",
        "category_type": "Books"
    },

    {
        "title": "Babel: Or the Necessity of Violence",
        "description": "An Arcane History of the Oxford Translators' Revolution",
        "price": 50,
        "image_url": "https://images-us.bookshop.org/ingram/9780063021426.jpg?height=500&v=v2-3103f4fe0d9c610a2b71dadd00000000",
        "category_type": "Books"
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

    for category in payment_category:
        category_obj = crud.payment_category.get_by_title(db, title=category["title"])
        if not category_obj:
            crud.payment_category.create(db, obj_in=schemas.PaymentCategoryCreate(**category))

    for payment in payments:
        payment_obj = crud.payment.get_by_title(db, title=payment["title"])
        if not payment_obj:
            category_id = crud.payment_category.get_by_title(db, title=payment["category_type"]).id
            del payment["category_type"]
            payment["category_id"] = category_id
            crud.payment.create(db, obj_in=schemas.PaymentCreate(**payment))
