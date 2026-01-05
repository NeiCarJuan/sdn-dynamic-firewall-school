from .status import router as status_router
from .firewall import router as firewall_router   

def register_routes(app):
    app.include_router(
        status_router,
        prefix="/status",
        tags=["Status"]
    )

    app.include_router(
        firewall_router,
        prefix="/firewall",
        tags=["Firewall"]
    )  

