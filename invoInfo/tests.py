from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Invoice, InvoiceDetails

class InvoiceAPITestCase(APITestCase):

    def setUp(self):
        self.invoice_data = {'date': '2022-01-01', 'customer_name': 'Test Customer'}
        self.invoice = Invoice.objects.create(**self.invoice_data)
        self.invoice_details_data = {'invoice': self.invoice, 'description': 'Test Item', 'quantity': 1, 'unit_price': 10, 'price': 10}
        self.invoice_details = InvoiceDetails.objects.create(**self.invoice_details_data)

    def test_create_invoice(self):
        url = reverse('invoice-list')
        data = {'date': '2022-01-02', 'customer_name': 'New Customer', 'bill': [{'description': 'Item 1', 'quantity': 2, 'unit_price': 5, 'price': 10}]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(InvoiceDetails.objects.count(), 2)

    def test_retrieve_invoice(self):
        url = reverse('invoice-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for invoice_data in response.data:
            self.assertEqual(invoice_data['customer_name'], self.invoice_data['customer_name'])

    def test_update_invoice(self):
        url = reverse('invoice-detail', args=[self.invoice.id])

        updated_date = "2024-01-02"
        updated_customer_name = "Updated Customer"
        updated_description = "Updated Item"
        updated_quantity = 3
        updated_unit_price = 15
        updated_price = updated_quantity * updated_unit_price

        data = { 
            'date': updated_date,
            'customer_name': updated_customer_name,
            'bill': [{
                'id': self.invoice_details.id,
                'description': updated_description,
                'unit_price': updated_unit_price,
                'quantity': updated_quantity,
                'price': updated_price
            }]
        }

        response = self.client.patch(url, data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.invoice.refresh_from_db()
        self.invoice_details.refresh_from_db()

        self.assertEqual(self.invoice.customer_name, updated_customer_name)

        updated_invoice_details = self.invoice.bill.get(id=self.invoice_details.id)
        self.assertEqual(updated_invoice_details.description, updated_description)
        self.assertEqual(updated_invoice_details.quantity, updated_quantity)
        self.assertEqual(updated_invoice_details.unit_price, updated_unit_price)
        self.assertEqual(updated_invoice_details.price, updated_price)

    def test_delete_invoice(self):
        url = reverse('invoice-detail', args=[self.invoice.id])
        
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceDetails.objects.count(), 1)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(InvoiceDetails.objects.count(), 0)