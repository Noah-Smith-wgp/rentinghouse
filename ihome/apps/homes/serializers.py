from rest_framework import serializers

from apps.homes.models import Area, House


# 查询城区列表
class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'


# 发布房源
class HouseSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    area = serializers.StringRelatedField()
    user_id = serializers.IntegerField()
    area_id = serializers.IntegerField()

    class Meta:
        model = House
        fields = '__all__'
