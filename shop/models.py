from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True,verbose_name=_('类别名称'))
    slug = models.SlugField(max_length=200,db_index=True,blank=True,verbose_name=_('分类简称'))

    class Meta:
        ordering = ('name',)
        verbose_name=_('商品分类')
        verbose_name_plural=verbose_name


    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=(self.slug,))

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE,verbose_name=_('商品分类'))
    name = models.CharField(max_length=200,db_index=True,verbose_name=_('商品名称'))
    slug = models.SlugField(max_length=200,blank=True,db_index=True,verbose_name=_('商品简称'))
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True,verbose_name=_('商品图片'))
    description = models.TextField(blank=True,verbose_name=_('商品描述'))
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name=_('价格'))
    available = models.BooleanField(default=True,verbose_name=_('可以购买'))
    created = models.DateTimeField(auto_now_add=True,verbose_name=_('创建时间'))
    updated = models.DateTimeField(auto_now=True,verbose_name=_('最近更新时间'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('商品')
        verbose_name_plural = verbose_name
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=(self.id,self.slug))
