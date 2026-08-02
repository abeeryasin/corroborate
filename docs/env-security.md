# Env Variables & Secrets

Course SLO 4.21. Explained in my own words, using this project's real `.env` setup — including a real mistake — as the example.

## `.env` vs. `.env.example`

`.env` is hidden from git, so it can store real information (like an API key) without the risk of it being shared on the internet when the project is deployed or pushed. `.env.example` contains fake placeholder info describing what's actually in `.env` — for example, the real API key is stored in `.env`, but only a placeholder like `your-api-key-here` goes in `.env.example`.

## Why the key can't just be typed into the code

`generation.py` (and every other code file) *is* tracked by git — unlike `.env`, nothing stops it from being pushed to GitHub. If the API key were typed directly into that file, it could be used or abused by others on the internet the moment the project is shared or deployed.

## The real mistake, and how we knew it was still safe

I typed the actual API key into `.env.example` itself instead of `.env` — the wrong file. Nothing bad ended up happening, but not because the mistake was harmless on its own — it was caught and confirmed safe. The proof wasn't just fixing the file afterward; it was running `git status` and seeing `.env.example` listed as **untracked**, meaning it had never been committed or pushed anywhere. If it *had* already been pushed to GitHub, editing the file afterward wouldn't have been enough on its own — the old version with the real key would still exist in the project's history, and the key would need to be revoked regardless of the edit. The lesson: after a secret ends up in the wrong place, check `git status` (or `git log`) before assuming the danger has passed — fixing the file and confirming nothing leaked are two different steps.
