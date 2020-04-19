from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')


def fault(request, fault):
    return render(request, 'fault.html', {'fault': fault})


def success(request, msg):
    return render(request, 'success.html', {'msg': msg})