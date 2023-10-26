from django import forms

from .models import ChatMessages



class ChatMessagesForm(forms.ModelForm):
    class Meta:
        model = ChatMessages
        fields = ("content",)
        widgets = { 
            'content':forms.Textarea(attrs={
                'class': "w-full py-4 px-6 rounded-xl border"
            }),
        }
    

