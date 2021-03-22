import requests

GRACEDB_BASE_URL = 'https://gracedb.ligo.org'
GRACEDB_EVENT_URL = f'{GRACEDB_BASE_URL}/superevents'
SKIP_BASE_URL = 'http://skip.dev.hop.scimma.org'
SKIP_API_URL = f'{SKIP_BASE_URL}/api/alerts'


class GravitationalWaveClient:

    def get_superevent_data(self, superevent_id: str) -> dict:
        return requests.get(f'{SKIP_API_URL}/?event_trigger_number={superevent_id}&topic=6&ordering=-alert_timestamp').json()['results'][0]['extracted_fields']
