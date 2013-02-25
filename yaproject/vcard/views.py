from django.shortcuts import render_to_response
from django.template.context import RequestContext

from yaproject.vcard.models import VCard


def contacts(request):
    contacts = VCard.objects.get(pk=1)

    return render_to_response('vcard/vcard_detail.html',
                              {'contacts': contacts},
                              RequestContext(request))
