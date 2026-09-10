from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
	__tablename__ = "tasks"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	title: Mapped[str] = mapped_column(String(200), nullable = False)
	description: Mapped[str] = mapped_column(String(1000), nullable = False)
	completed: Mapped[bool] = mapped_column(Boolean, default = False, nullable = False)
