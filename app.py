"""
An LLM-powered application vulnerable to prompt injection

This script can be run directly to launch the flask application server.
"""

import re
import zipfile

from flask import Flask, request, redirect
import languagemodels as lm

app = Flask(__name__)

lm.config.use_hf_model("jncraton/Llama-3.2-3B-Instruct-ct2-int8", "5da4ba8")
lm.config["max_tokens"] = 1


# All application state lives in this in-memory dictionary
resumes = {
    "Alice": {"score": "F", "resume": "I'm very smart"},
    "Bob": {"score": "F", "resume": "You should hire me"},
}

# Prompt to guide the LLM used for rating resumes
prompt = """
Respond with only a letter grade for the following CV for a cybersecurity candidate.

A is excellent fit with many cyber certifications and relevant graduate degree(s)
B is potential fit where candidate has a college degree and some experience
C is unlikely fit with degree only and limited experience
D is cannot be hired due to insufficient experience
F is an incomplete or incoherent CV

An excellent CV should have:

- 10+ years of work experience in cybersecurity or related fields
- Graduate work in cybersecurity or a related field
- Several relevant cybersecurity certifications

# CV

Here's the CV:
""".strip()


@app.route("/")
def root():
    return redirect("/apply")


@app.route("/apply")
def resume_get():
    return """
    <html>
    <head>
    <link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    </head>
    <body>
    <main>
    <h1>Apply</h1>
    <p>Thank you for your interest in our open cybersecurity position.</p>
    <p>Please complete the form below to apply for a position.</p>
    <form method=post enctype=multipart/form-data>
      <label>Your Name<input name=name autocomplete=name required /></label>
      <label>Resume<input type=file name=resume required ></input></label>
      <input type=submit value=Apply />
    </form>
    </main>
    </body>
    </html>
    """


@app.route("/apply", methods=["POST"])
def resume_post():
    resume = get_docx_text(request.files["resume"])

    score = generate(f"{prompt}\n\n{resume[:4000]}", choices=list("ABCDF"))

    resumes[request.form["name"]] = {"resume": resume, "score": score}

    return redirect("/thanks")


@app.route("/thanks")
def thanks_get():
    return """
    <html>
    <head>
    <link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    </head>
    <body>
    <main>
    <h1>Thank you</h1>
    <p>Thank you for submitting an application.</p>
    </main>
    </body>
    </html>
    """


@app.route("/applicants")
def applicants():
    applicants = sorted(resumes.items(), key=lambda x: x[1]["score"])

    rows = [
        f"<tr>"
        f"<td><details><summary>{n}</summary><pre>{v['resume']}</pre></details></td>"
        f"<td>Grade {v['score']}</td></tr>"
        for n, v in applicants
    ]
    tbody = "\n".join(rows)

    return f"""
    <html>
    <head>
    <link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    <style>
    pre {{
        overflow: hidden;
        text-overflow: ellipsis;
        max-height: 8rem;
    }}
    </style>
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


def generate(prompt, choices):
    chat_completion = lm.do(prompt)[0]

    if chat_completion not in choices:
        chat_completion = choices[-1]

    return chat_completion


def get_docx_text(file):
    """Extract plain text from docx file"""
    with zipfile.ZipFile(file) as docx:
        text = docx.read("word/document.xml").decode("utf-8")

        text = re.sub(r"<w:p>", "\n\n", text)
        text = re.sub(r"<w:br>", "\n", text)
        text = re.sub(r"<w:cr>", "\n", text)
        text = re.sub(r"<.*?>", "", text)

        text = text.replace("\r\n", "\n")
        text = re.sub(r"\n\n+", "\n\n", text)
        text = re.sub(r"\n[ \t]+", "\n", text)

    return text


app.run()
