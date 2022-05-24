from django.forms import ModelForm
from .models import Comment


class FormComment(ModelForm):
    def clean(self):
        data = self.cleaned_data
        name = data.get('comment_name')
        email = data.get('comment_email')
        comment = data.get('comment')

        # Name need to have at least 5 chars
        if len(name) < 5:
            self.add_error(
                'comment_name',
                'Nome precisa ter mais que 5 caracteres.'
            )

    class Meta:
        model = Comment
        fields = ('comment_name', 'comment_email', 'comment')
