from datetime import datetime
from typing import List

import fastapi
from asyncpg import Record
from fastapi import HTTPException, Depends
from Backend.database import get_db


router = fastapi.APIRouter(
    prefix = '/Admin',
    tags = ['Admin']
)

@router.get('/get_all_reservations_in_period/')
async def get_all_reservations(
        start_date: str,
        end_date: str,
        db=fastapi.Depends(get_db)
):
    try:

        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")  # Add 1 day to include the full end_date

        query = """
        SELECT * 
        FROM Reservation
        WHERE (
            pick_up_date::date BETWEEN $1 AND ($2::timestamp + INTERVAL '1 day')
            OR 
            return_date::date BETWEEN $1 AND ($2::timestamp + INTERVAL '1 day')
            OR 
            $1 BETWEEN pick_up_date::date AND (return_date + INTERVAL '1 day')
            OR 
            $2 BETWEEN pick_up_date::date AND (return_date+INTERVAL '1 day')
        )
        """
        reservations = await db.fetch(query, start_date_dt, end_date_dt)

        if not reservations:
            raise fastapi.HTTPException(status_code=404, detail="No reservations found")

        # Convert asyncpg records to dictionaries
        return [dict(reservation) for reservation in reservations]

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"Error fetching reservations: {str(e)}")



@router.get('/get_reservations_by_car/')
async def get_reservations_by_car(plat_id: str, db=fastapi.Depends(get_db)):
    try:
        reservations = await db.fetch("""SELECT * FROM Reservation WHERE plate_number = $1""", plat_id)
        if not reservations:
            raise fastapi.HTTPException(status_code=404, detail="No reservations found")
        return [dict(reservation) for reservation in reservations]  # Convert asyncpg record to dictionary
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))

@router.get('/get_status_cars/')
async def get_status_cars(user_id: int, db=fastapi.Depends(get_db)):
    try:
        cars = await db.fetch("""
        SELECT plate_number, available FROM Car WHERE available = True and office_id IN (SELECT office_id FROM Admin WHERE user_id = $1)""", user_id)
        if not cars:
            raise fastapi.HTTPException(status_code=404, detail="No cars found")
        return [dict(car) for car in cars]  # Convert asyncpg record to dictionary
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))

@router.get('/get_reservations_by_customer/')
async def get_reservations_by_customer(customer_id: int, db=fastapi.Depends(get_db)):
    customer_data = await db.fetchrow(
        """
        SELECT first_name, last_name, phone_number, city, street, zip_code 
        FROM Customer 
        WHERE customer_id = $1
        """,
        customer_id,
    )
    if not customer_data:
        raise HTTPException(status_code=404, detail="No customer found")

    reservations = await db.fetch(
        """
        SELECT r.reservation_date, r.pick_up_date, r.return_date, c.model, c.year, c.plate_number,p.total_price ,o.office_name, o.city
        FROM Reservation r
        JOIN Car c ON r.plate_number = c.plate_number
        JOIN Office o ON c.office_id = o.office_id 
        JOIN Customer cu ON r.customer_id = cu.customer_id
        JOIN Payment p ON r.reservation_id = p.reservation_id
        WHERE cu.customer_id = $1
        """,
        customer_id,
    )
    if not reservations:
        raise HTTPException(status_code=404, detail="No reservations found")
    return {"customer_data": dict(customer_data), "reservations": [dict(reservation) for reservation in reservations]}

@router.get('/get_daily_pay_in_period/')

async def get_daily_pay_in_period(
    start_date: str,
    end_date: str ,
    db = Depends(get_db)
    ):
    try:
        # Convert strings to datetime objects
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

        # Execute the query
        query = """
            SELECT payment_date::date AS payment_date, 
                   SUM(total_price) AS daily_payment
            FROM Payment
            WHERE payment_date >= $1 AND payment_date < ($2::timestamp + INTERVAL '1 day')
            GROUP BY payment_date::date
            ORDER BY payment_date::date;
            """
        payments: List[Record] = await db.fetch(query, start_date_dt, end_date_dt)

        if not payments:
            raise HTTPException(status_code=404, detail="No payments found")
        # Convert asyncpg records to dictionaries
        return [dict(payment) for payment in payments]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching daily payments: {str(e)}")