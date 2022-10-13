''' This class defines a message handler for a tom_alertstreams connection to GW events

'''
from tom_nonlocalizedevents.models import NonLocalizedEvent
import logging

logger = logging.getLogger(__name__)


EXPECTED_FIELDS = [
    'TRIGGER_NUM',
    'SEQUENCE_NUM',
    'NOTICE_TYPE',
    'SKYMAP_FITS_URL'
]


def extract_fields(message):
    fields = {}
    keys = message.split('\n')
    for key in keys:
        if key:
            field_name = key.split(':')[0]
            if field_name in EXPECTED_FIELDS:
                fields[field_name] = key.split(':')[1].strip()
    if set(EXPECTED_FIELDS) != set(fields.keys()):
        logger.warning(f"Incoming GW message did not have the expected fields, ignoring it: {keys}")
        return {}

    return fields


def handle_message(topic, message):
    # It receives a string topic, and bytestring message in the LIGO GW format
    # fields must be extracted from the message text and stored into in the model
    fields = extract_fields(message.decode('utf-8'))
    if fields:
        _, created = NonLocalizedEvent.objects.update_or_create(
            event_id = fields['TRIGGER_NUM'],
            sequence_id = fields['SEQUENCE_NUM'],
            event_type = NonLocalizedEvent.NonLocalizedEventType.GRAVITATIONAL_WAVE,
            defaults = {
                'skymap_fits_url': fields['SKYMAP_FITS_URL'],
                'event_subtype': fields['NOTICE_TYPE']
            }
        )
        if created:
            logger.info("Ingested a GW event from alertstream")
        else:
            logger.warning(f"GW event with id {fields['TRIGGER_NUM']} and sequence id {fields['SEQUENCE_NUM']} already exists in the system")
