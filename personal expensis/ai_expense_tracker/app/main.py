import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.utils import add_expense, load_expenses, calculate_total, process_file

# 1️⃣ Create FastAPI app
app = FastAPI()

# 2️⃣ Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3️⃣ Templates directory
templates = Jinja2Templates(directory="templates")

# 4️⃣ Ensure upload folder exists
os.makedirs("uploads", exist_ok=True)

# 5️⃣ Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    expenses = load_expenses()
    return templates.TemplateResponse("index.html", {"request": request, "expenses": expenses})

@app.post("/add_expense", response_class=HTMLResponse)
async def add_expense_route(
    request: Request,
    date: str = Form(...),
    category: str = Form(...),
    amount: float = Form(...),
    description: str = Form("")
):
    add_expense(date, category, amount, description)
    expenses = load_expenses()
    return templates.TemplateResponse("index.html", {"request": request, "expenses": expenses})

@app.get("/total", response_class=HTMLResponse)
async def total(request: Request):
    total_amount = calculate_total()
    return templates.TemplateResponse("total.html", {"request": request, "total": total_amount})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    process_file(file_path, file.filename)
    expenses = load_expenses()
    return templates.TemplateResponse("index.html", {"request": request, "expenses": expenses})
