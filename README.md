# Massachusetts Bill Sponsors

A Flask app that shows an interactive map and table of sponsors for bills in the Massachusetts legislature, using data scraped from [malegislature.gov](https://malegislature.gov/Bills/).

Written as a proof-of-concept in 2017.

<https://ma-bill-sponsors.herokuapp.com>

## TODO

- Turn these into GitHub Issues
- Add local dev instructions
- Extract instructions/script for generating legislator JSON
    - Currently a [Jupyter Notebook](./data/ma_legislators.ipynb) that scrapes [malegislature.gov](https://malegislature.gov/Legislators/)
    - Consider using the [Open States API](https://docs.openstates.org/en/latest/api/v2)
        - Caveat: [Massachusetts House districts should be abbreviated · Issue #170 · openstates/issues](https://github.com/openstates/issues/issues/170)
    - Probably belongs in [bhrutledge/ma-legislators](https://github.com/bhrutledge/ma-legislators)
- Automate updating district and legislator data
    - GeoJSON is currently copied from [bhrutledge/ma-legislators](https://github.com/bhrutledge/ma-legislators)
