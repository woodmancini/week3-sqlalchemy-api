from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
from database import engine, get_db
import schemas

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def home():
    return {"message":"Week 3 SQLAlchemy API is running"}

@app.get("/courses", response_model=list[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses

# db: Session = Depends(get_db)
# dependency injection: an architectural pattern where a function declares what it needs, and the framework provides it, 
# rather than the function creating the resource itself

# by isolating the database connection logic inside get_db() and injecting it via Depends, 
# your route handlers remain decoupled from the database infrastructure


# strict outbound filter. When your function returns a database record, FastAPI passes it through this Pydantic class. 
# It will strip away any data not explicitly defined in the class, convert the remaining data to a JSON string, and send it to the client. 
# The client will only see id, code, title, and lecturer
@app.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.post("/courses", response_model=schemas.CourseResponse, status_code=201)
def create_course(course_data: schemas.CourseCreate, db: Session = Depends(get_db)):

    course = models.Course(
        code=course_data.code,
        title=course_data.title,
        lecturer=course_data.lecturer
    )

    try:
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Course code already exists")