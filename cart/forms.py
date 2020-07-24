from django.utils.translation import gettext_lazy as _
from django import forms

#限制用户选择的数量为1-20
PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int,label=_('商品数量'))
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)

