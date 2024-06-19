from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, select
from database import Base


# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Идентификатор пользователя
    username = Column(String, unique=True)  # Имя пользователя, уникальное
    fio = Column(String)  # Полное имя пользователя
    phone_number = Column(String, unique=True)  # Номер телефона, уникальный
    age = Column(Integer)  # Возраст
    gender = Column(String, default='None')  # Пол, по умолчанию 'None'
    region = Column(String)  # Регион проживания
    order_count = Column(Integer, default=0)  # Количество заказов
    frequent_tariff = Column(String)
    created_at = Column(DateTime, default=datetime.now)  # Дата и время создания записи

    # Связь один-ко-многим с таблицей заказов
    orders = relationship('Order', back_populates='user')


# Модель для таблицы водителей
class Driver(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Идентификатор водителя
    name = Column(String(50))  # Имя
    surname = Column(String(50))  # Фамилия
    middle_name = Column(String(50))  # Отчество
    age = Column(Integer)  # Возраст
    phone_number = Column(String(15), unique=True, index=True)  # Номер телефона, уникальный
    gender = Column(String(10), default='None')  # Пол, по умолчанию 'None'
    rating = Column(Float, default=0.0)  # Рейтинг, по умолчанию 0.0
    license_number = Column(String(20), unique=True)  # Номер водительского удостоверения, уникальный
    car_plate = Column(String, unique=True)  # Номерной знак автомобиля, уникальный
    car_model = Column(String)  # Модель автомобиля
    status = Column(String)  # Статус
    income = Column(Float, default=0.0)  # Доход
    tariff_id = Column(Integer, ForeignKey('tariffs.id'))  # Ссылка на тариф
    created_at = Column(DateTime, default=datetime.now)  # Дата и время создания записи

    # Связь один-ко-многим с таблицей тарифов
    tariff = relationship('Tariff', back_populates='drivers')
    # Связь один-ко-многим с таблицей заказов
    orders = relationship('Order', back_populates='driver')


# Модель для таблицы заказов
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Идентификатор заказа
    user_id = Column(Integer, ForeignKey('users.id'))  # Ссылка на пользователя
    driver_id = Column(Integer, ForeignKey('drivers.id'))  # Ссылка на водителя
    tariff_id = Column(Integer, ForeignKey('tariffs.id'))  # Ссылка на тариф
    start_location = Column(String(255))  # Начальное местоположение
    end_location = Column(String(255))  # Конечное местоположение
    distance = Column(Float)  # Расстояние
    price = Column(Float)  # Цена
    created_at = Column(DateTime, default=datetime.now)  # Дата и время создания записи

    # Связь один-ко-многим с таблицей пользователей
    user = relationship('User', back_populates='orders')
    # Связь один-ко-многим с таблицей водителей
    driver = relationship('Driver', back_populates='orders')
    # Связь один-ко-многим с таблицей тарифов
    tariff = relationship('Tariff', back_populates='orders')


# Модель для таблицы тарифов
class Tariff(Base):
    __tablename__ = 'tariffs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Идентификатор тарифа
    name = Column(String(50), unique=True)  # Название тарифа, уникальное
    created_at = Column(DateTime, default=datetime.now)  # Дата и время создания записи

    # Связь один-ко-многим с таблицей заказов
    orders = relationship('Order', back_populates='tariff')
    # Связь один-ко-многим с таблицей водителей
    drivers = relationship('Driver', back_populates='tariff')

    # Гибридное свойство для подсчета количества заказов по данному тарифу
    @hybrid_property
    def order_count(self):
        return len(self.orders)

    @order_count.expression
    def order_count(cls):
        return (
            select([func.count(Order.id)])
            .where(Order.tariff_id == cls.id)
            .label('order_count')
        )


class UsedIds(Base):
    __tablename__ = 'used_ids'
    id = Column(Integer, primary_key=True, autoincrement=False)
    used = Column(Boolean, default=True)
