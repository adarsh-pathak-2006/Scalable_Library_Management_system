from django.contrib import admin
from .models import Cart, CartBook, Issue, IssuedBook

admin.site.register(Cart)
admin.site.register(CartBook)
admin.site.register(Issue)
admin.site.register(IssuedBook)