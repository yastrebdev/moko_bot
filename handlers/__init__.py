from .commands import router as commands_router
from .callbacks import router as callbacks_router
from .messages import router as messages_router

routers = [
    commands_router,
    callbacks_router,
    messages_router
]