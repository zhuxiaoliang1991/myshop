from django.shortcuts import render,get_object_or_404
from .recommender import Recommender
from cart.forms import CartAddProductForm
from .models import *


# Create your views here.
def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=category,available=True)
    return render(request,'shop/product/list.html',{
        'category':category,'categories':categories,'products':products
    })


def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product],max_results=4)
    return render(request,'shop/product/detail.html',{'product':product,'cart_product_form':cart_product_form,'recommended_products':recommended_products})