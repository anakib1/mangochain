from django.shortcuts import render

# Create your views here.
# messages/views.py
from rest_framework import generics
from .models import Block, User, Transaction
from .serializers import BlockSerializer, UserSerializer, TransactionSerializer
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


# class BlockListCreateAPIView(generics.ListCreateAPIView):
#   queryset = Block.objects.all()
#  serializer_class = BlockSerializer

@csrf_exempt
def store_block(request):
    if request.method == 'POST':
        try:
            block_data = json.loads(request.body.decode('utf-8'))
            block_json = json.dumps(block_data)  # Ensure the received data is re-serialized
            Block.objects.create(content=block_json)
            return JsonResponse({'message': 'Block stored successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    elif request.method == 'GET':
        blocks = Block.objects.all()
        block_json_list = []

        for block in blocks:
            try:
                block_data = block.content
                block_json_list.append(block_data)
            except json.JSONDecodeError:
                # Handle invalid JSON format in stored data
                pass

        return JsonResponse(block_json_list, safe=False)
    else:
        return JsonResponse({'error': 'Only POST and GET requests are allowed'})


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
