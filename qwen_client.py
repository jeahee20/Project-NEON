import re
import time

try:
    import requests
except Exception as requests_error:
    requests = None

import neon_prompt
import prompt_optimizer
import performance_state
import neon_filter


OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
QWEN_MODEL = "qwen3:1.7b"
DEBUG_QWEN = False
MAX_QWEN_SECONDS = 8


def clean_qwen_response(text):
    if text is None:
        return None

    text = str(text)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<thinking>.*?</thinking>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"^\s*(thinking|reasoning)\s*[:\uff1a].*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = text.replace("<think>", "").replace("</think>", "")
    text = text.replace("<thinking>", "").replace("</thinking>", "")

    forbidden_lines = (
        "As an AI",
        "As a language model",
        "I am Qwen",
        "I am an AI",
        "\uc800\ub294 AI\uc785\ub2c8\ub2e4",
        "\uc800\ub294 Qwen\uc785\ub2c8\ub2e4",
        "\uc800\ub294 \uc5b8\uc5b4 \ubaa8\ub378\uc785\ub2c8\ub2e4",
        "Alibaba",
    )

    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if any(phrase.lower() in stripped.lower() for phrase in forbidden_lines):
            continue
        lines.append(line.rstrip())

    cleaned = "\n".join(lines).strip()
    return neon_filter.filter_response(cleaned) or None


def ask_qwen(message, category="default", context=None):
    prompt = neon_prompt.build_prompt(message, category, context)
    if DEBUG_QWEN:
        print("[QWEN REQUEST]", prompt[:300])

    payload = {
        "model": QWEN_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:
        if requests is None:
            raise ImportError("requests module is not available")

        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=12)
        response.raise_for_status()
        result = response.json()
        if DEBUG_QWEN:
            print("[QWEN RAW]", result)
    except Exception as error:
        print("[QWEN ERROR]", error, flush=True)
        if DEBUG_QWEN:
            print("[QWEN ERROR]", error)
        return None

    return clean_qwen_response(result.get("response"))

def build_prompt(message, category="default", context=None):
    performance_state.set_stage(performance_state.STAGE_PROMPT, "prompt")
    try:
        return prompt_optimizer.build_optimized_prompt(message, category, context)
    except Exception as error:
        print("[PROMPT OPTIMIZER ERROR]", error)
        return neon_prompt.build_prompt(message, category, context)


def stream_qwen(message, category="default", context=None):
    prompt = build_prompt(message, category, context)
    if DEBUG_QWEN:
        print("[QWEN REQUEST]", prompt[:300])

    payload = {
        "model": QWEN_MODEL,
        "prompt": prompt,
        "stream": True,
    }
    payload["options"] = {"num_predict": 110}

    if requests is None:
        raise ImportError("requests module is not available")

    performance_state.set_stage(performance_state.STAGE_QWEN, "qwen")
    start_time = time.time()
    response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=(2, 8), stream=True)
    response.raise_for_status()

    for line in response.iter_lines(decode_unicode=True):
        if time.time() - start_time > MAX_QWEN_SECONDS:
            print("[QWEN TIMEOUT]", MAX_QWEN_SECONDS, flush=True)
            break
        if not line:
            continue
        try:
            result = response.json() if False else __import__("json").loads(line)
        except Exception:
            continue

        if DEBUG_QWEN:
            print("[QWEN RAW]", result)
        chunk = result.get("response", "")
        if chunk:
            yield chunk

        if result.get("done"):
            break


def ask_qwen(message, category="default", context=None):
    try:
        chunks = []
        for chunk in stream_qwen(message, category=category, context=context):
            chunks.append(chunk)
    except Exception as error:
        if DEBUG_QWEN:
            print("[QWEN ERROR]", error)
        return None

    performance_state.set_stage(performance_state.STAGE_FILTERING, "filter")
    return clean_qwen_response("".join(chunks))
