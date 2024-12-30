from dataclasses import field
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
async def get_all_reservations(
        model: str = "",
        year: int = 0,
        city: str = "",
        db=fastapi.Depends(get_db)
):
    """
    Fetch cars based on the provided model, year, and city filters.
    """
    try:
        # Base query
        query = "SELECT * FROM Car c join office o on c.office_id = o.office_id"
        filters = []
        params = []
        city = city.replace('+', ' ') if '+' in city else city
        if city:
            city = " ".join(word.capitalize() for word in city.split(" "))
        if model:
            model = model.capitalize()
        print (model)
        # Add filters dynamically
        if model:
            filters.append(f"model LIKE ${len(params) + 1}")
            params.append(f"%{model}%")
        if year:
            filters.append(f"year = ${len(params) + 1}")
            params.append(year)
        if city:
            filters.append(f"o.city LIKE ${len(params) + 1}")
            params.append(f"%{city}%")
        # Combine filters into the query
        if filters:
            query += " WHERE " + " AND ".join(filters)
        # Execute the query
        cars = await db.fetch(query, *params)

        if not cars:
            raise fastapi.HTTPException(status_code=404, detail="No cars found")

        # Convert asyncpg records to dictionaries
        return [dict(car) for car in cars]

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"Error fetching cars: {str(e)}")

@router.get('/get_car_by_plate_num/')
async def get_reservations_by_car(plate_number: str, db=fastapi.Depends(get_db)):
    try:
        car = await db.fetchrow("""SELECT * FROM Car c join office O on c.office_id = o.office_id WHERE plate_number = $1""", plate_number)
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
async def create_reservation(reservation_date: str,
                             pickup_date: str,
                             return_date: str,
                             plate_number: str, customer_id:int,
                             payment_type:str = "Cash", db=fastapi.Depends(get_db)):
    try:
        reservation_date = datetime.fromisoformat(reservation_date)
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
            reservation_date, pickup_date, return_date, plate_number, customer_id )

        reservation = await db.fetchrow("""SELECT reservation_id FROM Reservation WHERE reservation_date = $1 
        AND pick_up_date = $2 AND return_date = $3 AND plate_number = $4 AND customer_id = $5""",
                                        reservation_date, pickup_date, return_date, plate_number, customer_id)

        reservation_id = reservation['reservation_id']

        price = await db.fetchrow("""SELECT price FROM Car WHERE plate_number = $1""", plate_number)
        daily_price = price['price']
        total_days = ceil(((return_date - pickup_date).total_seconds() / (3600*24)))

        if total_days < 0:
            raise ValueError("Return date must be after pickup date.")

        total_price = daily_price * total_days

        await db.execute(
            """INSERT INTO Payment (payment_type, payment_date, total_price, reservation_id) VALUES ($1, $2, $3, $4)""",
            payment_type, reservation_date, total_price, reservation_id)

        return {"reservation_id": reservation_id, "payment_type": payment_type, "total_price": total_price}

    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))