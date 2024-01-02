from django.contrib import admin
from .models import Invoice, InvoiceDetails

admin.site.register(Invoice)
admin.site.register(InvoiceDetails)
