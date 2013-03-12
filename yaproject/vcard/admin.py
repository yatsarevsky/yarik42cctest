from django.contrib import admin

from yaproject.vcard.models import VCard, EntryLog, RequestStore


class RequestStoreAdmin(admin.ModelAdmin):
    class Meta:
        ordering = ('priority', )

    list_editable = ('priority',)
    list_filter = ('priority',)
    list_display = ('host', 'path', 'date', 'priority')


admin.site.register(VCard)
admin.site.register(EntryLog)
admin.site.register(RequestStore, RequestStoreAdmin)
