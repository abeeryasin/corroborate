# System Architecture

## What the frontend is, here

Frontend means the part of the app the user will interact with, i.e. the user interface. Streamlit is a Python library that turns a plain script into a web UI (a working browser page). The user will scroll to the search box, type in what they want to ask, upload PDFs, and submit.

## What the backend is, here

Backend means all the moving parts of the app that are not seen by the user but are essential for operations, e.g. the database, extraction, chunking, embeddings.

## How they currently talk to each other

Right now it's all one Python program talking to itself. `app/db`, `app/ingestion`, etc. are just other rooms in the same house, not a different building you have to call — so Streamlit isn't making any calls, it's calling functions directly.

## What's missing (the boundary)

The boundary between frontend and backend — it means the backend becomes its own independent thing with its own address, like `http://...`, that Streamlit, a future app, a script, or anything that knows how to make an HTTP call could call.

## Why the separation will eventually matter

So that it becomes reusable — different frontends could run against the same backend instead of each needing its own copy of the logic. Independent deployment of the backend on a more powerful machine, which means it could be updated without taking down the webpage. A single gate for security instead of logic scattered everywhere.
