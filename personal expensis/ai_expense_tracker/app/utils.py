import pandas as pd
from PyPDF2 import PdfReader
import markdown
from bs4 import BeautifulSoup
from app.database import load_expenses, save_expenses

# Add a single expense
def add_expense(date, category, amount, description):
    expenses = load_expenses()
    expenses.append({
        "date": date,
        "category": category,
        "amount": float(amount),
        "description": description
    })
    save_expenses(expenses)

# Calculate total expenses
def calculate_total():
    expenses = load_expenses()
    return sum(exp["amount"] for exp in expenses)

# Process uploaded file (CSV/PDF/Markdown)
def process_file(file_path, filename):
    # CSV
    if filename.endswith(".csv"):
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            add_expense(row["Date"], row["Category"], row["Amount"], row.get("Description", ""))

    # PDF
    elif filename.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        for line in text.strip().split("\n"):
            parts = line.split(",")
            if len(parts) >= 3:
                date, category, amount = parts[:3]
                description = parts[3] if len(parts) > 3 else ""
                add_expense(date.strip(), category.strip(), float(amount.strip()), description.strip())

    # Markdown
    elif filename.endswith(".md"):
        with open(file_path, "r", encoding="utf-8") as f:
            html = markdown.markdown(f.read())
        soup = BeautifulSoup(html, "html.parser")
        for row in soup.find_all("tr")[1:]:
            cells = [c.get_text() for c in row.find_all(["td","th"])]
            if len(cells) >= 3:
                date, category, amount = cells[:3]
                description = cells[3] if len(cells) > 3 else ""
                add_expense(date.strip(), category.strip(), float(amount.strip()), description.strip())
