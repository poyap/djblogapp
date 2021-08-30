from django import template
from ..models import Article
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

@register.inclusion_tag('articles/latest_artilce_list.html')
def get_latest_articles(count=3):
    latest_articles = Article.objects.order_by('-released_date')[:count]
    return {'latest_articles':latest_articles}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
