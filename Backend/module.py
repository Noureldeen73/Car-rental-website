from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: Optional[int]
    email: str
    password: str
    is_admin: bool

class Customer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    phone_number: str
    city: str
    street: str
    zip_code: str
    user_id: int

class Office(BaseModel):
    office_id: int
    office_name: str
    city: str
    street: str
    zip_code: str


class Admin(BaseModel):
    admin_id: int
    first_name: str
    last_name: str
    user_id: int
    office_id: int

class Car(BaseModel):
    car_id: int
    plate_number: str
    model : str
    year: int
    free : bool
    office_id: int

class Reservation(BaseModel):
    reservation_id: int
    reservation_date: str
    pick_up_date: str
    return_date: str
    car_id: int
    customer_id: int

class Payment(BaseModel):
    payment_id: int
    payment_type: str
    payment_date: str
    amount: float
    reservation_id: int

