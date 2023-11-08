from django.contrib import admin

from .models import Entry, Owner, Stick, Storage, SeedTypes, Gateway
# Register your models here.


admin.site.register(Entry)
admin.site.register(Owner)
admin.site.register(Storage)
admin.site.register(Stick)
admin.site.register(SeedTypes)
admin.site.register(Gateway)
