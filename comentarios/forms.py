from django.forms import ModelForm
from .models import Comment
from django.conf import settings
import requests


class FormComment(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            attr_update = {
                "class": "form-control"
            }
            self.fields[str(field)].widget.attrs.update(attr_update)

    def clean(self):
        raw_data = self.data

        # Get reCaptcha response
        recaptcha_response = raw_data.get('g-recaptcha-response')

        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.SECRET_KEY_RECAPTCHA,
                'response': recaptcha_response
            }
        )
        recaptcha_result = recaptcha_request.json()

        if not recaptcha_result.get('success'):
            self.add_error(
                'comment',
                'Confirme que você não é um robô.'
            )

        cleaned_data = self.cleaned_data
        name = cleaned_data.get('comment_name')
        email = cleaned_data.get('comment_email')
        comment = cleaned_data.get('comment')

        # Name need to have at least 5 chars
        if len(name) < 5:
            self.add_error(
                'comment_name',
                'Nome precisa ter mais que 5 caracteres.'
            )

    class Meta:
        model = Comment
        fields = ('comment_name', 'comment_email', 'comment')
