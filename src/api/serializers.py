from rest_framework import serializers

from market_data.models.instrument import Instrument
from market_data.models.ohlc import OHLC


class InstrumentSerializer(serializers.Serializer):
    class Meta:
        model = Instrument


class OHLCSerializer(serializers.Serializer):
    class Meta:
        model = OHLC
