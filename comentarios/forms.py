from django .forms import ModelForm
from .models import Comment


class FormComment(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_name', 'comment_email', 'comment')