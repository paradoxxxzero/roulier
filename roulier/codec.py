"""Transform to/from a carrier specific format."""
from abc import ABC, abstractmethod
from .exception import InvalidApiInput
from .api import ApiParcel
import logging

_logger = logging.getLogger(__name__)


class Encoder(ABC):
    def __init__(self, config_object):
        self.config = config_object

    def _extra_input_data_processing(self, input_payload, data):
        return data

    @abstractmethod
    def transform_input_to_carrier_webservice(self, data, action):
        pass

    def encode(self, input_payload):
        """Transform input from external app to compatible input for carrier webservice."""
        validator = self.config.api(self.config)
        if not validator.validate(input_payload):
            _logger.warning("Laposte api call exception:")
            raise InvalidApiInput(
                {"api_call_exception": validator.errors(input_payload)}
            )
        data = validator.normalize(input_payload)
        data = self._extra_input_data_processing(input_payload, data)
        return self.transform_input_to_carrier_webservice(data)


class DecoderGetLabel(ABC):
    def __init__(self, config_object):
        """
            items in parcels list should be a dict of this form
            label = {
                "id": 1,
                "reference": "",
                "tracking": {
                    "number":"",
                    "url": "",
                    "partner": "",
                },
                "label": {
                    "data": base64 label,
                    "name": "",
                    "type": "",
                },
            }
        """
        self.config = config_object
        self.result = {
            "parcels": [],
            "annexes": [],
        }

    @abstractmethod
    def decode(self, response, payload):
        """Transform a specific representation to python dict.
        Args:
            response : answer from the webservice
            payload : data sent initially to the webservice
        Need to increment the result attribute of the object, it does not need to return
        anything
        """
        pass
