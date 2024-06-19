from fastapi import FastAPI
from database import Base, engine
from api.users_api.users import users_router
from api.drivers_api.drivers import drivers_router
from api.tariffs_api.tariffs import tariffs_router
from api.orders_api.orders import orders_router

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/', title='IGo')


app.include_router(users_router)
app.include_router(drivers_router)
app.include_router(tariffs_router)
app.include_router(orders_router)
