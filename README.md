# Massachusetts Bill Sponsors

A Flask app that shows an interactive map and table of sponsors for bills in the Massachusetts legislature, using data scraped from [malegislature.gov](https://malegislature.gov/Bills/).

Written as a proof-of-concept in 2017.

<https://ma-bill-sponsors.herokuapp.com>

## Developing

Install the dependencies:

```
$ python3 -m venv venv && source venv/bin/activate
$ pip install -U setuptools pip wheel
$ pip install -r requirements.txt
```

Set environment variables for Flask:

```
$ export FLASK_APP=ma_bill_sponsors.py
$ export FLASK_DEBUG=1
```

Run the development server:

```
$ flask run
```

Deploy to Heroku:

```
$ git push heroku
```

## TODO

- Rebuild map based on <https://bhrutledge.com/ma-legislature/> and <https://github.com/actonmass/campaign-map>
- Deploy via push to GitHub
