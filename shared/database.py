from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from shared.instances import engine


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    message: Mapped[str]


Base.metadata.create_all(engine)
