# -*- coding: utf-8 -*-
"""Factory of main classes."""
from .carriers.laposte.laposte import Laposte
from .carriers.dummy.dummy import Dummy
from .carriers.geodis.geodis import Geodis
from .carriers.dpd_fr.dpd import Dpd as Dpd_fr
from .carriers.dpd.dpd import Dpd as Dpd_legacy

def _carriers():
    """Get names:class of carriers.

    You may use the factory get('laposte') instead.
    """
    return {
        "laposte": Laposte,
        "dummy": Dummy,
        "geodis": Geodis,
        "dpd_fr": Dpd_fr,
        "dpd": Dpd_legacy,
    }


def get_carriers():
    """Get name of available carriers.

    return: list of strings
    """
    return _carriers().keys()


def get(carrier):
    """Get a 1 method carrier implementation.

    If you need more, like only encode or only transport
    (Webservice), instanciate class directly like:
    from roulier.carriers.laposte import LaposteTransport
    ws = LaposteTransport()
    ws.send(data)
    """
    carrier_obj = _carriers().get(carrier.lower())

    if carrier_obj:
        return carrier_obj()
    else:
        raise BaseException("Carrier not found")
