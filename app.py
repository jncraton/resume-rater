import time
import re
import requests
import json
import os
import zipfile

from flask import Flask, request, redirect

app = Flask(__name__)

def generate(prompt, choices):
    response = requests.post(
        f"http://{os.environ.get('VLLM_HOST')}:{os.environ.get('VLLM_PORT')}/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "model": "hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 2
        })
    )

    if response.status_code == 200:
        response_data = response.json()
    else:
        print("Error:", response.status_code, response.text)
        return choices[-1]

    chat_completion = response_data["choices"][0]["message"]["content"]

    if chat_completion not in choices:
        chat_completion = choices[-1]

    return chat_completion

resumes = {
    "Jack B": {"score": "F", "resume": "I'm very smart"},
    "Jill S": {"score": "F", "resume": "You should hire me"},
}


@app.route("/")
def root():
    return redirect("/apply")


@app.route("/apply")
def resume_get():
    return f"""
    <html>
    <head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    </head>
    <body>
    <main>
    <h1>Apply</h1>
    <p>Thank you for your interest in our open cybersecurity position. Please complete the form below to apply for a position.</p>
    <form method=post enctype=multipart/form-data>
      <label>Your Name<input name=name autocomplete=name /></label>
      <label>Resume<input type=file name=resume></input></label>
      <input type=submit value=Apply />
    </form>
    </main>
    </body>
    </html>
    """


@app.route("/apply", methods=["POST"])
def resume_post():
    name = request.form["name"]

    if not name.strip():
        return redirect("/apply")

    # Quick hack to extract text from docx
    with zipfile.ZipFile(request.files["resume"]) as docx:
        document_xml = docx.read("word/document.xml").decode("utf-8")

        resume = document_xml
        resume = re.sub(r"<w:p>", "\n\n", resume)
        resume = re.sub(r"<w:br>", "\n", resume)
        resume = re.sub(r"<w:cr>", "\n", resume)
        resume = re.sub(r"<.*?>", "", resume)

        resume = resume.replace("\r\n", "\n")
        resume = re.sub(r"\n\n+", "\n\n", resume)
        resume = re.sub(r"\n[ \t]+", "\n", resume)
        resume = resume[:4000]

    start = time.perf_counter()
    score = generate(
        f"""
Respond with only a single letter grade for the following CV for a cybersecurity candidate.

A means excellent fit with many relevant certifications and at least one relevant graduate degree
B means potential fit where candidate has a college degree and some experience
C means unlikely fit with degree only and limited experience
D means cannot be hired due to insufficient experience
F means an incomplete or incoherent CV

An excellent CV should have:

- 10+ years of work experience in cybersecurity or related fields
- Graduate work in cybersecurity or a related field
- Several relevant cybersecurity certifications

# CV

Here's the CV:

{resume}""".strip(),
        choices=[f"{i}" for i in "ABCDF"],
    )

    resumes[name] = {
        "resume": resume,
        "score": score,
        "time": time.perf_counter() - start,
    }

    return redirect("/apply")


@app.route("/applicants")
def applicants():
    applicants = sorted(resumes.items(), key=lambda x: x[1]["score"])

    rows = [
        f"<tr><td><details><summary>{n}</summary><pre>{v['resume']}</pre></details></td><td>{v['score']}</td></tr>"
        for n, v in applicants
    ]
    tbody = "\n".join(rows)

    return f"""
    <html>
    <head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    </head>
    <body>
    <main>
    <h1>Applicants</h1>
    <table>
    <thead>
    <tr><td>Name</td><td>AI ResumeRating™</td></tr>
    </thead>
    <tbody>{tbody}</tbody>
    </table>
    </main>
    </body>
    </html>
    """

@app.route("/clear-applicants")
def clear_applicants():
    global resumes
    resumes = {}
    return redirect("/applicants")

app.run()
