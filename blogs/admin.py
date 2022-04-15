from django.contrib import admin
from .models import Post, Category,Contact, BlogComment, IpModel, SubcribeUsers
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_title',)
    icon_name = 'apps'

# class CommentAdmin(admin.ModelAdmin):
#     list_display =('post','username')
class ContactAdmin(admin.ModelAdmin):
    list_display=("name","email","phone")
    icon_name='contact_phone'

class PostAdmin(admin.ModelAdmin):
    list_display = ('image_tag','title','post_date',)
    search_fields = ('tags',)
    list_filter= ('category','title',)
    list_per_page = 8
    icon_name='add_to_photos'

class SubAdmin(admin.ModelAdmin):
    icon_name='verified_user'
    list_display=('email','date')

class blgAdmin(admin.ModelAdmin):
    icon_name='message'
    list_display=('user','timestamp')

admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(BlogComment,blgAdmin)
admin.site.register(IpModel)

admin.site.register(SubcribeUsers,SubAdmin)
