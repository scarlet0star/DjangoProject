from django.shortcuts import redirect,render


def homeView(request):
    return render(request,'index.html')

def error400(request,exception=None):
    context = {}
    response = render(request, "error/400.html", context=context)
    response.status_code = 400
    return response

def error404(request,exception):
    context = {}
    response = render(request, "error/404.html", context=context)
    response.status_code = 404
    return response

def error500(request,exception=None):
    context = {}
    response = render(request, "error/500.html", context=context)
    response.status_code = 500
    return response