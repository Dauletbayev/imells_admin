from fastapi import APIRouter, HTTPException
from database.orderservice import *

orders_router = APIRouter(tags=['Управление заказами'], prefix='/orders')


# Создание нового заказа
@orders_router.post('/api/make_order')
async def make_order(
        user_id: int,
        driver_id: int,
        tariff_id: int,
        start_location: str,
        end_location: str,
        distance: float,
        price: float
):
    result = make_order_db(
        user_id=user_id,
        driver_id=driver_id,
        tariff_id=tariff_id,
        start_location=start_location,
        end_location=end_location,
        distance=distance,
        price=price
    )

    if result:
        return {'message': result}
    raise HTTPException(status_code=400, detail='Error making order')


# Поиск заказов по заданному запросу
@orders_router.post('/api/search_order')
async def search_order(query: str):
    result = search_order_db(query)
    if result:
        return result
    raise HTTPException(status_code=404, detail='No matching orders found')


# Получение списка всех заказов
@orders_router.get('/api/get_all_orders')
async def get_all_orders():
    return get_all_orders_db()


# Получение детальной информации о заказе
@orders_router.get('/api/get_detailed_order')
async def get_detailed_order(order_id: int):
    result = get_detailed_order_db(order_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail='Order not found')


# Получение общего количества заказов
@orders_router.get('/api/get_all_orders_count')
async def get_all_orders_count():
    return get_all_orders_count_db()


# Получение статистики по заказам
@orders_router.get('/api/get_statistics')
async def get_statistics():
    return get_statistics_db()


@orders_router.get('/api/count_orders_last_7_months')
async def count_orders_last_7_months():
    result = count_orders_last_7_months_db()
    if result:
        return result
    return 'Orders not found!'


# Удаление заказа по его ID
@orders_router.delete('/api/delete_order')
async def delete_order(order_id):
    result = delete_order_db(order_id)
    if result:
        return result
    return 'Error!'

