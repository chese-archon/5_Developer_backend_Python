from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import datetime
from database import save_device_data, get_all_data, analyze_device_data

app = FastAPI()
templates = Jinja2Templates(directory="templates")
class UserInput(BaseModel):
    deviceId: str
    x: float
    y: float
    z: float


# Для анализа статистики
class Data_analys(BaseModel):
    type: str = "specific"
    deviceId: str = None


fake_db = {}

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.post("/add_user")
async def add_user(user_input: UserInput):
    timestamp = str(datetime.datetime.now())
    user_data = {"x": user_input.x, "y": user_input.y, "z": user_input.z,
                 "data": timestamp,
                 "device_Id": user_input.deviceId}
    save_device_data(user_input.deviceId, user_input.x, user_input.y, user_input.z)
    return {"message": f"Получены данные {user_data}"}

@app.get('/all_data')
async def get_all_users():
    return json.dumps(get_all_data())

@app.get('/analys', response_class=HTMLResponse)
async def get_all_users(request: Request):
    return templates.TemplateResponse("analys.html", {"request": request})

@app.post('/analys_statistic')
async def analys_statistic(answ: Data_analys):
    if answ.type != 'all':
        return {"message": f"Получены данные {answ.deviceId}: {analyze_device_data(answ.deviceId)}"}
    else:
        return {"message": f"Получены данные {analyze_device_data(answ.type)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)