import models
from database import SessionLocal

db = SessionLocal()

try:
    courses = db.query(models.Course).all()

    for course in courses:
        print(course.id, course.code, course.title, course.lecturer)

finally:
    db.close()