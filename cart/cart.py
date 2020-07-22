from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self,request):
        '''
        初始化购物车对象
        '''
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #向session中存入空白购物车数据
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self,product,quantity=1,update_quantity=False):
        '''
        向购物车添加和更新商品及数量
        :param product: 商品对象
        :param quantity: 商品数量
        :param update_quantity: 是否为更新数据
        :return:
        '''
        product_id = str(product.id)
        #如果该商品在购物车里
        if product_id in self.cart:
            #如果是更新购物车中该商品的数量
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        #该商品不在购物车里面
        self.cart[product_id] = {'quantity':quantity,'price':str(product.price)}

    def save(self):
        #设置session.modified的值为True,中间件在看到这个属性的时候，就会保存session
        self.session.modified = True

    def remove(self,product):
        '''
        从购物车删除该商品
        :param product: 商品对象
        :return:
        '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''
        遍历所有购物车中的商品并从数据库中取得商品对象
        :return:
        '''
        product_ids = self.cart.keys()
        #获取购物车内所有商品对象
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product']=product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        '''
        购物车内一共有几件商品
        :return:
        '''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()