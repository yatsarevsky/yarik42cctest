from django.contrib import admin

from yaproject.vcard.models import VCard, EntryLog


admin.site.register(VCard)
admin.site.register(EntryLog)
