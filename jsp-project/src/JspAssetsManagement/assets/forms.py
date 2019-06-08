from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Asset, Category

class AssetModelForm(forms.ModelForm):
    productName = forms.CharField(required=True, widget=forms.TextInput(
                                            attrs={"placeholder":" Product Name",
                                                    "style":"font-size: 20px"}))
    acquiredDate = forms.CharField(required=True, widget=forms.TextInput(
                                            attrs={"placeholder":" YY-MM-DD",
                                                    "style":"font-size: 15px"}))                                                                               
    description = forms.CharField(label='', widget=forms.Textarea(
                                            attrs={"style":"height: 70px!important", "cols":30}))
    class Meta:
        model = Asset
        fields =   ['productName',
                    'categoryName',
                    'model',
                    'serialNumber',
                    'acquiredDate',
                    'purchasePrice',
                    'condition',
                    'location',
                    'description',
                    'assetImage',
                    'rentStatus',
                    'assetMovement'
                    ]

    def __init__(self, *args, **kwargs):
        super(AssetModelForm, self).__init__(*args, **kwargs)
        self.fields['productName'].label = "Name "
        self.fields['productName'].widget.attrs.update({
                                                    "style":"margin-left: 10%"
                                                    }
                                                    )
        self.fields['productName'].help_text = "<i><small>Enter an asset name</small></i>"
        self.fields['categoryName'].label = "Category "
        self.fields['categoryName'].widget.attrs['style'] = "margin-left: 0px; display: inline; width: 300px"
        self.fields['model'].label = "Model: "
        self.fields['serialNumber'].label = "Serial Number "
        self.fields['serialNumber'].widget.attrs['style'] = "margin-left: 100px; display: inline; width: 300px"
        self.fields['acquiredDate'].label = "Date Acquired "
        self.fields['purchasePrice'].label = "Purchase Price "
        self.fields['purchasePrice'].widget.attrs['style'] = "margin-left: 0px; display: inline; width: 300px"
        self.fields['condition'].label = "Asset Condition "
        self.fields['location'].label = "Asset Location: "
        self.fields['location'].help_text = "<i><small>Where an asset is located</small></i>"
        self.fields['description'].label = "Description "
        self.fields['assetImage'].label = "Photo "

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryName']
        widget = {

        }
    
    def __init__(self, *args, **kwargs):
        super(CategoryModelForm, self).__init__(*args, **kwargs)
        self.fields['categoryName'].label = "Category: "
        self.fields['categoryName'].help_text = "<i>Enter a category name</i>"