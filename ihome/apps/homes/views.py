from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.homes.models import Area, House
from apps.homes.serializers import AreaSerializer, HouseSerializer
from utils.response_code import RET


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
