from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows':3})
        }

    def __init__(self, *arg, **kwargs,):
        super().__init__(*arg, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'textarea w-1/3 textarea-primary'
                )
            })