from django.shortcuts import render , get_object_or_404
from .models import Post
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.core.mail import send_mail
from .forms import PostShareForm , CommentForm, SearchForm
from django.conf import settings
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector , SearchQuery , TrigramSimilarity


def post_list(request,tag_slug=None):

	object_list = Post.published.all()

	form = SearchForm()
	query = None
	results = []

	if 'query' in request.GET:

		form = SearchForm(data=request.GET)

		if form.is_valid():

			query = form.cleaned_data['query']
			search_vactor = SearchVector('title' , weight='A') + SearchVector('body',weight='B')
			search_query  = SearchQuery(query)
			object_list = Post.published.annotate(similarity=TrigramSimilarity('title',query)).filter(similarity__gt=0.3).order_by('-similarity')

	
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag , slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])	

	paginator 	= Paginator(object_list,3)
	page 	  	= request.GET.get('page')

	try:
		posts = paginator.page(page)
	except EmptyPage:
		posts = paginator.page(1)
	except PageNotAnInteger:
		posts = paginator.page(paginator.num_pages)

	return render(request , 'blog/list.html' , {'page':page,
												'posts':posts,
												'tag':tag,
												'form':form,
												'query':query})


def post_detail(request , year , month , day , post , tag_slug=None):

	post = get_object_or_404(Post, slug=post ,
											   publish__year=year,
											   publish__month=month,
											   publish__day=day,
											   status='published')



	list_tags_ids = post.tags.values_list('id' , flat=True)
	similar_posts = Post.published.filter(tags__in=list_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.order_by('-publish')


	comments = post.comments.all()
	new_comment = None

	if request.POST:

		form = CommentForm(data=request.POST)

		if form.is_valid():

			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		form = CommentForm()




	return render(request , 'blog/detail.html' , {'post':post,
												  'new_comment':new_comment,
												  'form':form,
												  'comments':comments,
												  'similar_posts':similar_posts})


def post_share(request , post_id):

	post = get_object_or_404(Post , id=post_id, status='published')

	sent = False

	if request.POST:

		form = PostShareForm(data=request.POST)

		if form.is_valid():
			post_url = request.build_absolute_uri(post.get_absolute_url())

			cd = form.cleaned_data

			subject = f"{cd['name']} {cd['email']} recommends you reading {post.title}"
			message = f"Read {post.title} via {post_url}\n comments:\n {cd['comment']}"
			send_mail(subject , message , settings.EMAIL_HOST_USER , [cd['to']] , fail_silently=False)
			snet    =True

	else:
		form = PostShareForm()

	return render(request , 'blog/share.html' , {'post':post,
												 'form':form,
												 'sent':sent})