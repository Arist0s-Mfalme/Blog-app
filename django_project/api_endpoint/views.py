from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def item_list(request):
    if request.method == 'GET':
        return JsonResponse({
            "message": "Hello from pure Django!",
            "status": "success"
        }, status=200)
