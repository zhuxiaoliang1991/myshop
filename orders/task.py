from worker import call_by_worker
from django.core.mail import send_mail
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