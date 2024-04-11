from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Customer, Bill, BillDetail


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user

    class Meta:
        model = User
        fields = ["username", "password"]


class AddProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = ["id", "product_name", "product_price", "description", "user"]


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
        partial = True


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'customer', 'total_amount', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class BillDetailSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    products = ProductSerializer(many=True)

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        products_data = validated_data.pop('products')
        bill = Bill.objects.create(customer_id=customer_id, total_amount=0)

        total_amount = 0
        for product_data in products_data:
            product_id = product_data['product_id']
            quantity = product_data['quantity']

            product = get_object_or_404(Product, id=product_id)
            subtotal = product.product_price * quantity
            total_amount += subtotal

            BillDetail.objects.create(bill=bill, customer_id=customer_id, product=product, quantity=quantity)

        bill.total_amount = total_amount
        bill.save()

        return bill
