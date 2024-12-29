import fastapi
from Backend.database import get_db


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

