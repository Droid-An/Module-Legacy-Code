# PurpleForest Backend

To run:

### One time

1. In the `backend` directory, create a file named `.env` with values for the following environment variables:
   * `JWT_SECRET_KEY`: Any random string.
   * `POSTGRES_PASSWORD`: Any random string.
   * `POSTGRES_USER`: `postgres`, assuming you're using the bundled docker-based database, or whatever user you need if you have a custom postgres set up.
   * Optionally, `POSTGRES_DB`, `POSTGRES_HOST`, and `POSTGRES_PORT` if you're not using default postgres values.
2. Make a virtual environment: `python3 -m venv .venv`
3. Activate the virtual environment: `. .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the database: `../db/run.sh` (you must have Docker installed and running).
6. Create the database schema: `../db/create-schema.sh`

You may want to run `python3 populate.py` to populate sample data.

If you ever need to wipe the database, just delete `../db/pg_data` (and remember to set it up again after).

### Each time

1. In one terminal, run the database: `../db/run.sh` (you must have Docker installed and running).
2. In another terminal, activate the virtual environment: `. .venv/bin/activate`
3. With the virtual environment activated, run the backend: `python3 main.py`
