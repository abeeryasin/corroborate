# Deployment Rationale

Course SLO 4.17. Explained in my own words, using this project's real deploy of Corroborate as the example.

## What deploying means

Deploying means connecting the app to a public address (a URL) that anyone can type into a browser and open. It's always reachable in principle — but whether it stays warm, keeps its data, and handles real traffic depends on the type of host and tier being used. It also allows for multiple users.

It's different from running locally: when an app runs in a terminal, it only runs on that one laptop and cannot be opened from another machine — and closing the terminal closes the app too.

Analogy: a kitchen versus a restaurant. A kitchen (a locally running app) only runs while you're in it, and isn't open to the public — only to the household. A restaurant, on the other hand, has the option to be open 24/7, serve multiple customers, and run on proper infrastructure — but that's an option it has, not something automatic just by being a restaurant.

## Ephemeral vs. persistent storage

Ephemeral storage means 12 hours of inactivity triggers sleep, and it's specifically waking back up (or a new redeploy) that wipes the disk, deleting all uploaded papers in the process. So working on the same set of papers over several days becomes impossible without re-uploading after every period of inactivity or sleep.

A persistent volume would mean that once papers are added to the website, they get stored on disk permanently, and only get deleted when I choose to delete them.

I decided ephemeral storage was fine for now — for a demo lasting under 12 hours, it's adequate. Paying $5 a month (and possibly more) on a recurring basis for an MVP didn't seem worth it yet. This can be reconsidered in v2 or v3.

## Why a GitHub account was necessary

I needed a GitHub account because until then, the app and all its changes were only accessible from my own laptop. Uploading to GitHub means the code can be accessed from other machines, and it can be deployed on a host platform like Streamlit Community Cloud directly from the GitHub repo, rather than manually copying files. Streamlit Community Cloud pulls directly from the GitHub repo, which is why GitHub was necessary before deployment.
