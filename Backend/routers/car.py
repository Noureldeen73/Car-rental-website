from math import ceil

import fastapi
from Backend.database import get_db
from datetime import datetime

router = fastapi.APIRouter(
    prefix = '/Car',
    tags = ['Car']
)

#model year city
@router.get('/get_car_by_filter/')
async def get_all_reservations(model: str, year:int, city:str, db=fastapi.Depends(get_db)):
    try:
        cars = await db.fetch("""SELECT * FROM Car WHERE model = $1 AND year = $2 AND 
        office_id IN (SELECT office_id FROM Office WHERE city = $3)""", model, year, city)
        if not cars:
            raise fastapi.HTTPException(status_code=404, detail="No cars found")
        return [dict(car) for car in cars]  # Convert asyncpg record to dictionary

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))

@router.get('/get_car_by_plate_num/')
async def get_reservations_by_car(plate_number: str, db=fastapi.Depends(get_db)):
    try:
        car = await db.fetchrow("""SELECT * FROM Car WHERE plate_number = $1""", plate_number)
        if not car:
            raise fastapi.HTTPException(status_code=404, detail="No car is found")
        return dict(car)  # Convert asyncpg record to dictionary

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


@router.get('/get_reservation_dates_by_car')
async def get_reservation_dates_by_plate_number(plate_number:str, db=fastapi.Depends(get_db)):
    try:
        dates = await db.fetch("""SELECT pick_up_date, return_date FROM Reservation WHERE plate_number = $1""", plate_number)

        if not dates:
            return []

        return [dict(date) for date in dates]  # Convert asyncpg record to dictionary

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


@router.post('/make_reservation')
async def create_reservation(hoss: str,
                             pickup_date: str,
                             return_date: str,
                             plate_number: str, customer_id:int,
                             payment_type:str, db=fastapi.Depends(get_db)):
    try:
        hoss = datetime.fromisoformat(hoss)
        pickup_date = datetime.fromisoformat(pickup_date)
        return_date = datetime.fromisoformat(return_date)

        not_available = await db.fetchrow("""
        SELECT * FROM reservation where pick_up_date between $1 and $2 and plate_number = $3
        """, pickup_date, return_date, plate_number)

        if not_available:
            raise ValueError("Car is not available for the selected dates.")

        not_available = await db.fetchrow("""
        SELECT * FROM reservation where return_date between $1 and $2 and plate_number = $3
        """, pickup_date, return_date, plate_number)

        if not_available:
            raise ValueError("Car is not available for the selected dates.")

        await db.execute(
            """INSERT INTO Reservation (reservation_date, pick_up_date, return_date, plate_number, customer_id) VALUES ($1, $2, $3, $4, $5)""",
            hoss, pickup_date, return_date, plate_number, customer_id )

        reservation = await db.fetchrow("""SELECT reservation_id FROM Reservation WHERE reservation_date = $1 
        AND pick_up_date = $2 AND return_date = $3 AND plate_number = $4 AND customer_id = $5""",
                                        hoss, pickup_date, return_date, plate_number, customer_id)

        reservation_id = reservation['reservation_id']

        price = await db.fetchrow("""SELECT price FROM Car WHERE plate_number = $1""", plate_number)
        daily_price = price['price']
        total_days = ceil(((return_date - pickup_date).total_seconds() / (3600*24)))

        if total_days < 0:
            raise ValueError("Return date must be after pickup date.")

        total_price = daily_price * total_days

        await db.execute(
            """INSERT INTO Payment (payment_type, payment_date, total_price, reservation_id) VALUES ($1, $2, $3, $4)""",
            payment_type, hoss, total_price, reservation_id)

        return {"reservation_id": reservation_id, "payment_type": payment_type, "total_price": total_price}

    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))