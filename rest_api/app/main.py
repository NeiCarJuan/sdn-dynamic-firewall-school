from fastapi import FastAPI
from app.api import register_routes

app = FastAPI(
    title="SDN Dynamic Firewall REST API",
    version="0.1"
)

register_routes(app)
