from rest_framework.views import APIView
from rest_framework.response import Response

from apps.homes.models import Area
from apps.homes.serializers import AreaSerializer
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
