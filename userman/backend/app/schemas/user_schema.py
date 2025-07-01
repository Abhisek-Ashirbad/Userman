from pydantic import BaseModel, EmailStr, validator, field_validator
from typing import Optional, Annotated
from datetime import date
from pydantic.types import StringConstraints

# Define string constraints
PhoneNumber = Annotated[
    str,
    StringConstraints(pattern=r'^\+?\d{1,3}(?:-)\d{10}$')
]

SecurePassword = Annotated[
    str,
    StringConstraints(min_length=8)
]

class UserBase(BaseModel):
    firstname: str
    middlename: Optional[str] = None
    lastname: str
    username: str
    gender: str
    date_of_birth: date
    email: EmailStr
    phone_number: PhoneNumber
    age: Optional[int] = None  # Add age field with Optional type

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v: str) -> str:
        allowed_genders = ['male', 'female', 'other']
        if v.lower() not in allowed_genders:
            raise ValueError('Gender must be either male, female, or other')
        return v.lower()

    @field_validator('date_of_birth')
    @classmethod
    def validate_dob(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v

    @field_validator('age')
    @classmethod
    def calculate_age(cls, v: Optional[int], values) -> int:
        if 'date_of_birth' in values.data:
            today = date.today()
            dob = values.data['date_of_birth']
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 0:
                raise ValueError('Invalid date of birth')
            return age
        return v or 0  # Return provided age or 0 if no date_of_birth

class UserCreate(UserBase):
    password: SecurePassword

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
