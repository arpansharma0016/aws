from django.contrib import admin

from .models import Product, Visitor_counter, Info, Confirm, Password, Banner, Widget, Tag

admin.site.register(Product)
admin.site.register(Visitor_counter)
admin.site.register(Info)
admin.site.register(Password)
admin.site.register(Confirm)
admin.site.register(Banner)
admin.site.register(Widget)
admin.site.register(Tag)

