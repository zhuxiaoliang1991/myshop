from django.urls import path
from .views import *
from django.utils.translation import gettext_lazy as _

app_name='orders'

urlpatterns = [
    path(_('create/'),order_create,name='order_create'),
    path('admin/order/<int:order_id>/',admin_order_detail,name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/',admin_order_pdf,name='admin_order_pdf'),
]