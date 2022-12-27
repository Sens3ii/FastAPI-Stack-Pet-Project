from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Role, UsersRoles
from app.schemas import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    def get_multi_by_user(
            self, db: Session, *, user_id: int
    ) -> list[Role]:
        return db.query(self.model).filter(Role.users.any(user_id=user_id)).all()

    def get_by_codename(
            self, db: Session, *, codename: str
    ) -> Role:
        return db.query(self.model).filter(self.model.codename == codename).first()

    @staticmethod
    def add_user(db: Session, *, role_id: int, user_id: int):
        db.add(UsersRoles(role_id=role_id, user_id=user_id))
        db.commit()

    @staticmethod
    def delete_roles_by_user_id(db: Session, user_id: int):
        db.query(UsersRoles).filter(
            UsersRoles.user_id == user_id
        ).delete()


role = CRUDRole(Role)
