from . import Base
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import Integer,String,DateTime
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from datetime import datetime

password_hash = PasswordHash(hashers=[BcryptHasher()])


class User(Base):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    email:Mapped[str] = mapped_column(String(100),unique=True)
    username:Mapped[str] = mapped_column(String(100))
    _password:Mapped[str] = mapped_column(String(200))

    def __init__(self, *args, **kw):
        password = kw.pop('password')
        super.__init__(*args, **kw)
        if password :
            self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = password_hash.hash(raw_password)

    def check_password(self,raw_password):
        return password_hash.verify(raw_password,self.password)

class EmailCode(Base):
    __tablename__ = 'email_code'
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    email:Mapped[str] = mapped_column(String(100),unique=True)
    code:Mapped[str] = mapped_column(String(10))
    create_time: Mapped[datetime] = mapped_column(DateTime,default=datetime.now)