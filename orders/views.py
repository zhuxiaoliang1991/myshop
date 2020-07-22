from django.shortcuts import render

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
                return render(request,'orders/order/created.html',{'order':order})
    else:
        form = OrderCreateForm()
        return render(request,'orders/order/create.html',{'cart':cart,'form':form})
