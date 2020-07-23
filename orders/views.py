from django.shortcuts import render, redirect
from django.urls import reverse

from orders.task import order_created
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
                #成功生成OrderItem之后，清除购物车
                cart.clear()
                #启动异步任务
                order_created(order.id)
                #在session中加入订单id
                request.session['order_id'] = order.id
                #重定向到支付支付页面
                return redirect(reverse('paymant:process'))
    else:
        form = OrderCreateForm()
        return render(request,'orders/order/create.html',{'cart':cart,'form':form})

