from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from apps.homes.models import Area, House, HouseImage
from apps.homes.serializers import AreaSerializer, HouseSerializer, HouseImageSerializer
from utils import constants
from utils.decorators import login_required
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

        return Response({"errmsg": '获取成功', "errno": RET.OK, "data": data_list})


# 发布房源
class HouseAPIView(ModelViewSet):

    serializer_class = HouseSerializer
    queryset = House.objects.all()
    # pagination_class = PageNum

    @method_decorator(login_required)
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

    # 房屋数据搜索
    def list(self, request, *args, **kwargs):
        page = request.query_params.get('p')
        sort_key = request.query_params.get('sk')
        # 查询数据
        if sort_key == "booking":
            # 订单量从高到低
            houses = House.objects.all().order_by("-order_count")
        elif sort_key == "price-inc":
            # 价格从低到高
            houses = House.objects.all().order_by("price")
        elif sort_key == "price-des":
            # 价格从高到低
            houses = House.objects.all().order_by("-price")
        else:
            # 默认以最新的排序
            houses = House.objects.all().order_by("-create_time")
        # queryset = self.get_queryset()

        paginator = Paginator(houses, constants.HOUSE_LIST_PAGE_CAPACITY)
        page_houses = paginator.page(page)
        total_page = paginator.num_pages
        house_list = []
        for i in page_houses:
            house = House.to_basic_dict(i)
            house_list.append(house)

        return Response({'errmsg': '请求成功', 'errno': RET.OK, 'data': {'houses': house_list, 'total_page': total_page}})


# 上传房源图片
class HouseImageView(ModelViewSet):

    serializer_class = HouseImageSerializer
    queryset = HouseImage.objects.all()

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        image = request.FILES.get('house_image')
        house_id = kwargs.get('house_id')
        key = qiniu_upload(image.read())
        house = House.objects.get(id=house_id)
        house.index_image_url = key
        house.save()
        HouseImage.objects.create(house_id=house_id, url=key)

        return Response({
            'errmsg': '图片上传成功',
            'errno': RET.OK,
            'data': {
                'url': settings.QINIU_URL + key
            }
        })


# 我的房屋列表
class HouseListView(APIView):

    @method_decorator(login_required)
    def get(self, request):

        user = request.user
        houses = House.objects.filter(user=user)
        house_list = []
        for i in houses:
            data = House.to_basic_dict(i)
            house_list.append(data)
        return Response({'errmsg': 'OK', 'errno': RET.OK, 'data': {'houses': house_list}})


# 首页房屋推荐
class HouseIndexView(APIView):

    def get(self, request):
        houses = House.objects.all()
        house_list = []
        for i in houses:
            house = House.to_basic_dict(i)
            house_list.append(house)
        return Response({'errmsg': 'OK', 'errno': RET.OK, 'data': house_list})


# 房屋详情页面
class HouseDetailView(APIView):

    def get(self, request, house_id):

        house = House.objects.get(id=house_id)
        detail_list = House.to_full_dict(house)
        return Response({'errmsg': 'OK', 'errno': RET.OK, 'data': {'house': detail_list, 'user_id': house.user_id}})
