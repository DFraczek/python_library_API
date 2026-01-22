import pathlib
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent.parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

router = APIRouter()

@router.get("/monitor", response_class=HTMLResponse)
async def get_monitor(request: Request):
    """
    Endpoint zwracający stronę HTML do monitoringu serwera.
    """
    return templates.TemplateResponse("monitor.html", {"request": request})