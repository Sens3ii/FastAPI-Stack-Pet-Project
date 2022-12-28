from .crud_account import account
from .crud_deposit import deposit
from .crud_item import item
from .crud_item_category import item_category
from .crud_order import order
from .crud_payment import payment
from .crud_payment_category import payment_category
from .crud_review import review
from .crud_role import role
from .crud_transaction import transaction_log
from .crud_user import user
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
