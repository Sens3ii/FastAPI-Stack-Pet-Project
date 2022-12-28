from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.auth import User, UsersRoles
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            phone=obj_in.phone,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            gender=obj_in.gender,
            birth_date=obj_in.birth_date,
            hashed_password=get_password_hash(obj_in.password),
            avatar_url=obj_in.avatar_url,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        crud.role.delete_roles_by_user_id(db=db, user_id=db_obj.id)
        role = crud.role.get_by_codename(db=db, codename=obj_in.role_code)
        crud.role.add_user(db=db, role_id=role.id, user_id=db_obj.id)
        crud.account.generate_user_account(db=db, user_id=db_obj.id)
        crud.deposit.generate_user_deposit(db=db, user_id=db_obj.id)
        return db_obj

    @staticmethod
    def update_password(db: Session, *, db_obj: User, password: str) -> User:
        hashed_password = get_password_hash(password)
        db_obj.hashed_password = hashed_password
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_admin(self, db, user: User) -> bool:
        role_id = crud.role.get_by_codename(db, codename="admin").id
        query = db.query(UsersRoles).filter(UsersRoles.user_id == user.id, UsersRoles.role_id == role_id).first()
        return bool(query)

    def is_seller(self, db, user: User) -> bool:
        role_id = crud.role.get_by_codename(db, codename="seller").id
        query = db.query(UsersRoles).filter(UsersRoles.user_id == user.id, UsersRoles.role_id == role_id).first()
        return bool(query)


user = CRUDUser(User)
