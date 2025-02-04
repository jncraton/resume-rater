# Resume Rater

An LLM application vulnerable to [prompt injection](https://en.wikipedia.org/wiki/Prompt_injection)

Learning Objectives
-------------------

After exploring and exploiting this application, learners will be able to:

- Analyze an LLM powered web application to identify potential security vulnerabilities
- Describe prompt injection vulnerabilities
- Explore source code to identify areas of weakness
- Change the behavior of an LLM with access to only part of its prompt

Interface
---------

Applicants upload resumes in `.docx` format using the root endpoint:

![Upload screenshot](https://github.com/user-attachments/assets/9def3ef6-973a-49fa-88a7-0ef6690679f5)

These resumes are then automatically processed and rated by an LLM for a hiring manager.

Here's an example showing the list of applicants with Jon's rating maliciously elevated to an "A" despite a lack of relevant credentials or experience:

![Exploit screenshot](https://github.com/user-attachments/assets/961c90ed-3cbe-48c3-af26-80bb828aac45)

Tasks
-----

- Upload a resume that would ordinarily get a low rating, but gets an "A" via prompt injection
- Upload a resume that breaks the application in other ways

Running
-------

By default this app will use the [languagemodels](https://github.com/jncraton/languagemodels) Python package and Llama 3.2 3B for local inference. It can be run as:

```sh
python3 app.py
```

This app can use a local [VLLM](https://github.com/vllm-project/vllm) server to use for inference. It could be easily modified to use any service that uses an OpenAI compatible API.

The app can be run to use VLLM as:

```sh
VLLM_HOST=vllm VLLM_PORT=8000 python3 app.py
```
