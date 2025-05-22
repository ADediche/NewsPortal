from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'category',
           'title',
           'text',
       ]

   def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("description")
        text = cleaned_data.get("text")
        if title is not None and len(title) > 100:
            raise ValidationError({
                "tetle": "Заголовок не может быть более 100 символов."
            })
        if text is not None and len(text) > 5000:
            raise ValidationError({
                "text": "Текст не может быть более 5000 символов."
            })
        return cleaned_data