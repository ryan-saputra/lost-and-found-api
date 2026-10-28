
from fastapi import FastAPI

from lost_and_found.database import Base, engine
from lost_and_found.models.item import ItemReport
from lost_and_found.routers.item_router import router as item_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lost and Found Management API",
    description="API untuk pelaporan dan pencarian barang hilang dan temuan.",
    version="1.0.0",
)


app.include_router(item_router)


@app.get("/")
def read_root():
    return {
        "message": "Lost and Found Management API berjalan",
        "status": "success",
    }
