from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager



class PostManager(models.Manager):

	def get_queryset(self):
		return super(PostManager,self).get_queryset().filter(status='published')


class Post(models.Model):

	STATUS_CHOICES = (
		('draft','Draft'),
		('published','Published')
		)

	title   = models.CharField(max_length=20)
	author  = models.ForeignKey(User , on_delete=models.CASCADE , related_name='blog_posts')
	body    = models.TextField()
	slug    = models.SlugField(max_length=50 , unique_for_date='publish')
	publish = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	status  = models.CharField(max_length=20 , choices=STATUS_CHOICES , default='draft')
	tags    = TaggableManager()


	class Meta:

		ordering = ('-publish',)

	objects 	= models.Manager()
	published 	= PostManager()

	def get_absolute_url(self):

		return reverse('blog:post_detail' , args=[self.publish.year,
												  self.publish.month,
												  self.publish.day,
												  self.slug])



class Comment(models.Model):

	name 	= models.CharField(max_length=20)
	email 	= models.EmailField()
	content = models.TextField()
	post    = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments")
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return f"Comment by {self.post.author} on {self.post.title}"
