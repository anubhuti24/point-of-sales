from django.contrib.auth.models import User
from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Customer, Bill, BillDetail
from .serializers import EmployeeSerializer, AddProductSerializer, CustomerSerializer, BillSerializer, BillDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from drf_spectacular.utils import extend_schema


class EmployeeRegistration(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmployeeSerializer
    queryset = User.objects.all()


class EmployeeLogin(CreateAPIView):
    permission_classes = [AllowAny]

    @extend_schema(request=EmployeeSerializer, responses={200: EmployeeSerializer})
    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            login(request, user)
            return Response(
                {
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            # If authentication fails, return an error response
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class AddProduct(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddProductSerializer
    queryset = Product.objects.all()

    @extend_schema(responses={200: AddProductSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(request=AddProductSerializer, responses={201: AddProductSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateRemoveProduct(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddProductSerializer
    queryset = Product.objects.all()

    @extend_schema(request=AddProductSerializer, responses={200: AddProductSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(request=AddProductSerializer, responses={200: AddProductSerializer})
    def put(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(responses={204: None})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AddCustomer(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    @extend_schema(responses={200: CustomerSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(request=CustomerSerializer, responses={201: CustomerSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateRemoveCustomer(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    @extend_schema(request=CustomerSerializer, responses={200: CustomerSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(request=CustomerSerializer, responses={200: CustomerSerializer})
    def put(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(responses={204: None})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CustomerBill(CreateAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=BillDetailSerializer, responses={201: BillSerializer})
    def post(self, request):
        customer_id = request.data.get('customer_id')
        products = request.data.get('products')

        customer = get_object_or_404(Customer, id=customer_id)

        total_amount = 0
        bill = Bill.objects.create(customer=customer, total_amount=total_amount)

        for item in products:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            product = get_object_or_404(Product, id=product_id)
            subtotal = product.product_price * quantity
            total_amount += subtotal

            BillDetail.objects.create(bill=bill, product=product, quantity=quantity)

        bill.total_amount = total_amount
        bill.save()

        bill_serializer = BillSerializer(bill)

        return Response(bill_serializer.data, status=201)


class GetBill(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BillSerializer
    queryset = Bill.objects.all()

    @extend_schema(responses={200: BillSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


