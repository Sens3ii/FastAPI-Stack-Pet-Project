# db events
from sqlalchemy import event, func, select, update

from app.models import Review, Item


@event.listens_for(Review, "before_insert")
@event.listens_for(Review, "before_insert")
def update_item_rating(mapper, connection, target):
    item_id = target.item_id
    sql = select(func.avg(Review.rating)).where(Review.item_id == item_id)
    rating = connection.execute(
        sql
    ).scalar()
    stmt = update(Item).where(Item.id == item_id).values(rating=rating)
    connection.execute(stmt)
