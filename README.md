# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## Tasks

There are `@TODO` comments throughout the project. We recommend tackling the sections in order. Start by reading the READMEs in:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to complete the required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)

## How to Run and Test Backend and Frontend

### Backend Setup

1. Create venv (I usually do this from the project folder, `./coffee-shop/`)
   - `py -3.7 -m venv venv` (or whichever python3 version you use)
2. Activate venv
   - `source venv/Scripts/activate`
3. Update pip and setuptools in venv to ensure required packages are installed correctly
   - `python -m pip install -U pip setuptools`
4. Install required packages (in `./coffee-shop/backend/`)
   - `cd backend`
   - `pip install -r requirements.txt`
5. Set flask env vars
   - `export FLASK_APP=api.py`
   - `export FLASK_DEBUG=True`
6. Run flask app (from `src` folder)
   - `cd src`
   - `flask run`
7. App should now be running on `localhost:5000` (or `http://127.0.0.1:5000`)

### Frontend Setup

1. Intall node.js/npm (if not already installed)
   - [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
2. Install required npm packages (in `./coffee-shop/frontend/`)
   - `npm install`
3. There may still be dependency issues with node-sass. If ionic throws errors in step 6, try this:
   1. To fix, first uninstall node-sass: `npm uninstall node-sass`
   2. Then install sass: `npm install sass`
4. Install ionic (if not already installed)
   - `npm install -g @ionic/cli`
5. To fix potential self-signed certificate issue:
   - `export NODE_OPTIONS=--openssl-legacy-provider`
6. Start serving via ionic
   - `ionic serve`
7. A new browser tab should automatically open to coffee shop page on `http://localhost:8100`

### Postman Setup

1. In Postman, click `Import`, then navigate to `./coffee-shop/backend`
2. Import updated `udacity-fsnd-udaspicelatte.postman_collection.json` collection
3. Right click `udacity-fsnd-udaspicelatte.postman_collection` (or click the three dots next to the name) and select `Run Collection`
4. In Runner, click `Run udacity-fsnd-udaspicelatte` to run all tests
5. Note: the tokens for Manager and Barista have been set to timeout after 24 hours
