from uvicorn import run

from insight_python.app import app
from insight_python.settings import settings

if __name__ == "__main__":
    if settings.FASTAPI_PRODUCTION:
        run(app, host="0.0.0.0", port=80, reload=False)
    else:
        run(
            "insight_python.app:app",
            host="0.0.0.0",
            port=9999,
            reload=True,
            reload_dirs=["insight_python"],
        )
