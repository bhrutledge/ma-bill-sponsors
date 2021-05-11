import csv
from collections import OrderedDict
from io import StringIO
from pathlib import PurePath
from datetime import timedelta

import requests
import requests_cache
from bs4 import BeautifulSoup
from flask import Flask, abort, jsonify, render_template, request

app = Flask(__name__)

# Assuming we'll be using OrderedDict
app.config["JSON_SORT_KEYS"] = False

requests_cache.install_cache(expire_after=timedelta(minutes=10))

LEGISLATORS = requests.get(
    "https://bhrutledge.com/ma-legislature/dist/ma_legislators.json"
).json()
LEGISLATOR_FIELDS = ["chamber", "district", "first_name", "last_name", "party", "url"]

BASE_URL = "https://malegislature.gov"


def csvify(data):
    """
    Returns a CSV response for list of dicts.
    """
    csv_data = StringIO()
    writer = csv.DictWriter(csv_data, data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return app.response_class(csv_data.getvalue(), mimetype="text/csv")


def select_string(soup, selector):
    return (soup.select_one(selector).string or "").strip()


def get_soup(url):
    # HACK: Work around SSLError "unable to get local issuer certificate"
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def parse_bill(soup):
    return OrderedDict(
        [
            ("name", select_string(soup, "title")),
            ("term", select_string(soup, "h1 .subTitle")),
            ("title", select_string(soup, ".content h2")),
            (
                "presenters",
                [
                    get_cosponsor_url(x)
                    for x in soup.select(".billInfo [href*=Legislators]")
                ],
            ),
            (
                "sponsors",
                [
                    get_cosponsor_url(x)
                    for x in soup.select("#searchResults [href*=Legislators]")
                ],
            ),
        ]
    )


def get_cosponsor_url(link):
    # Assuming link like
    # <a href="/Legislators/Profile/JBE0/190/Cosponsor">James B. Eldridge</a>
    return BASE_URL + str(PurePath(link["href"]).parent.parent)


def get_bill(term_name, bill_name):
    bill_url = BASE_URL + f"/Bills/{term_name}/{bill_name}/Cosponsor"

    bill_soup = get_soup(bill_url)
    bill = parse_bill(bill_soup)
    bill["url"] = bill_url

    return bill


# TODO: Use itertools.groupby
# TODO: Add party
def tally_legislators(legislators):
    house = [x for x in legislators if x["chamber"] == "House"]
    senate = [x for x in legislators if x["chamber"] == "Senate"]

    return {
        "house": len(house),
        "house_sponsors": len([x for x in house if x["sponsor"]]),
        "senate": len(senate),
        "senate_sponsors": len([x for x in senate if x["sponsor"]]),
    }


# TODO: Regex routes
# TODO: Break into smaller functions
# TODO: Allow multiple bills
# TODO: Consider adding term_name to downloaded filename
# TODO: Consider using tablib and send_file to streamline CSV and JSON response
# TODO: Consider Bill and Legislator classes
@app.route("/<term_name>/<bill_name>")
def get_legislators_for_bill(term_name, bill_name):
    try:
        bill = get_bill(term_name, bill_name)
    except requests.HTTPError as ex:
        abort(ex.response.status_code)

    def process(legislator):
        """
        Returns an OrderedDict of legislator fields and bill sponsorship.
        """
        result = OrderedDict((k, legislator[k]) for k in LEGISLATOR_FIELDS)
        result["sponsor"] = legislator["url"] in bill["sponsors"]

        return result

    legislators = [process(x) for x in LEGISLATORS]

    request_format = request.args.get("format")

    # TODO: AJAX
    if request_format == "json":
        return jsonify(legislators)

    if request_format == "csv":
        return csvify(legislators)

    tally = tally_legislators(legislators)

    # TODO: Use `g` for context?
    return render_template("bill.html", bill=bill, legislators=legislators, tally=tally)


@app.route("/")
def index():
    return render_template("index.html")
