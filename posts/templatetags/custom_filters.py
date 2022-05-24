from django import template

register = template.Library()


@register.filter(name='comment_plural')
def comment_plural(comments_number):
    try:
        comments_number = int(comments_number)
        if comments_number >= 2:
            return f'{comments_number} Comentários'
        elif comments_number == 0:
            return f'Sem comentários'
        else:
            return f'{comments_number} Comentário'
    except:
        return f'{comments_number} Comentário(s)'
