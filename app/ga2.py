import io
import json
import hashlib
from datetime import datetime
from PIL import Image
import numpy as np
import colorsys
import pandas as pd
from typing import Dict

def ga2_q1(params: Dict, file_content: str = None) -> str:
    x =  {"answer": """# Weekly Step Analysis

## Introduction

Tracking steps is a **crucial** part of understanding our daily activity levels. This analysis provides insights into my step count over a week and compares it with friends to observe trends and evaluate performance.

---

## Methodology

1. Data was collected using a fitness tracker.
2. Daily step counts were recorded and averaged.
3. A Python script analyzed trends over time and relative performance with friends.

Inline example: The Python function `analyze_steps(data)` was pivotal in calculating averages and comparisons.

---

**Results**

*Daily Steps*

- *Key Highlights*:
  - Highest steps recorded on Friday.
  - Steady improvement over the week.
  - Sunday was the least active day.

### Comparison with Friends

- Outperformed Friend A in step count for 4 days.
- Lagged behind Friend B consistently (*note*: they have a more active routine).

---

```python
# Python script to analyze steps
def analyze_steps(data):
    daily_average = sum(data) / len(data)
    print(f"Average steps: {daily_average}")
```
 
- Item
1. Step One
   
**Sample_code**  
#### Table of Daily Steps

| Day       | My Steps | Friend A | Friend B |
|-----------|----------|----------|----------|
| Monday    | 6,500    | 5,800    | 7,200    |
| Tuesday   | 7,100    | 6,200    | 7,500    |
| Wednesday | 7,800    | 7,000    | 8,000    |
| Thursday  | 8,000    | 6,500    | 8,300    |
| Friday    | 9,500    | 7,800    | 10,000   |
| Saturday  | 8,300    | 7,200    | 9,800    |
| Sunday    | 5,400    | 5,900    | 6,500    |

[Hyperlink](https://example.com)

![Image](https://example.com/image.jpg)

> "The journey of a thousand miles begins with a single step." """}

    return json.dumps(x)

def ga2_q2(params: Dict, file_content: str = None) -> str:
    """
    Q2: Images: Compression
    Compress an image losslessly to less than 1,500 bytes.
    If the input image is already under 1,500 bytes, it will still attempt lossless compression.
    """
    if "file_content" not in params:
        return "Error: Image file required"
    
    try:
        # Check the size of the input image
        input_size = len(params["file_content"])
        if input_size < 1500:
            # Even if the input is under 1,500 bytes, we compress it to ensure WebP format
            pass  # Proceed with compression as per the question's requirement
        
        # Open and compress the image
        img = Image.open(io.BytesIO(params["file_content"]))
        output = io.BytesIO()
        img.save(output, format="WEBP", lossless=True)
        compressed_size = output.tell()
        
        if compressed_size >= 1500:
            return f"Error: Compressed size {compressed_size} bytes exceeds 1,500 bytes (input size was {input_size} bytes)"
        return str(compressed_size)
    except Exception as e:
        return f"Error: {str(e)}"
    
def ga2_q3(params: Dict, file_content: str = None) -> str:
    x = {"answer": params.get("github_pages_url", "https://elias60-s.github.io/push-email/")}
    return json.loads(json.dumps(x))

def ga2_q4(params: Dict, file_content: str = None) -> str:
    email = params.get("email", "22f3000155@ds.study.iitm.ac.in")
    year = datetime.now().year
    x = {"answer": hashlib.sha256(f"{email} {year}".encode()).hexdigest()[-5:]}
    return json.loads(json.dumps(x))

def ga2_q5(params: Dict, file_content: str = None) -> str:
    if "file_content" not in params:
        return "Error: Image file required"
    try:
        img = Image.open(io.BytesIO(params["file_content"]))
        rgb = np.array(img) / 255.0
        lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
        x = {"answer":str(int(np.sum(lightness > 0.757)))}
        return json.loads(json.dumps(x))
    except Exception as e:
        return f"Error: {str(e)}"

def ga2_q6(params: Dict, file_content: str = None) -> str:
    """
    Q6: Serverless hosting: Vercel
    Returns the Vercel URL.
    """
    x = {"answer":params.get("vercel_url", "https://vercel-api-y2nk.vercel.app/api")}
    return json.loads(json.dumps(x))

def ga2_q7(params: Dict, file_content: str = None) -> str:
    x = {"answer":params.get("repo_url", "https://github.com/Elias60-s/firstsite.github.io")}
    return json.loads(json.dumps(x))

def ga2_q8(params: Dict, file_content: str = None) -> str:
    x = {"answer": params.get("docker_url", "https://hub.docker.com/repository/docker/elias60/py-hello/general")}
    return json.loads(json.dumps(x))

def ga2_q9(params: Dict, file_content: str = None) -> str:
    if "file_content" not in params or not params["file_name"].endswith('.csv'):
        return "Error: q-fastapi.csv file required"
    try:
        df = pd.read_csv(io.BytesIO(params["file_content"]))
        students = [{"studentId": row["studentId"], "class": row["class"]} for _, row in df.iterrows()]
        classes = params.get("classes", [])
        if isinstance(classes, str):
            classes = [classes]
        elif not isinstance(classes, list):
            classes = []
        if classes:
            students = [s for s in students if s["class"] in classes]
        return json.dumps({"url": params.get("api_url", "http://127.0.0.1:8000/api"), "students": students})
    except Exception as e:
        return f"Error: {str(e)}"

def ga2_q10(params: Dict, file_content: str = None) -> str:
    # if "file_content" not in params:
    #     return "Error: Llama file required"
    # try:
    #     img = Image.open(io.BytesIO(params["file_content"]))
        # x = {"answer":({"url": params.get("ngrok_url", "https://9826-152-59-153-64.ngrok-free.app/"), "size": len(params["file_content"])})}
        # return json.loads(json.dumps(x))
        x = {"answer":"https://9826-152-59-153-64.ngrok-free.app/"}
        return json.loads(json.dumps(x))
    # except Exception as e:
    #     return f"Error: {str(e)}"

handlers = {
    "GA2-Q1": ga2_q1,
    "GA2-Q2": ga2_q2,
    "GA2-Q3": ga2_q3,
    "GA2-Q4": ga2_q4,
    "GA2-Q5": ga2_q5,
    "GA2-Q6": ga2_q6,
    "GA2-Q7": ga2_q7,
    "GA2-Q8": ga2_q8,
    "GA2-Q9": ga2_q9,
    "GA2-Q10": ga2_q10,

}