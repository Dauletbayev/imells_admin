from fastapi import APIRouter, HTTPException
from database.tariffservice import *

tariffs_router = APIRouter(tags=['Управление тарифами'], prefix='/tariffs')


# Добавление нового тарифа
@tariffs_router.post('/api/add_tariff')
async def add_tariff(name: str):
    result = add_tariff_db(name)
    if result:
        return {'message': result}
    raise HTTPException(status_code=400, detail='Error adding tariff')


# Поиск тарифов по заданному запросу
@tariffs_router.post('/api/search_tariff')
async def search_tariff(query: str):
    result = search_tariff_db(query.capitalize())
    if result:
        return result
    raise HTTPException(status_code=404, detail='No matching tariffs found')


# Получение списка всех тарифов
@tariffs_router.get('/api/get_all_tariffs')
async def get_all_tariffs():
    return get_all_tariffs_db()


# Получение детальной информации о тарифе
@tariffs_router.get('/api/get_detailed_tariff')
async def get_detailed_tariff(tariff_id: int):
    result = get_detailed_tariff_db(tariff_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail='Tariff not found')


# Получение заказов, связанных с указанным тарифом
@tariffs_router.get('/api/get_orders_of_this_tariff')
async def get_orders_of_this_tariff(tariff_id: int):
    result = get_orders_of_this_tariff_db(tariff_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail='No orders found for this tariff')


# Удаление тарифа по его ID
@tariffs_router.delete('/api/delete_tariff')
async def delete_tariff(tariff_id):
    result = delete_tariff_db(tariff_id)
    if result:
        return result
    return 'Error!'

