from django.db import models
from shop.models import Product

# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=50,verbose_name='姓')
    last_name = models.CharField(max_length=50,verbose_name='名')
    email = models.EmailField(verbose_name='邮箱')
    address = models.CharField(max_length=250,verbose_name='收货地址')
    postal_code = models.CharField(max_length=20,verbose_name='邮编')
    city = models.CharField(max_length=100,verbose_name='城市')
    created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    paid = models.BooleanField(default=False,verbose_name='是否支付')
    braintree_id = models.CharField(max_length=150,blank=True)

    class Meta:
        verbose_name = '订单用户信息'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        return "购买者{}".format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE,verbose_name='购买者')
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE,verbose_name='订单商品')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    quantity = models.PositiveIntegerField(default=1,verbose_name='商品数量')

    class Meta:
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity