from app.core.app import init_app
from app.core.settings import Settings

settings = Settings()
app = init_app(settings)
