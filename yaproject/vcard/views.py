from django.shortcuts import render_to_response, redirect, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from yaproject.vcard.models import VCard, RequestStore
from yaproject.vcard.forms import MemberAccountForm, VCardForm

import json


def contacts(request):
    contacts = VCard.objects.get(pk=1)
    return render_to_response('vcard/vcard_detail.html',
        {'contacts': contacts}, RequestContext(request))


def requests_store(request):
    requests = RequestStore.objects.all().order_by('id')[:10]
    return render_to_response('requests.html',
        {'requests': requests}, RequestContext(request))


@login_required(login_url='/login/')
def edit_page(request):
    instance = VCard.objects.get(pk=1)
    form = VCardForm(instance=instance)

    if request.POST:
        form = VCardForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()

            if request.is_ajax():
                return HttpResponse(json.dumps({'ok': True}),
                    content_type='application/json')

    return render_to_response('vcard/edit_vcard.html',
        {'form': form}, RequestContext(request))


def accounts_registration(request):
    form = MemberAccountForm()

    if request.POST:
        form = MemberAccountForm(request.POST)

        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'],
                password=request.POST['password'])
            login(request, user)
            return redirect('home')

    return render_to_response('accounts/signup_member.html',
        {'form': form}, RequestContext(request))
