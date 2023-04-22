from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import InstrumentSerializer, OHLCSerializer
from data_sources.models import MarketDataSourceChoices
from market_data.models.instrument import Instrument
from market_data.models.ohlc import OHLC


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


class OHLCViewSet(viewsets.ReadOnlyModelViewSet):
    model = OHLC
    serializer_class = OHLCSerializer
    queryset = OHLC.objects.all()

    def get(self, request: Request, *args, **kwargs):
        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().get(request, *args, **kwargs)
