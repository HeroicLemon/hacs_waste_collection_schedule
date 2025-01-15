
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
import requests
from datetime import datetime
from base64 import b64encode

TITLE = "Choice Waste Services"
DESCRIPTION = "Source for Choice Waste Services in the Commonwealth of Virginia, US."
COUNTRY = "us"
URL = "https://choicewasteservices.com/"
TEST_CASES = {
    "Choice Waste": {
        "username": "!secret choice_waste_username",
        "password": "!secret choice_waste_password",
    },
    "Choice Waste with manual site ID": {
        "username": "!secret choice_waste_username",
        "password": "!secret choice_waste_password",
        "site_id": "!secret choice_waste_site_id"
    }
}

ICON_MAP = {
    "trash": "mdi:trash-can",
    "recycle": "mdi:recycle",
}

API_URL = "https://choicewaste-portal.navusoft.net/rest"


class Source:
    def __init__(self, username, password, site_id=None):
        self._username = username
        self._password = password
        self._site_id = site_id

    def fetch(self):
        session = requests.session()

        # Create the hash for Basic Auth.
        hash = b64encode(f"{self._username}:{self._password}".encode(
            'utf-8')).decode("ascii")
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {hash}"
        }

        # If the site ID was not manually specified, query the listings and grab the first one.
        # This would probably be sufficient for most residential users.
        if self._site_id is None:
            r = session.get(f"{API_URL}/customer/listing", headers=headers)
            r.raise_for_status()
            self._site_id = r.json()['sitelist'][0]['id']

        # TODO: Determine how the valid dates for this request are determined.
        # For now, hardcode one year before this year/month through one year from this year/month.
        current_date = datetime.today()
        current_year = current_date.year
        current_month = current_date.strftime("%m")
        period_id = f"{current_year - 1}-{current_month}"
        through_period = f"{current_year + 1}-{current_month}"

        params = {
            "siteId": self._site_id,
            "periodId": period_id,
            "thruPeriod": through_period
        }

        r = session.get(f"{API_URL}/dispatch/services",
                        headers=headers, params=params)
        r.raise_for_status()

        services = r.json()

        if len(services) == 0:
            raise Exception("No services found")

        entries = []
        for service in services:
            date: datetime.date = datetime.strptime(
                service['scheduleddate'], "%Y-%m-%d").date()
            equipment_type: str = service['equipmenttype']
            icon = None

            if "recycle" in equipment_type.lower():
                icon = ICON_MAP.get("recycle")
            elif "trash" in equipment_type.lower():
                icon = ICON_MAP.get("trash")

            entries.append(Collection(date, equipment_type, icon))

        return entries
