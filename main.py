from fastapi import FastAPI, Form, File, UploadFile, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import re
import importlib
import json
import zipfile
from io import BytesIO, TextIOWrapper

app = FastAPI()

# Mount the static directory to serve the HTML file
app.mount("/static", StaticFiles(directory="static"), name="static")

# Import handlers dynamically from ga1.py to ga5.py
handlers = {}
for i in range(1, 6):
    module_name = f"ga{i}"
    try:
        module = importlib.import_module(module_name)
        module_handlers = getattr(module, "handlers", {})
        handlers.update(module_handlers)
        print(f"{module_name.upper()} Handlers: {list(module_handlers.keys())}")
    except ImportError as e:
        print(f"Error importing {module_name}: {e}")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@app.post("/api/")
async def process_question(
    question: str = Form(...),
    params: str = Form(None),
    file: UploadFile = File(None)
):
    question_id_match = re.search(r"GA[1-5]-Q(1[0-8]|[1-9])", question)
    
    # Default to GA1-Q8 if no match found
    question_id = question_id_match.group(0) if question_id_match else "GA1-Q8"

    handler = handlers.get(question_id)
    if not handler:
        return {"answer": f"Error: No handler found for question ID: {question_id}"}

    # Parse params as JSON if provided
    parsed_params = {"question": question}
    if params:
        try:
            parsed_params.update(json.loads(params))
        except json.JSONDecodeError:
            return {"answer": "Error: Invalid JSON format for params"}

    # Read and process file content if uploaded
    file_content = None
    if file:
        parsed_params["file_name"] = file.filename
        file_content = await file.read()
        parsed_params["file_content"] = file_content

    try:
        answer = handler(parsed_params, file_content=file_content)
        return {"answer": str(answer)}
    except Exception as e:
        return {"answer": f"Error processing question: {str(e)}"}

# Upload & Process ZIP File
@app.post("/upload/")
async def upload_and_process(file: UploadFile = File(...)):
    try:
        # Read uploaded file content
        file_content = await file.read()
        
        # Check if uploaded file is a ZIP file
        if not file.filename.lower().endswith(".zip"):
            return {"error": "Only ZIP files are allowed"}
        
        # Open ZIP file
        zip_data = BytesIO(file_content)
        with zipfile.ZipFile(zip_data, "r") as zip_ref:
            
            # Check if "extract.csv" is present
            if "extract.csv" not in zip_ref.namelist():
                return {"error": "extract.csv not found in ZIP file"}
            
            # Open and read extract.csv
            with zip_ref.open("extract.csv") as csv_file:
                csv_reader = csv.DictReader(TextIOWrapper(csv_file, "utf-8"))
                rows = list(csv_reader)
                
                # Check if CSV has data
                if not rows:
                    return {"error": "extract.csv is empty"}
                
                # Ensure "answer" column exists
                if "answer" not in rows[0]:
                    return {"error": "'answer' column not found in extract.csv"}
                
                return {"answer": rows[0]["answer"]}

    except Exception as e:
        return {"error": str(e)}

# Function Handlers
def get_ticket_status(ticket_id: int):
    return f"Status of ticket {ticket_id}"

def schedule_meeting(date: str, time: str, meeting_room: str):
    return f"Meeting scheduled on {date} at {time} in {meeting_room}"

def get_expense_balance(employee_id: int):
    return f"Expense balance for employee {employee_id}"

def calculate_performance_bonus(employee_id: int, current_year: int):
    return f"Performance bonus for employee {employee_id} in {current_year}"

def report_office_issue(issue_code: int, department: str):
    return f"Office issue {issue_code} reported for {department}"

# Execute Query API
@app.get("/execute")
async def execute(q: str):
    if not q:
        raise HTTPException(status_code=400, detail="Error: 'query' parameter required")

    query = q.strip()

    # Regex patterns
    patterns = {
        "get_ticket_status": r"What is the status of ticket (\d+)\?",
        "schedule_meeting": r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (Room [A-Z])\.",
        "get_expense_balance": r"Show my expense balance for employee (\d+)\.",
        "calculate_performance_bonus": r"Calculate performance bonus for employee (\d+) for (\d{4})\.",
        "report_office_issue": r"Report office issue (\d+) for the (\w+) department\."
    }

    # Match query
    for function_name, pattern in patterns.items():
        match = re.match(pattern, query)
        if match:
            args = match.groups()
            return {
                "name": function_name,
                "arguments": json.dumps(dict(zip(pattern.split(r"\(", 1)[1].split(r"\)", 1)[0].split(r"\|"), args)))
            }

    raise HTTPException(status_code=400, detail="Error: Invalid query")
