from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from shuffle import shuffle, sync


async def lifespan(app):
    await call_sync()
    await call_shuffle()
    yield

app = FastAPI(lifespan=lifespan)

@repeat_every(seconds=86400)  # 24 hours
async def call_shuffle():
    shuffle()

@repeat_every(seconds=60)
async def call_sync():
    sync()
