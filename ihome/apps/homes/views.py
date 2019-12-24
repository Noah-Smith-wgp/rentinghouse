from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from apps.homes.models import Area, House, HouseImage
from apps.homes.serializers import AreaSerializer, HouseSerializer, HouseImageSerializer
from utils.response_code import RET
from utils.qiniu import qiniu_upload


# 查询城区列表
class AreaAPIView(APIView):

    def get(self, request):

        areas = Area.objects.all()
        serializer = AreaSerializer(areas, many=True)

        data_list = []
        for data in serializer.data:
            a_dict = {
                "aid": data['id'],
                'aname': data['name']
            }
            data_list.append(a_dict)

        return Response({
            "errmsg": '获取成功',
            "errno": RET.OK,
            "data": data_list
        })


# 发布房源
class HouseAPIView(ModelViewSet):

    serializer_class = HouseSerializer
    queryset = House.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'errmsg': '发布成功',
            'errno': RET.OK,
            'data': {
                'house_id': serializer.data.get('id')
            }
        })


# 上传房源图片
class HouseImageView(ModelViewSet):

    serializer_class = HouseImageSerializer
    queryset = HouseImage.objects.all()

    def create(self, request, *args, **kwargs):
        image = request.FILES.get('house_image')
        house_id = kwargs.get('house_id')
        key = qiniu_upload(image.read())
        house = House.objects.get(id=house_id)
        house.index_image_url = key
        house.save()
        HouseImage.objects.create(house_id=house_id, url=key)

        return Response({
            'errmsg':'图片上传成功',
            'errno':RET.OK,
            'data':{
                'url':settings.QINIU_URL + key
            }
        })


# 我的房屋列表
class HouseListView(APIView):

    def get(self, request):

        user = request.user
        user = House.objects.get(user=user.username)
        data = House.to_basic_dict(user)
        return Response({'errmsg':'OK','errno': RET.OK,'data':data })