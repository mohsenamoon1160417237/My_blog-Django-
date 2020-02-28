from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(num=3):

	latest_posts = Post.published.order_by('-publish')[:num]

	return {'latest_posts':latest_posts}

@register.inclusion_tag('most_commented_posts.html')
def get_most_commented_posts(num=3):

	most_commented_posts = Post.published.annotate(total_comments=Count('comments'))
	most_commented_posts = most_commented_posts.order_by('-total_comments','-publish')[:num]
	return {'most_commented_posts':most_commented_posts}

@register.filter(name='markdown')
def markdown_format(text):

	return mark_safe(markdown.markdown(text))