from pydantic import BaseModel, ConfigDict, Field

class CourseCreate(BaseModel):
    code: str = Field(min_length=2, max_length=20)
    title: str = Field(min_length=3, max_length=100)
    lecturer: str = Field(min_length=2, max_length=280)


class CourseResponse(BaseModel):
    id: int
    code: str
    title: str
    lecturer: str

    model_config = ConfigDict(from_attributes=True)

# from_attributes=True tells Pydantic to check for attributes if dictionary lookups fail
# ie data.title (from object attributes)
# if data["title"] fails