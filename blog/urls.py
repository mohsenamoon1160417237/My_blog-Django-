from django.urls import path
from . import views


urlpatterns = [

	path('' , views.post_list , name='post_list'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/' , views.post_detail , name='post_detail'),
	path('Share/<int:post_id>/' , views.post_share , name='post_share'),
	path('tags/<slug:tag_slug>/',views.post_list , name="post_list_by_tag"),


]