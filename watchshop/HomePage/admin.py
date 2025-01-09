from django.contrib import admin
from.models import Watches,RatingComment

# Register your models here.
@admin.register(Watches)
class WatchesAdmin(admin.ModelAdmin):
    list_display =('id','name','price')
    search_filed =('name',)
    ordering = ('upload_date',)
    list_filter = ('price',)

@admin.register(RatingComment)
class RatingCommentAdmin(admin.ModelAdmin)  :
    list_display = ("product","user","rating","comment","created_on")
