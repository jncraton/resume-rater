# Resume Rater

An example LLM application vulnerable to [prompt injection](https://en.wikipedia.org/wiki/Prompt_injection)

Learning Objectives
-------------------

After exploring and exploiting this application, learners will be able to:

- Describe prompt injection attacks
- Explore source code to identify areas of weakness
- Change the behavior of an LLM with access to only part of its prompt

Running
-------

This app expects a local [VLLM](https://github.com/vllm-project/vllm) server to use for inference. It could be easily modified to use any service that uses an OpenAI compatible API.

The app can be run as:

```sh
VLLM_HOST=vllm VLLM_PORT=8000 python3 app.py
```
