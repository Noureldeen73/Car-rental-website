from fastapi import  HTTPException, APIRouter, Depends
from Backend.database import get_db


router = APIRouter(
    prefix = '/Customer',
    tags = ['Customer']
)

@router.get('get_by_id/')
async def get_all_reservations(customer_id: int, db=Depends(get_db)):
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

