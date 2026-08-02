# What an API Is

Course SLO 4.20. Explained in my own words, using this project's real Claude API call as the example.

## What is an API?

Application Programming Interface — a way for programs to communicate with each other. An API is like a waiter at a restaurant: you're the client, the kitchen is the server. To get your food, you talk to the waiter, who takes your order, relays it to the kitchen, and brings back what you asked for. You never talk to the kitchen directly, and you don't need to know how it cooks.

## What actually happens on a real API call

When we ran the first "say hello" test, no code was shared between my computer and Anthropic's — my Python code stayed on my machine the whole time. What actually traveled over the internet was a **message**: the text "Say hello in exactly 3 words," sent to Anthropic's servers, processed there, and a text reply ("Hello there, friend!") sent back. An API call means sending information and getting information back — not sending a program to be run somewhere else.

## System vs. user message

The system part is fixed for all queries — an unchangeable set of rules for how Claude should respond, the same every time. The user part is the specific question — it changes per request and doesn't need to repeat the rules. In this project, `SYSTEM_PROMPT` in `app/rag/generation.py` is one constant reused on every call; the user message (excerpts + question) gets rebuilt fresh each time.

## Why the app actually needs the API call

Without calling Claude, the app would only be able to show the raw retrieved text chunks — relevant, but not processed into an answer to the specific question asked (that was as far as Step 5 got). The API call is what turns "here are some relevant paragraphs" into "here is a direct, cited answer to your actual question."
