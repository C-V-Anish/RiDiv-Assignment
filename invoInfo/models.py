from django.db import models
from django.core.validators import MinValueValidator

class Invoice(models.Model) :
    date = models.DateField()
    customer_name = models.CharField(max_length = 64)

    def __str__(self):
        return self.customer_name
    
class InvoiceDetails(models.Model) :
    invoice = models.ForeignKey(Invoice, on_delete = models.CASCADE, related_name = 'bill')
    description = models.CharField(max_length = 512)
    quantity = models.IntegerField(validators=[MinValueValidator(limit_value=1)], default = 0)
    unit_price = models.IntegerField(validators = [MinValueValidator(limit_value=1)])
    price = models.IntegerField(validators = [MinValueValidator(limit_value=1)])

    def save(self, *args, **kwargs):
        self.price = self.unit_price * self.quantity
        
        if self.pk:
            max_id = InvoiceDetails.objects.filter(invoice=self.invoice).aggregate(models.Max('id'))['id__max'] or 0
            self.id = max_id + 1

        super(InvoiceDetails, self).save(*args, **kwargs)

    def __str__(self):
        return self.description
