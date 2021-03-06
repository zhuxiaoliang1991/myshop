from io import BytesIO

import weasyprint
from django.conf import settings

from django.template.loader import render_to_string

from worker import call_by_worker
from django.core.mail import send_mail, EmailMessage
from .models import Order

@call_by_worker
def order_created(order_id):
    '''
    当一个订单创建完成后发送邮件通知给用户
    :param order_id:
    :return:
    '''
    order = Order.objects.get(id=order_id)
    subject = '订单{}'.format(order.id)
    message = "亲爱的{},\n\n您的订单已完成，您的订单编号是{}".format(order.first_name,order.id)

    mail_sent = send_mail(subject,message,'634509103@qq.com',[order.email])
    return mail_sent


@call_by_worker
def send_order_mail(order):
    subject = '我的商城－发票 no.{}'.format(order.id)
    message = '您好，请接受您的购物订单'
    email = EmailMessage(subject, message, 'admin@shop.com', [order.email])

    #生成PDF文件
    html = render_to_string('orders/order/pdf.html',{'order':order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)

    #附加pdf文件作为邮件附件
    email.attach('订单_{}.pdf'.format(order.id),out.getvalue(),'application/pdf')

    email.send()

