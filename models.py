from sqlalchemy import Column, Integer, String

from database import Base

class Course(Base):

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, unique=True, nullable=False)

    title = Column(String, nullable=False)

    lecturer = Column(String, nullable=False)

