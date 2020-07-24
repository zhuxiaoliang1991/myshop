from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True,verbose_name='优惠券卡号')
    valid_from = models.DateTimeField(verbose_name='起始有效期')
    valid_to = models.DateTimeField(verbose_name='终止有效期')
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name='折扣')
    active = models.BooleanField(verbose_name='是否有效')

    class Meta:
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code