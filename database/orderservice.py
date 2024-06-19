from collections import defaultdict
from .models import Order, Driver, User
from datetime import datetime, timedelta
from database import get_db
from sqlalchemy.sql import func, and_
from sqlalchemy import update


# Создание нового заказа
def make_order_db(
        user_id: int,
        driver_id: int,
        tariff_id: int,
        start_location: str,
        end_location: str,
        distance: float,
        price: float
):
    db = next(get_db())
    new_order = Order(
        user_id=user_id,
        driver_id=driver_id,
        tariff_id=tariff_id,
        start_location=start_location,
        end_location=end_location,
        distance=distance,
        price=price,
        created_at=datetime.now()
    )

    db.add(new_order)

    update_driver_income(driver_id, price)

    update_order_count_for_user(user_id)

    db.commit()
    return 'Order accepted!'


# Получение списка всех заказов
def get_all_orders_db():
    db = next(get_db())
    orders = db.query(Order).all()
    return orders


# Получение детальной информации о заказе по ID
def get_detailed_order_db(order_id: int):
    db = next(get_db())
    order = db.query(Order).filter_by(id=order_id).first()
    return order


# Поиск заказов по строковому запросу
def search_order_db(query: str):
    db = next(get_db())
    orders = db.query(Order).filter(
        (Order.start_location.like(f"%{query}%")) |
        (Order.end_location.like(f"%{query}%")) |
        (Order.price.like(f"%{query}%"))
    ).all()
    return orders


# Получение общего количества заказов
def get_all_orders_count_db():
    db = next(get_db())
    return db.query(func.count(Order.id)).scalar()


# Получение статистики по заказам
def get_statistics_db():
    db = next(get_db())

    # Получаем общее количество заказов
    total_orders = db.query(func.count(Order.id)).scalar()

    # Получаем количество заказов за вчерашний день
    yesterday_orders = get_yesterday_order_count()

    # Рассчитываем процент роста
    if yesterday_orders == 0:
        growth_percentage = 100.0
    else:
        growth_percentage = ((total_orders - yesterday_orders) / yesterday_orders) * 100

    return {
        "total_orders": total_orders,
        "growth_percentage": growth_percentage
    }


# Получение количества заказов за вчерашний день
def get_yesterday_order_count():
    db = next(get_db())
    yesterday_orders = db.query(func.count(Order.id)).filter(Order.created_at < func.now() - timedelta(days=1)).scalar()
    return yesterday_orders


# Удаление заказа по его ID
def delete_order_db(order_id: int):
    db = next(get_db())
    order = db.query(Order).filter_by(id=order_id).first()
    db.delete(order)
    db.commit()
    return 'Good!'


def count_orders_last_7_months_db() -> dict:
    db = next(get_db())
    now = datetime.now()

    # Create a dictionary to store the count of orders for each month
    orders_by_month = defaultdict(int)

    # Iterate over the last 7 months
    for i in range(6, -1, -1):
        start_date = now - timedelta(days=30 * (i + 1))  # Approximation of the start of the month
        end_date = now - timedelta(days=30 * i)  # Approximation of the end of the month

        # Execute a query to count the orders registered in this month
        count = db.query(func.count(Order.id)).filter(
            and_(
                Order.created_at >= start_date,
                Order.created_at < end_date
            )
        ).scalar()

        # Get the name of the month
        month_name = start_date.strftime("%B")

        # Add the count of orders to the dictionary
        orders_by_month[month_name] = count

    return orders_by_month


def update_driver_income(driver_id, price):
    db = next(get_db())
    # Выполняем запрос на обновление дохода водителя
    stmt = update(Driver).where(Driver.id == driver_id).values(income=Driver.income + price)
    db.execute(stmt)
    db.commit()


def update_order_count_for_user(user_id):
    db = next(get_db())
    # Выполняем запрос для подсчета общего количества заказов пользователя
    order_count = db.query(func.count(Order.id)).filter(Order.user_id == user_id).scalar()

    # Обновляем значение order_count для данного пользователя
    db.query(User).filter(User.id == user_id).update({"order_count": order_count})

    db.commit()
