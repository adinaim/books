from rest_framework import serializers

from .models import (
    BookPurchase, 
    OrderItems
    )


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['book', 'book_num']


class BookPurchaseSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True) 

    class Meta:
        model = BookPurchase
        fields = ['order_id', 'created_at', 'total_sum', 'items']

    def create(self, validated_data, *args, **kwargs):
        items = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = super().create(validated_data) 
        total_sum = 0
        orders_items = []

        for item in items:
            tickets = (OrderItems(
                order=order,
                book=item['book'],
                book_num=item['book_num']
            ))
            orders_items.append(tickets)

            if item['book'].book_count >= item['book_num']:
                item['book'].book_count -= item['book_num']

                total_sum += item['book'].price_som * item['book_num']
                
                OrderItems.objects.bulk_create(orders_items, *args, **kwargs)
                order.total_sum = total_sum

                # order.create_code() ###
                item['book'].save()
                order.save()

                return order
            else:
                raise serializers.ValidationError('We do not have so many books')
    

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPurchase
        fields = ('order_id', 'total_sum', 'status', 'created_at', 'book')