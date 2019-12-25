from rest_framework import serializers
from apps.orders.models import Order


class OrderInfoSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    house = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField()
    house_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = '__all__'
