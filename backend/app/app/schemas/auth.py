from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    codename: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int

    class Config:
        orm_mode = True
