from fastapi import APIRouter, HTTPException
from database.driverservice import *

drivers_router = APIRouter(tags=['Управление водителями'], prefix='/drivers')


# Регистрация нового водителя
@drivers_router.post('/api/register_new_driver')
async def register_new_driver(
        name: str,
        surname: str,
        middle_name: str,
        phone_number: str,
        age: int,
        gender: str,
        rating: float,
        license_number: str,
        car_plate: str,
        car_model: str,
        status: str,
        tariff_id: int
):
    try:
        result = register_driver_db(
            name,
            surname,
            middle_name,
            phone_number,
            age,
            gender,
            rating,
            license_number,
            car_plate,
            car_model,
            status,
            tariff_id
        )

        if result:
            return {'message': result}
        raise HTTPException(status_code=400, detail='Error registering driver')
    except:
        return 'Повторите попытку!'


# Поиск водителей по заданному запросу
@drivers_router.post('/api/search_driver')
async def search_driver(query: str):
    result = search_driver_db(query)
    if result:
        return result
    return {'message': 'No matching drivers found'}


# Удаление водителя
@drivers_router.delete('/api/delete_driver')
async def delete_driver(driver_id: int):
    result = delete_driver_db(driver_id)
    if result:
        return {'message': 'Driver successfully deleted'}
    raise HTTPException(status_code=404, detail='Driver not found')


# Получение списка всех водителей
@drivers_router.get('/api/get_all_drivers')
async def get_all_drivers():
    return get_all_drivers_db()


# Получение детальной информации о водителе
@drivers_router.get('/api/get_detailed_driver')
async def get_detailed_driver(driver_id: int):
    result = get_detailed_driver_db(driver_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Driver not found")


# Получение статистики водителей
@drivers_router.get('/api/get_driver_statistics')
async def get_driver_statistics():
    return get_statistics_db()


# Получение количества водителей
@drivers_router.get('/api/get_drivers_count')
async def get_drivers_count():
    return get_drivers_count_db()


# Получение топ 3 водителей по рейтингу
@drivers_router.get('/api/get_top_3_drivers')
async def get_top_3_drivers():
    return get_top_three_drivers_db()


# Подсчет водителей, зарегистрированных в указанном месяце
@drivers_router.get('/api/count_drivers_registered_in_last_7_months')
async def count_drivers_registered_in_last_7_months():
    return count_drivers_registered_in_last_7_months_db()


@drivers_router.get('/api/count_orders_for_driver')
async def count_orders_for_driver(driver_id):
    result = count_orders_for_driver_db(driver_id)
    if result:
        return result
    return 'Nothing!'
