from rest_framework import viewsets
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework.response import Response
from rest_framework import status

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    http_method_names = ['get','post','put','patch', 'delete']
