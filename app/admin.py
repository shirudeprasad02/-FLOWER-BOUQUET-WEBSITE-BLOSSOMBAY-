from django.contrib import admin

from app.models import Flower
# from app.models import CustomUser
# Register your models here.
class FlowerAdmin(admin.ModelAdmin):
    list_display=['id','fname','price','is_active','cat',]
    list_filter=['cat','is_active','price']
    

admin.site.register(Flower,FlowerAdmin)


