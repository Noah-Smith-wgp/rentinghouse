from rest_framework import serializers

from apps.homes.models import Area, House


# 查询城区列表
class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'
