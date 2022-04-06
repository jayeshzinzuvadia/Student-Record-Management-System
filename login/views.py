from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.
def manageLogin(request):
    """
    Renders get login page and post login page redirection
    """
    if request.method == 'POST':
        usernm = request.POST.get('usernm')
        passwd = request.POST.get('passwd')
        # NOT A GOOD WAY as UNAME and PASSWD are hardcoded
        # But it's fine for this requirement
        if usernm == "user1" and passwd == "user10702":
            request.session['isAuthenticated'] = True
            return HttpResponseRedirect(reverse('student:allstudentslist'))
        return render(request, "view_login.html", {'invalidUser':'True'})
    return render(request, "view_login.html")

def manageLogout(request):
    """
    Log out user
    """
    if 'isAuthenticated' in request.session:
        del request.session['isAuthenticated']
    return HttpResponseRedirect(reverse('login:login'))