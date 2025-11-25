# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer
from django.http import JsonResponse


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    '''
        data = request.data
        product = Product.objects.order_by("?").first()
        if not product:
            return Response({})

    data = ProductSerializer(product).data

    '''    
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        #instance itself
        data=serializer.save()
        print(data)
        #data=serializer.data
    return Response(serializer.data)
