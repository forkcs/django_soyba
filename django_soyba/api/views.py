from rest_framework import serializers, viewsets
from rest_framework.request import Request

from api.serializers import InstrumentSerializer, OhlcSerializer
from data_sources.models import MarketDataSourceChoices
from market_data.models.instrument import Instrument
from market_data.models.ohlc import Ohlc


class RequestSerializer(serializers.Serializer):
    data_source = serializers.ChoiceField(choices=MarketDataSourceChoices.choices)


class InstrumentsViewSet(viewsets.ReadOnlyModelViewSet):
    model = Instrument
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()

    def get(self, request: Request, *args, **kwargs):
        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().get(request, *args, **kwargs)


class OhlcViewSet(viewsets.ReadOnlyModelViewSet):
    model = Ohlc
    serializer_class = OhlcSerializer
    queryset = Ohlc.objects.all()

    def get(self, request: Request, *args, **kwargs):
        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().get(request, *args, **kwargs)
