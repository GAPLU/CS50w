from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.IntegerField(min_value=1)
    image_url = forms.CharField(required=False)
    category = forms.CharField(max_length=64, required=False)


class Comment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label='')
