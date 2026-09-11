# Vacation Planner

A Python/Flask vacation planner for sequencing multiple cities, exporting an itinerary to CSV, and getting locally focused exploration ideas from the **City Guide** assistant.

## Run it

From the project folder, create a virtual environment and install the one Python dependency:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
flask --app vacation_planner:create_app run --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000` in a browser.

## Use it

1. Enter a trip name and start/end dates.
2. Add cities in travel order, each with arrival/departure dates and the transport used to reach it.
3. Download the itinerary as CSV, then load that CSV to resume planning later.
4. In **City Guide**, choose one of your cities, optionally name places you already want to see, and describe your travel style.
5. Open **Connect City Guide**, choose Google Gemini API, and provide the key location. Use `env:GEMINI_API_KEY` (recommended), or a key-file path within the ignored `Transportation/` or `Hotel/` folder. The local Python server calls Gemini.

The API key is never included in a CSV, written to browser storage, or saved in this repository. A key file may be stored in `Transportation/` or `Hotel/` because those folders are ignored by Git; do not commit it anywhere else.

City Guide is instructed to prioritize credible local signals over influencer and tourist-list recommendations. Treat its suggestions as leads and verify current hours, reservation requirements, and sources before making plans.

## Project structure

```text
src/vacation_planner/       Python application package
├── routes.py               Web and API routes
├── services/city_guide.py  Gemini integration and key handling
├── templates/              Flask HTML templates
└── static/                 Browser JavaScript and CSS
tests/                      Automated tests
Transportation/             Private ignored transport records
Hotel/                      Private ignored lodging records
```
