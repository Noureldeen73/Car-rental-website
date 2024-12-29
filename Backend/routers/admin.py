import fastapi
from Backend.database import get_db


router = fastapi.APIRouter(
    prefix = '/Admin',
    tags = ['Admin']
)

@router.get('/Admin/get_all_reservations/')
async def get_all_reservations(db=fastapi.Depends(get_db)):
    try:
        reservations = await db.fetch("""SELECT * FROM Reservation""")
        if not reservations:
            raise fastapi.HTTPException(status_code=404, detail="No reservations found")
        return [dict(reservation) for reservation in reservations]  # Convert asyncpg record to dictionary
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))



@router.get('Admin/get_reservations_by_car/')
async def get_reservations_by_car(car_id: int, db=fastapi.Depends(get_db)):
    try:
        reservations = await db.fetch("""SELECT * FROM Reservation WHERE car_id = $1""", car_id)
        if not reservations:
            raise fastapi.HTTPException(status_code=404, detail="No reservations found")
        return [dict(reservation) for reservation in reservations]  # Convert asyncpg record to dictionary
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))

