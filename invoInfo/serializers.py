from rest_framework import serializers
from .models import Invoice, InvoiceDetails

class InvoiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetails
        fields = ['id', 'description', 'unit_price', 'quantity', 'price' ]

class InvoiceSerializer(serializers.ModelSerializer):
    bill = InvoiceDetailsSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'date', 'customer_name', 'bill']

    def create(self, validated_data):
        details_data = validated_data.pop('bill', [])
        invoice = Invoice.objects.create(**validated_data)
        
        for detail_data in details_data:
            detail_data['invoice'] = invoice
            InvoiceDetails.objects.create(**detail_data)

        return invoice

    def update(self, instance, validated_data):
        details_data = validated_data.pop('bill', [])
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        existing_detail_ids = set()

        for detail_data in details_data:
            detail_id = detail_data.get('id', None)

            if detail_id:
                detail_instance = InvoiceDetails.objects.filter(id=detail_id, invoice=instance).first()

                if detail_instance:
                    detail_instance.description = detail_data.get('description', detail_instance.description)
                    detail_instance.quantity = detail_data.get('quantity', detail_instance.quantity)
                    detail_instance.unit_price = detail_data.get('unit_price', detail_instance.unit_price)
                    detail_instance.price = detail_data.get('price', detail_instance.price)
                    detail_instance.save()

                    existing_detail_ids.add(detail_instance.id)

        for detail_data in details_data:
            detail_id = detail_data.get('id', None)

            if not detail_id:
                detail_data['invoice'] = instance
                new_detail = InvoiceDetails.objects.create(**detail_data)
                existing_detail_ids.add(new_detail.id)

        instance.bill.exclude(id__in=existing_detail_ids).delete()

        return instance

