from collections import defaultdict
from .models import User, Order, Tariff, UsedIds
from datetime import datetime, timedelta
from database import get_db
from sqlalchemy.sql import func, and_


def register_user_db(
        username: str,
        fio: str,
        phone_number: str,
        age: int,
        gender: str,
        region: str
):
    db = next(get_db())

    existing_user = db.query(User).filter_by(phone_number=phone_number).first()
    if existing_user:
        return "User with this phone number already exists"

    # Определить следующий доступный идентификатор
    next_id = db.query(User.id).order_by(User.id.desc()).first()
    next_id = next_id[0] + 1 if next_id else 1

    # Проверить, не был ли этот идентификатор использован ранее
    while db.query(UsedIds).filter_by(id=next_id).first():
        next_id += 1

    new_user = User(
        id=next_id,
        username=username,
        fio=fio,
        phone_number=phone_number,
        age=age,
        gender=gender,
        region=region,
        created_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "User successfully registered"



# Удаление пользователя по ID
def delete_user_db(user_id: int):
    db = next(get_db())
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


# Просмотр списка всех пользователей
def get_all_users_db():
    db = next(get_db())
    users = db.query(User).all()
    return users


# Просмотр детальной информации о пользователе по ID
def get_detailed_user_db(user_id: int):
    db = next(get_db())
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        return user
    return None


# Поиск пользователей по строковому запросу
def search_user_db(query: str):
    db = next(get_db())
    users = db.query(User).filter(
        (User.username.like(f"%{query}%")) |
        (User.fio.like(f"%{query}%")) |
        (User.phone_number.like(f"%{query}%"))
    ).all()
    return users


# Получение статистики по пользователям
def get_statistics_db():
    db = next(get_db())

    # Получаем общее количество пользователей
    total_users = db.query(func.count(User.id)).scalar()

    # Получаем количество пользователей за вчерашний день
    yesterday_users = get_yesterday_user_count()

    # Рассчитываем процент роста
    if yesterday_users == 0:
        growth_percentage = 100.0
    else:
        growth_percentage = ((total_users - yesterday_users) / yesterday_users) * 100

    return {
        "total_users": total_users,
        "growth_percentage": growth_percentage
    }


# Получение количества пользователей за вчерашний день
def get_yesterday_user_count():
    db = next(get_db())
    yesterday_users = db.query(func.count(User.id)).filter(User.created_at < func.now() - timedelta(days=1)).scalar()
    return yesterday_users


# Получение общего количества пользователей
def get_users_count_db():
    db = next(get_db())
    return db.query(func.count(User.id)).scalar()


def count_users_registered_in_last_7_months_db() -> dict:
    db = next(get_db())
    now = datetime.now()

    # Создаем словарь для хранения количества пользователей для каждого месяца
    users_by_month = defaultdict(int)

    # Итерируемся по последним 7 месяцам
    for i in range(7):
        start_date = now - timedelta(days=30 * (i + 1))  # Грубое приближение начала месяца
        end_date = now - timedelta(days=30 * i)  # Грубое приближение конца месяца

        # Выполняем запрос в базу данных, чтобы подсчитать количество пользователей, зарегистрированных в этом месяце
        count = db.query(func.count(User.id)).filter(
            and_(
                User.created_at >= start_date,
                User.created_at < end_date
            )
        ).scalar()

        # Получаем название месяца
        month_name = start_date.strftime("%B")

        # Добавляем количество пользователей в словарь
        users_by_month[month_name] = count

    return users_by_month


def find_most_frequent_tariff_for_user_db(user_id):
    db = next(get_db())

    # Выполняем запрос для подсчета количества заказов для каждого тарифа пользователя
    query_result = db.query(Order.tariff_id, func.count(Order.id)).filter(Order.user_id == user_id).group_by(
        Order.tariff_id).all()

    # Создаем словарь, где ключами будут ID тарифов, а значениями - количество заказов
    tariff_counts = {tariff_id: count for tariff_id, count in query_result}

    # Проверяем, что tariff_counts не пустой
    if tariff_counts:
        # Находим тариф с наибольшим количеством заказов
        most_frequent_tariff_id = max(tariff_counts, key=tariff_counts.get)

        # Получаем название часто используемого тарифа
        most_frequent_tariff = db.query(Tariff.name).filter(Tariff.id == most_frequent_tariff_id).scalar()

        return most_frequent_tariff
    else:
        return None  # Возвращаем None, если список тарифов пустой


