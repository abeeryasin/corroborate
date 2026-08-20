---
name: launch-app
description: Launch and drive Corroborate's Streamlit app (frontend/streamlit_app.py) to test it for real — upload a paper, ask a question, verify a real cited answer comes back. Use whenever asked to run, test, or screenshot this project's app.
---

# Launching Corroborate

## Start the server

```bash
source .venv/bin/activate
nohup streamlit run frontend/streamlit_app.py --server.headless true --server.port 8501 > /tmp/streamlit.log 2>&1 &
STREAMLIT_PID=$!
```

Wait for it to actually serve before doing anything else:

```bash
until curl -sf http://localhost:8501 >/dev/null; do sleep 1; done
```

(macOS's default shell doesn't have `timeout` — don't rely on it; the `until`/`curl` loop above works everywhere.)

## Gotcha: first request is slow

Streamlit only runs the script when a real client connects — nothing happens at server-start time. The *first* connection loads the `sentence-transformers` embedding model into memory, which takes 10–15+ seconds and produces no output until it's done. Check `/tmp/streamlit.log` for `Loading weights: 100%` before assuming the app is ready. A browser-automation script that times out on its first `wait-for` is almost always just hitting this cold start, not a real bug — wait longer (`sleep 15` before driving it, or a generous `waitForSelector` timeout) rather than debugging a fake failure.

## Drive it (Playwright / chromium-cli)

Real things learned testing this app, not generic advice:

- The page has **two** elements matching the text "Question" (the `<h2>` heading and the actual input). Use `page.getByRole("textbox", { name: "Question" })` — a bare `getByLabel("Question")` throws a strict-mode ambiguity error.
- `st.text_input` only triggers a Streamlit rerun on blur or Enter, **not on every keystroke**. After `.fill()`, send a `Tab` keypress (or click elsewhere) before checking for results — otherwise you'll see stale/empty output and wrongly conclude the feature is broken.
- Uploading a file: `page.locator('input[type="file"]').setInputFiles(path)`, fill in the Title field, then click the Upload button (`page.getByRole("button", { name: "Upload" })`) — the form only actually submits on that click.
- A real question through `generate_answer()` takes several real seconds (it's a live Claude API call, not local search). Wait for the "Reading your papers..." spinner text to disappear rather than a short fixed timeout.

## Stop it

```bash
kill $STREAMLIT_PID
```

Works reliably as long as you captured `$!` immediately after backgrounding the `nohup ... &` command (not after some other command ran in between).
