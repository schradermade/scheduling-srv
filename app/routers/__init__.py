from .todo import router as TodoRouter
from .auth import router as AuthRouter
from .admin import router as AdminRouter
from .users import router as UserRouter

__all__ = ['TodoRouter', 'AuthRouter', 'AdminRouter', 'UserRouter']
