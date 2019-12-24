from rest_framework import serializers

from apps.homes.models import Area, House, HouseImage


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


# 上传房源图片
class HouseImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseImage
        fields = '__all__'


# 首页房屋推荐
# class HouseIndexSerializer(serializers.ModelSerializer):
#
#     # user = serializers.StringRelatedField()
#     # area = serializers.StringRelatedField()
#     # user_id = serializers.IntegerField()
#     # area_id = serializers.IntegerField()
#
#     class Meta:
#         model = House
#         fields = ['house_id', 'img_url', 'title']
