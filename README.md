# IGDB API Wrapper

![Python](https://img.shields.io/badge/Python-3.10.9-green.svg?style=flat&logo=python "Python Version")

This is a simple wrapper for the [IGDB API](https://api-docs.igdb.com).

Fetches the following data:
Game name, description, cover image

## Required Environment Variables:

| Variable      | Description                                                   | Required? | Default   |
|---------------|---------------------------------------------------------------|-----------|-----------|
| CLIENT_ID     | Client ID of IGDB API                                         |  &check; | None      |
| CLIENT_SECRET | Client Secret of IGDB API                                     |  &check; | None      |
| DB_URI        | A [tortoise-orm supported database][link1] connection string. |  &check; | None      |
| HOST          | Host to run the server on                                     |     _     | 127.0.0.1 |
| PORT          | Port to run the server on                                     |     _     | 8000      |

[link1]: https://tortoise.github.io/databases.html?h=support#databases "Tortoise-ORM Supported Databases"

## Installation

* Clone the repository

```bash
git clone https://github.com/infinity-plus/igdb-api.git -b master
cd igdb-api
```

*  Install the requirements

```bash
python -m pip install -r requirements.txt
```

* Create a `.env` file in the root directory and add the required environment variables
* Run the server

```bash
python -m IGDB
```
