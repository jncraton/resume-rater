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

Here's an example showing the list of applicants with Jon's rating maliciously elevated to an "A" despite a lack of relevant credentials or experience:

![Exploit screenshot](https://github.com/user-attachments/assets/42e4afdb-9cab-4a75-aee7-aa72bc9b214d)

Running
-------

This app expects a local [VLLM](https://github.com/vllm-project/vllm) server to use for inference. It could be easily modified to use any service that uses an OpenAI compatible API.

The app can be run as:

```sh
VLLM_HOST=vllm VLLM_PORT=8000 python3 app.py
```
