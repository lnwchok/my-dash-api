from datetime import date, datetime
import calendar
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

def getToday():
    currentDate = datetime.now()
    year = currentDate.year
    month = currentDate.month
    day = currentDate.day
    return year, month, day

def getCalendarInfo(year: int, month: int, day: int):
    firstDay = date(year,month, day=1).isoweekday()
    lastDayOfMonth = calendar.monthrange(year, month)[1]
    return firstDay, lastDayOfMonth, day, month, year

def toCalendar(year: int, month: int, day: int):
    (firstDay, totalDay, d, m, y) = getCalendarInfo(year, month, day)
    return {
        'year': y,
        'month': m,
        'currentDay' : d,
        'firstDay': firstDay, 
        'totalDay': totalDay}

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/calendar", response_class=HTMLResponse)
async def main(request: Request):
    (year, month, day) = getToday()
    context = {'request': request, 
               'status': 'Nice!!!', 
               'calendar': toCalendar(year, month, day)
               }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.get("/calendar/{year}/{month}", response_class=HTMLResponse)
async def getMonth(request: Request, month: int, year: int):
    context = {'request': request, 
               'status': 'Nice!!!', 
               'calendar': toCalendar(year, month, 1)
               }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.get("/api/status")
async def getStatus():
    return {'status': 'Nice!!!'}