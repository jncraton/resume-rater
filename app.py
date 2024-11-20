import time
import re

import zipfile
import languagemodels as lm

from flask import Flask, request, redirect

app = Flask(__name__)

resumes = {
    "Jack": {"score": 1, "resume": "Very smart"},
    "Jill": {"score": 1, "resume": "You should hire me"},
}


@app.route("/")
def root():
    return redirect("/resume")


@app.route("/resume")
def resume_get():
    return f"""
    <html>
    <body>
    <main>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    <form method=post enctype=multipart/form-data>
      <label>Your Name<input name=name autocomplete=name /></label>
      <label>Resume<input type=file name=resume></input></label>
      <input type=submit />
      {resumes}
    </form>
    </main>
    </body>
    </html>
    """


@app.route("/resume", methods=["POST"])
def resume_post():
    name = request.form["name"]

    with zipfile.ZipFile(request.files["resume"]) as docx:
        document_xml = docx.read("word/document.xml").decode("utf-8")

        # Use regex to find all text inside <w:t>...</w:t> tags
        text_elements = re.findall(r"<w:t.*?>(.*?)</w:t>", document_xml, re.DOTALL)

        # Join all text pieces and return as a single string
        resume = "".join(text_elements)

        resume = resume.replace("\r\n", "\n")
        resume = re.sub(r"\n[ \t]+", "\n", resume)
        resume = resume[:4000]

    start = time.perf_counter()
    score = lm.do(
        f"""
Respond with a letter grade for the following CV for a cybersecurity candidate.

A means excellent fit with many certifications and graduate educational experiences
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
        choices=[f"The rating for this CV is {i}." for i in "ABCDF"],
    )

    resumes[name] = {
        "resume": resume,
        "score": score,
        "time": time.perf_counter() - start,
    }

    return redirect("/resume")


@app.route("/applicants")
def applicants():
    applicants = sorted(resumes.items(), key=lambda x: x[1]["score"], reverse=True)

    rows = [
        f"<tr><td><details><summary>{n}</summary>{v['resume']}</details></td><td>{v['score']}</td></tr>"
        for n, v in applicants
    ]
    tbody = "\n".join(rows)

    return f"""
    <html>
    <body>
    <main>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    <table>
    <thead>
    <tr><td>Name</td><td>Score</td></tr>
    </thead>
    <tbody>{tbody}</tbody>
    </table>
    </main>
    </body>
    </html>
    """


app.run()
