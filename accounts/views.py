from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def auth(request):
    if request.method == 'POST':
        if not request.POST.get('username', '') or not request.POST.get('password', ''):
            messages.error(request, 'Username or password cannot be empty!')
        else:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('patient.views.index'))
            else:
                messages.error(request, 'Incorrect username or password!')
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('patient.views.index'))
    return render(request, 'accounts/login.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts.views.auth'))