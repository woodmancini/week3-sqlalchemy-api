import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    courses = [
        models.Course(code="CC101", title="Cloud Computing", lecturer="Stelios"),
        models.Course(code="DB101", title="Databases", lecturer="Maria"),
    ]

    for course in courses:
        existing_course = (
            db.query(models.Course)
            .filter(models.Course.code == course.code)
            .first()
        )

        if existing_course is None:
            db.add(course)

    db.commit()

    print("Database created and courses checked.")

finally:
    db.close()