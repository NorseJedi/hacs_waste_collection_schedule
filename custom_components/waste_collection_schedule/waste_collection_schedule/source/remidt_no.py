import datetime
import urllib

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "ReMidt Midt-Norge"
DESCRIPTION = "Source for ReMidt in central Norway."
URL = "https://www.remidt.no"
TEST_CASES = {
    "Follovegen": {"address": "Follovegen 1 B", "join_events": False },
    "Follovegen Joined": {"address": "Follovegen 1 B", "join_events": True },
    "Makrellsvingen": {"address": "Makrellsvingen 14 - 20", "join_events": False },
    "Makrellsvingen Joined": {"address": "Makrellsvingen 14 - 20", "join_events": True },
    "Taubaneveien": {"address": "Taubaneveien 46", "join_events": False },
    "Taubaneveien Joined": {"address": "Taubaneveien 46", "join_events": True },
    "Mistfjordveien": {"address": "Mistfjordveien 1299", "join_events": False },
    "Mistfjordveien Joined": {"address": "Mistfjordveien 1299", "join_events": True },
}

API_URL = "https://kalender.renovasjonsportal.no/api/address/"  # or station

ICON_MAP = {  # Optional: Dict of waste types and suitable mdi icons
    "Restavfall": "mdi:trash-can",
    "Glass og metallemballasje": "mdi:bottle-soda",
    "Matavfall": "mdi:food-apple",
    "Papir": "mdi:package-variant",
    "Plastemballasje": "mdi:recycle",
    "Multiple": "mdi:delete-variant"
}

PARAM_DESCRIPTIONS = { # Optional dict to describe the arguments, will be shown in the GUI configuration below the respective input field
    "en": {
        "address": "Address for the waste collection.",
        "join_events": "Join same-day events into one event per day.",
    }
}
#
# PARAM_TRANSLATIONS = {  # Optional dict to translate the arguments, will be shown in the GUI configuration form as placeholder text
#     "en": {
#         "address": "Collection address",
#         "join_events": "Join same-day events",
#     }
# }

class Source:
    def __init__(self, address: str, join_events: bool = False):
        self.address = address
        self.join_events = join_events

    def fetch(self):
        r = requests.get(API_URL + urllib.parse.quote(self.address))
        r.raise_for_status()
        address_id = r.json()["searchResults"][0]["id"]

        r = requests.get(API_URL + address_id + "/details/")
        r.raise_for_status()
        disposals = r.json()["disposals"]

        # Parse all collections
        parsed = [
            (
                datetime.datetime.fromisoformat(d["date"]).date(),
                d["fraction"],
            )
            for d in disposals
        ]

        # Default one event per disposal type
        if not self.join_events:
            return [
                Collection(
                    date=date,
                    t=fraction,
                    icon=ICON_MAP.get(fraction),
                )
                for date, fraction in parsed
            ]

        # Join same-day events:
        grouped = {}
        for date, fraction in parsed:
            grouped.setdefault(date, []).append(fraction)

        # Build the joined events
        entries = []
        for date, fractions in sorted(grouped.items()):
            # Comma separated event title
            t_value = ", ".join(fractions)

            # Use default icon if multiple types, otherwise select the proper icon
            if len(fractions) == 1:
                icon = ICON_MAP.get(fractions[0])
            else:
                icon = ICON_MAP.get("Multiple")

            entries.append(
                Collection(
                    date=date,
                    t=t_value,
                    icon=icon,
                )
            )

        return entries
