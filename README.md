# 3D Word Cloud

A full-stack web app that visualizes topics from a news article as an interactive 3D word cloud. Paste any article URL and the backend will extract and rank keywords using TF-IDF, then render them in a 3D sphere using React Three Fiber.

## Tech Stack

**Frontend:** React, TypeScript, React Three Fiber, Three.js, Tailwind CSS

**Backend:** Python, FastAPI, BeautifulSoup, scikit-learn

## Prerequisites

- Python 3.x
- Node.js

## Setup & Running

From the root directory:
```bash
./setup.sh
```

This will install all dependencies for both frontend and backend and start both servers concurrently.

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

> If ports 8000 or 5173 are already in use, kill the existing processes before running setup.sh.

## API

`POST /analyze`

Body:
```json
{ "url": "https://..." }
```

Returns:
```json
{ "words": [{ "word": "string", "weight": 0.0 }] }
```

## Notes

- Keyword extraction uses TF-IDF via scikit-learn. Weights are normalized to 0–1 and square-root scaled for visual balance.
- Word size and color (blue → pink) both encode relevance — bigger and pinker means more important.
- The 3D sphere uses a Fibonacci distribution for even word spacing.
- Crawling is basic — works well on most news sites but may return limited results on paywalled or JS-rendered pages.
