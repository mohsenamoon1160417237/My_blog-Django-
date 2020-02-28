from django.contrib import admin
from .models import Post ,Comment


class PostAdmin(admin.ModelAdmin):

	list_display 		= ('title','author','publish','status','updated')
	list_filter  		= ('status','title','author' , 'publish')
	date_hierarchy 		= 'publish'
	prepopulated_fields = {'slug':('title',)}
	search_fields  		= ('title','author')
	raw_id_fields    	= ('author',)


admin.site.register(Post , PostAdmin)
admin.site.register(Comment)


