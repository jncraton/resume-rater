# Resume Rater

An example LLM application vulnerable to [prompt injection](https://en.wikipedia.org/wiki/Prompt_injection)

Learning Objectives
-------------------

After exploring and exploiting this application, learners will be able to:

- Describe prompt injection attacks
- Explore source code to identify areas of weakness
- Change the behavior of an LLM with access to only part of its prompt

Example
-------

Applicants upload resumes in `.docx` format using the root endpoint:

![Upload screenshot](https://github.com/user-attachments/assets/23114a2e-586f-497f-8316-135e123a11b1)

These resumes are then automatically processed and rated by an LLM for a hiring manager.

Here's an example showing the list of applicants with Jon's rating maliciously elevated to an "A" despite a lack of relevant credentials or experience:

![Exploit screenshot](https://github.com/user-attachments/assets/3742457e-fcc2-45aa-92ed-2f81b548dc04)

Running
-------

This app expects a local [VLLM](https://github.com/vllm-project/vllm) server to use for inference. It could be easily modified to use any service that uses an OpenAI compatible API.

The app can be run as:

```sh
VLLM_HOST=vllm VLLM_PORT=8000 python3 app.py
```
