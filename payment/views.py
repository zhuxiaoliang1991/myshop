import random

import time
from django.shortcuts import render, get_object_or_404, redirect
from alipay import AliPay
from django.conf import settings
from orders.models import Order


# Create your views here.
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    total_cost = order.get_total_cost()
    if request.method == 'GET':
        random_id = random.randint(0, 999999)
        braintree_id = time.strftime('%Y%m%d%H%M%S') + str(random_id)
        return render(request, 'pays/process.html', {'app_id': settings.APP_ID, 'total_cost': total_cost,'braintree_id':braintree_id})
    else:
        total_cost = request.POST.get('total_cost')
        braintree_id = request.POST.get('braintree_id')
        alipay = AliPay(
            appid=settings.APP_ID,
            app_notify_url=None,
            app_private_key_string=settings.APP_PRIVATE_KEY,
            alipay_public_key_string=settings.APP_PUBLIC_KEY,
            sign_type='RSA2',
            debug=True
        )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no = braintree_id,
            total_amount = total_cost,
            subject = str(Order.items.product),
            return_url = redirect('payment:done'),
        )
        order.braintree_id = braintree_id
        order.paid = True
        order.save()
        return redirect("https://openapi.alipaydev.com/gateway.do?" + order_string)


def payment_done(request):
    return render(request,'payment/done.html')


def payment_canceled(request):
    return render(request,'payment/canceled.html')