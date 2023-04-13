from rest_framework import viewsets

from api.serializers import InstrumentSerializer, OHLCSerializer
from data_sources.api_interfaces.schema import OHLC
from market_data.models.instrument import Instrument


class InstrumentsViewSet(viewsets.ModelViewSet):
    model = Instrument
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()


class OHLCViewSet(viewsets.ModelViewSet):
    model = OHLC
    serializer_class = OHLCSerializer
    queryset = Instrument.objects.all()
