import datetime
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from apps.orders.models import Order
from apps.homes.models import House
from apps.orders.serializers import OrderInfoSerializer


class OrderInfo(ModelViewSet):

    serializer_class = OrderInfoSerializer
    lookup_field = ['order_id']

    def get_queryset(self):

        user_id = self.request.user.id
        # user_id = 1
        role = self.request.query_params.get('role')
        if role == 'custom':
            return Order.objects.filter(user_id=user_id).order_by('-begin_date')
        elif role == 'landlord':
            houses = House.objects.filter(user_id=user_id)
            return Order.objects.filter(house__in=houses).order_by('-begin_date')

    def list(self, request, *args, **kwargs):
        """订单列表"""

        orders = self.filter_queryset(self.get_queryset())
        order_list = []
        for i in orders:
            order = Order.to_dict(i)
            order_list.append(order)
        return Response({
            'data': {'orders': order_list},
            'errno': '0',
            'errmsg': 'OK',

        })

    def create(self, request, *args, **kwargs):
        """添加订单"""

        data = request.data
        data['user_id'] = request.user.id
        data['user'] = request.user
        house_id = data.get('house_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        data['begin_date'] = start_date

        data['house_price'] = House.objects.get(id=house_id).price
        data['days'] = (datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days
        data['amount'] = data['house_price'] * data['days']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': {'order_id': serializer.data.get('id')},
            'errno': '0',
            'errmsg': '下单成功'
        })

    @action(methods=['put'], detail=True)
    def accept_order(self, request, order_id):
        """接收订单/拒绝订单"""

        # order = self.get_object()
        order=Order.objects.get(id=order_id)
        if request.data.get('action') == 'accept':
            order.status = Order.ORDER_STATUS.get('WAIT_COMMENT')
            order.save()
            return Response({
                "errno": "0",
                "errmsg": "操作成功"
            })
        elif request.data.get('action') == 'reject':
            order.status = Order.ORDER_STATUS.get('REJECTED')
            order.comment = request.data.get('reason')
            order.save()
            return Response({
                "errno": "0",
                "errmsg": "操作成功"
            })

    @action(methods=['put'], detail=True)
    def set_comment(self, request, order_id):
        """评论"""

        # order = self.get_object()
        order = Order.objects.get(id=order_id)
        order.comment = request.data.get('comment')
        order.status = Order.ORDER_STATUS.get('COMPLETE')
        order.save()
        return Response({
            "errno": "0",
            "errmsg": "评论成功"
        })
