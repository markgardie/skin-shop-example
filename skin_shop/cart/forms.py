from django import forms

class AddToCartForm(forms.Form):
    skin_id = forms.IntegerField(widget=forms.HiddenInput())
    
class RemoveFromCartForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
