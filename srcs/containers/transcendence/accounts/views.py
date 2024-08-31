from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

@login_required
def redirect_to_2fa_setup(request):
    print("redirect_to_2fa_setup...")
    setup_url = reverse('two_factor:setup')  # Adjust this if the URL name is different
    return JsonResponse({'setup_url': setup_url})

