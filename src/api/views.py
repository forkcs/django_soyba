from rest_framework import viewsets

from api.serializers import InstrumentSerializer, OHLCSerializer
from market_data.models.instrument import Instrument
from market_data.models.ohlc import OHLC


class InstrumentsViewSet(viewsets.ModelViewSet):
    model = Instrument
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()


class OHLCViewSet(viewsets.ModelViewSet):
    model = OHLC
    serializer_class = OHLCSerializer
    queryset = OHLC.objects.all()
