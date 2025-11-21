from django.http import HttpResponseBadRequest
from django.shortcuts import render

def home_view(request):
    return render(request, "home.html", {"name": "Sudharsana"})


def about_view(request):
    return HttpResponse("Trying to create another page ;) ")


def add_view(request):
    num1 = request.GET.get("num1")
    num2 = request.GET.get("num2")
    a = float(num1)
    b = float(num2)
    result = a + b

    return render(request, "result.html", {"result": result})
