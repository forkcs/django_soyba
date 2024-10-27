from rest_framework import serializers

from market_data.models.instrument import Instrument
from market_data.models.ohlc import Ohlc


class InstrumentSerializer(serializers.Serializer):
    class Meta:
        model = Instrument
        fields = '__all__'


class OhlcSerializer(serializers.Serializer):
    class Meta:
        model = Ohlc
        fields = '__all__'
