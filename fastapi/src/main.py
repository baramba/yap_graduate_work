import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import views
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(views.router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
