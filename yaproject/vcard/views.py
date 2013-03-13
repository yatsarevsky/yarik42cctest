from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from yaproject.vcard.models import VCard, RequestStore
from yaproject.vcard.forms import (MemberAccountForm, VCardForm,
                                   RequestStoreFormSet)


def contacts(request):
    contacts = VCard.objects.get(pk=1)
    return render_to_response('vcard/vcard_detail.html',
        {'contacts': contacts}, RequestContext(request))


def requests_store(request):
    requests = RequestStore.objects.all()
    formset = RequestStoreFormSet(queryset=requests)

    if request.POST:
        formset = RequestStoreFormSet(request.POST)

    if formset.is_valid():
        formset.save()
        return redirect('requests')

    return render_to_response('requests.html',
        {'requests': requests, 'formset': formset},
        RequestContext(request))


@login_required(login_url='/login/')
def edit_page(request):
    instance = VCard.objects.get(pk=1)
    form = VCardForm(instance=instance)

    if request.POST:
        form = VCardForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()

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
