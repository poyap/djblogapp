from django.contrib import admin
from .models import Article, Profile, Comment
# Register your models here.
class Articlelist(admin.ModelAdmin):
    list_display = ['title','user','released_date']
    list_filter = ['released_date']
    search_fields = ['title']

class Commentlist(admin.ModelAdmin):
    list_display = [ 'name','email' ,'created','active']
    list_filter  = [ 'active', 'name']
    search_fields = ['post']
    
admin.site.register(Article,Articlelist)
admin.site.register(Profile)
admin.site.register(Comment, Commentlist)





