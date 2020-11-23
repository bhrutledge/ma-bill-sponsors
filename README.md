# Massachusetts Bill Sponsors

A Flask app that shows an interactive map and table of sponsors for bills in the Massachusetts legislature, using data scraped from [malegislature.gov](https://malegislature.gov/Bills/).

Written as a proof-of-concept in 2017.

<https://ma-bill-sponsors.herokuapp.com>

## TODO

- Add local dev instructions
- Add instructions/script for generating legislator JSON
    - Currently a Jupyter Notebook that scrapes [malegislature.gov](https://malegislature.gov/Legislators/)
- Add instructions/script for generating legislative district GeoJSON
    - Originally from MassGIS Data for the [House](https://docs.digital.mass.gov/dataset/massgis-data-massachusetts-house-legislative-districts) and [Senate](https://docs.digital.mass.gov/dataset/massgis-data-massachusetts-senate-legislative-districts) legislative districts
    - See [bhrutledge/somerville-city-council](https://github.com/bhrutledge/somerville-city-council) for an example
