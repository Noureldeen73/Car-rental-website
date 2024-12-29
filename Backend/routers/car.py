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
        if model == '' and year == 0 and city == '':
            cars = []
        elif model == '' and year == 0:
            cars = await db.fetch("""SELECT * FROM Car WHERE office_id IN (SELECT office_id FROM Office WHERE city = $3)""", city)
        elif model == '' and city == '':
            cars = await db.fetch("""SELECT * FROM Car WHERE year = $2""", year)
        elif year == 0 and city == '':
            cars = await db.fetch("""SELECT * FROM Car WHERE model = $1""", model)
        elif year == 0:
            cars = await db.fetch("""SELECT * FROM Car WHERE model = $1 AND 
        office_id IN (SELECT office_id FROM Office WHERE city = $3)""", model, city)
        elif city == '':
            cars = await db.fetch("""SELECT * FROM Car WHERE model = $1 AND year = $2""", model, year)
        elif model == '':
            cars = await db.fetch("""SELECT * FROM Car WHERE year = $2 AND 
        office_id IN (SELECT office_id FROM Office WHERE city = $3)""", year, city)
        else:
            cars = await db.fetch("""SELECT * FROM Car WHERE model = $1 AND year = $2 AND 
        office_id IN (SELECT office_id FROM Office WHERE city = $3)""", model, year, city)
        if not cars:
            raise fastapi.HTTPException(status_code=404, detail="No cars found")
        return [dict(car) for car in cars]

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))

@router.get('/get_car_by_plate_num/')
async def get_reservations_by_car(plate_number: str, db=fastapi.Depends(get_db)):
    try:
        car = await db.fetchrow("""SELECT * FROM Car c JOIN office o ON c.office_id = o.office_id WHERE plate_number = $1""", plate_number)
        if not car:
            raise fastapi.HTTPException(status_code=404, detail="No car is found")
        return dict(car)  # Convert asyncpg record to dictionary

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))

