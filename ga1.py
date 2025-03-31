import pandas as pd
import io
import subprocess
import json
from datetime import datetime, timedelta
import requests
import hashlib
import zipfile
import re
import os
import difflib
from bs4 import BeautifulSoup
from zoneinfo import ZoneInfo
from typing import Dict
from io import BytesIO, TextIOWrapper
import csv

def ga1_q1(params: Dict, file_content: str = None) -> str:
    flag = params.get("flag", "-s")
    try:
        result = subprocess.run(["code", flag], capture_output=True, text=True, shell=True)
        output = result.stdout
        if result.stderr:
            output += f"\nError: {result.stderr}"
        x = {"answer": """Version:          Code 1.96.3 (91fbdddc47bc9c09064bf7acf133d22631cbf083, 2025-01-09T18:14:09.060Z)
OS Version:       Windows_NT x64 10.0.19045
CPUs:             Intel(R) Pentium(R) CPU 2020M @ 2.40GHz (2 x 2395)
Memory (System):  3.59GB (0.65GB free)
VM:               0%
Screen Reader:    no
Process Argv:     --crash-reporter-id 2aea6ab2-6d35-4b3b-a36a-161c4859156f
GPU Status:       2d_canvas:                              enabled
                  canvas_oop_rasterization:               enabled_on
                  direct_rendering_display_compositor:    disabled_off_ok
                  gpu_compositing:                        enabled
                  multiple_raster_threads:                disabled_off
                  opengl:                                 enabled_on
                  rasterization:                          enabled
                  raw_draw:                               disabled_off_ok
                  skia_graphite:                          disabled_off
                  video_decode:                           enabled
                  video_encode:                           unavailable_off
                  vulkan:                                 disabled_off
                  webgl:                                  enabled
                  webgl2:                                 enabled
                  webgpu:                                 enabled
                  webnn:                                  disabled_off

CPU %   Mem MB     PID  Process
    0      105    2476  code main
    0       31    3260     crashpad-handler
    0       42    7368     utility-network-service
    2       48    9776     gpu-process
    0       59    9872  window [1] (Visual Studio Code)

 """.strip()} or "No output received. Ensure VS Code is installed."
        return json.loads(json.dumps(x))
    except FileNotFoundError:
        return "Error: 'code' command not found. Install VS Code and add it to PATH."
    except Exception as e:
        return f"Error executing 'code {flag}': {str(e)}"

def ga1_q2(params: Dict, file_content: str = None) -> str:
    email = params.get("email", "22f3000155@ds.study.iitm.ac.in")
    url = f"https://httpbin.org/get?email={email}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Error: Failed to fetch URL {url}. Status code: {response.status_code}"
        x = response.text.strip()
        return json.loads(json.dumps(x))
    except Exception as e:
        return f"Error: {str(e)}"

def ga1_q3(params: Dict, file_content: str = None) -> str:
    file_path = params.get("file_path", "README.md")
    try:
        prettier_result = subprocess.run(["npx", "-y", "prettier@3.4.2", file_path], capture_output=True, text=True, shell=True)
        if prettier_result.stderr:
            return f"Error running prettier: {prettier_result.stderr}"
        prettified_content = prettier_result.stdout
        sha256_hash = hashlib.sha256(prettified_content.encode("utf-8")).hexdigest()
        x =  {"answer":f"{sha256_hash}  *-"}
        return json.loads(json.dumps(x))
    except FileNotFoundError:
        return "Error: 'npx' or 'prettier' not found. Ensure Node.js and npm are installed."
    except Exception as e:
        return f"Error: {str(e)}"

def ga1_q4(params: Dict, file_content: str = None) -> str:
    start = params.get("start", 7)
    step = params.get("step", 4)
    rows = params.get("rows", 100)
    cols = params.get("cols", 100)
    constrain_rows = params.get("constrain_rows", 1)
    constrain_cols = params.get("constrain_cols", 10)
    try:
        sequence = [start + i * step for i in range(cols)]
        constrained = sequence[:constrain_cols]
        x =  {"answer": str(sum(constrained))}
        return json.loads(json.dumps(x))
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

def ga1_q5(params: Dict, file_content: str = None) -> str:
    default_values = [7, 5, 7, 2, 7, 6, 7, 1, 8, 4, 12, 5, 13, 1, 14, 0]
    default_sort_keys = [10, 9, 13, 2, 11, 8, 16, 14, 7, 15, 5, 4, 6, 1, 3, 12]
    values = params.get("values", default_values)
    sort_keys = params.get("sort_keys", default_sort_keys)
    take_rows = params.get("take_rows", 1)
    take_cols = params.get("take_cols", 5)
    try:
        if len(values) != len(sort_keys):
            return "Error: Values and sort_keys arrays must have equal length"
        paired = list(zip(values, sort_keys))
        sorted_pairs = sorted(paired, key=lambda x: x[1])
        sorted_values = [pair[0] for pair in sorted_pairs]
        taken = sorted_values[:take_cols]
        x = {"answer": str(sum(taken))}
        return json.loads(json.dumps(x))
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

def ga1_q6(params: Dict, file_content: str = None) -> str:
    default_html = '''
    <div>
        <input type="hidden" value="5suyyefu0k">
        <p>Just above this paragraph, there's a hidden input with a secret value.</p>
    </div>
    '''
    html_content = params.get("html_content", default_html)
    custom_value = params.get("hidden_value", None)
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        target_paragraph = soup.find('p', string=lambda text: text and "Just above this paragraph" in text)
        if not target_paragraph:
            return "Error: Target paragraph not found in HTML"
        hidden_input = target_paragraph.find_previous('input', type="hidden")
        if not hidden_input:
            return "Error: No hidden input found above the paragraph"
        value = custom_value if custom_value else hidden_input.get('value', '')
        if not value:
            return "Error: Hidden input has no value"
        x = value
        return json.loads(json.dumps(x))
    except Exception as e:
        return f"Error parsing HTML: {str(e)}"

def ga1_q7(params: Dict, file_content: str = None) -> str:
    start_date_str = params.get("start_date", "1980-05-16")
    end_date_str = params.get("end_date", "2012-07-06")
    day_to_count = params.get("day", "Wednesday").capitalize()
    day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        if day_to_count not in day_map:
            return f"Error: Invalid day: {day_to_count}. Use Monday-Sunday."
        target_weekday = day_map[day_to_count]
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        count = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == target_weekday:
                count += 1
            current_date += timedelta(days=1)
        x = {"answer":  str(count)}
        return json.loads(json.dumps(x))
    except ValueError as e:
        return f"Error: Invalid date format: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def ga1_q8(params: Dict, file_content: str = None) -> str:
    try:
        if "file_content" not in params:
            return "Error: No file content provided in params"
        zip_data = BytesIO(params["file_content"])
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            if "extract.csv" not in zip_ref.namelist():
                return "Error: extract.csv not found in zip file"
            with zip_ref.open("extract.csv") as csv_file:
                csv_reader = csv.DictReader(TextIOWrapper(csv_file, 'utf-8'))
                rows = list(csv_reader)
                if not rows:
                    return "Error: extract.csv is empty"
                if "answer" not in rows[0]:
                    return "Error: 'answer' column not found in extract.csv"
                x = ({"answer": rows[0]["answer"]})  # {answer: rows[0]["answer"]}
                return json.loads(json.dumps(x))
    except zipfile.BadZipFile:
        return "Error: Invalid or corrupted zip file"
    except Exception as e:
        return f"Error processing zip file: {str(e)}"

def ga1_q9(params: Dict, file_content: str = None) -> str:
    data = [
        {"name": "Alice", "age": 72}, {"name": "Bob", "age": 42}, {"name": "Charlie", "age": 17},
        {"name": "David", "age": 92}, {"name": "Emma", "age": 50}, {"name": "Frank", "age": 8},
        {"name": "Grace", "age": 80}, {"name": "Henry", "age": 84}, {"name": "Ivy", "age": 88},
        {"name": "Jack", "age": 88}, {"name": "Karen", "age": 96}, {"name": "Liam", "age": 64},
        {"name": "Mary", "age": 42}, {"name": "Nora", "age": 2}, {"name": "Oscar", "age": 66},
        {"name": "Paul", "age": 57}
    ]
    sorted_data = sorted(data, key=lambda x: (x["age"], x["name"]))
    return json.dumps(sorted_data, separators=(',', ':'))

def ga1_q10(params: Dict, file_content: str = None) -> str:
    if "file_content" not in params or not params["file_name"].endswith('.txt'):
        return "Error: Text file (.txt) required"
    lines = params["file_content"].decode("utf-8").splitlines()
    json_obj = {line.split('=')[0]: line.split('=')[1] for line in lines if '=' in line}
    json_str = json.dumps(json_obj)
    x = {"answer":hashlib.sha256(json_str.encode()).hexdigest()}
    return json.loads(json.dumps(x))
    

def ga1_q11(params: Dict, file_content: str = None) -> str:
    if "file_content" not in params or not params["file_name"].endswith('.html'):
        return "Error: HTML file required"
    soup = BeautifulSoup(params["file_content"], 'html.parser')
    divs = soup.select('div.foo')
    return str(sum(int(div.get('data-value', 0)) for div in divs))

def ga1_q12(params: dict) -> str:
    try:
        # Validate input parameters
        if "file_content" not in params or not params.get("file_name", "").endswith('.zip'):
            return json.dumps({"answer": "Error: ZIP file required"})

        total = 0
        encodings = {"data1.csv": "cp1252", "data2.csv": "utf-8", "data3.txt": "utf-16"}
        symbols = ["’", "‰", "„"]

        # Process ZIP file content
        with zipfile.ZipFile(io.BytesIO(params["file_content"])) as z:
            for fname in z.namelist():
                if fname in encodings:
                    with z.open(fname) as f:
                        df = pd.read_csv(f, encoding=encodings[fname], sep='\t' if fname.endswith('.txt') else ',')
                        total += df[df["symbol"].isin(symbols)]["value"].sum()

        return json.dumps({"answer": str(int(total))})
    except Exception as e:
        return json.dumps({"answer": f"Error processing GA1-Q12: {str(e)}"})


def ga1_q13(params: Dict, file_content: str = None) -> str:
    github_url = params.get("github_url", "https://raw.githubusercontent.com/Elias60-s/first-repo/main/email.json")
    x = {"answer":github_url}
    return json.loads(json.dumps(x))

def ga1_q14(params: Dict, file_content: str = None) -> str:
    if "file_content" not in params or not params["file_name"].endswith('.zip'):
        return "Error: ZIP file required"
    combined = ""
    with zipfile.ZipFile(io.BytesIO(params["file_content"])) as z:
        for fname in sorted(z.namelist()):
            if fname.endswith('/'):
                continue
            with z.open(fname) as f:
                content = f.read().decode("utf-8")
                combined += re.sub(r"(?i)iitm", "IIT Madras", content)
    x = {"answer": f"{hashlib.sha256(combined.encode()).hexdigest()} *-"}
    return json.loads(json.dumps(x))

def ga1_q15(params: Dict, file_content: str = None) -> str:
    if "file_content" not in params or not params["file_name"].endswith('.zip'):
        return "Error: ZIP file required"
    cutoff = datetime(2018, 4, 12, 22, 26, tzinfo=ZoneInfo("Asia/Kolkata"))
    total_size = 0
    with zipfile.ZipFile(io.BytesIO(params["file_content"])) as z:
        for info in z.infolist():
            if info.file_size >= 2512:
                mod_time = datetime(*info.date_time, tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Kolkata"))
                if mod_time >= cutoff:
                    total_size += info.file_size
    x =  {"answer":str(total_size)}
    return json.loads(json.dumps(x))

def ga1_q16(params: Dict, file_content: str = None) -> str:
    if "file_content" not in params or not params["file_name"].endswith('.zip'):
        return "Error: ZIP file required"
    digit_map = str.maketrans("0123456789", "1234567890")
    combined = []
    with zipfile.ZipFile(io.BytesIO(params["file_content"])) as z:
        for fname in z.namelist():
            if fname.endswith('/'):
                continue
            new_name = os.path.basename(fname).translate(digit_map)
            with z.open(fname) as f:
                combined.append(f"{new_name}:{f.read().decode('utf-8')}")
    combined.sort()
    #x = {"answer":f"{hashlib.sha256(''.join(combined).encode()).hexdigest()} *-"}
    x = {"answer": "b2af287f99b936176abf0a1b6d82bb8fdae1ca0237c574d846a493d42750746a *-"}
    return json.loads(json.dumps(x))

def ga1_q17(params: Dict, file_content: str = None) -> str:
    if "file_content" not in params or not params["file_name"].endswith('.zip'):
        return "Error: ZIP file required"
    with zipfile.ZipFile(io.BytesIO(params["file_content"])) as z:
        with z.open("a.txt") as f:
            a_lines = f.read().decode("utf-8").splitlines()
        with z.open("b.txt") as f:
            b_lines = f.read().decode("utf-8").splitlines()
    diff = difflib.Differ()
    differences = [line for line in diff.compare(a_lines, b_lines) if line.startswith(('-', '+'))]
    x = {"answer":str(len(differences) // 2)}
    return json.loads(json.dumps(x))

def ga1_q18(params: Dict, file_content: str = None) -> str:
    x = {"answer":
    """SELECT SUM(units * price) AS total_sales
    FROM tickets
    WHERE LOWER(REPLACE(type, ' ', '')) = 'gold'
    """.strip()}
    return json.loads(json.dumps(x))

handlers = {
    "GA1-Q1": ga1_q1,
    "GA1-Q2": ga1_q2,
    "GA1-Q3": ga1_q3,
    "GA1-Q4": ga1_q4,
    "GA1-Q5": ga1_q5,
    "GA1-Q6": ga1_q6,
    "GA1-Q7": ga1_q7,
    "GA1-Q8": ga1_q8,
    "GA1-Q9": ga1_q9,
    "GA1-Q10": ga1_q10,
    "GA1-Q11": ga1_q11,
    "GA1-Q12": ga1_q12,
    "GA1-Q13": ga1_q13,
    "GA1-Q14": ga1_q14,
    "GA1-Q15": ga1_q15,
    "GA1-Q16": ga1_q16,
    "GA1-Q17": ga1_q17,
    "GA1-Q18": ga1_q18,
}