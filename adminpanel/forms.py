from django import forms
from product.models import Productimage

class ImageForm(forms.ModelForm):
    class Meta:
        model = Productimage
        fields = ('image',)