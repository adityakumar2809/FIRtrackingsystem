from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def create_fir(request):
    return render(request, 'firBeta/create_fir.html', {})
