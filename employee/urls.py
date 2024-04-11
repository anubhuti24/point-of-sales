from django.contrib import admin
from django.urls import path
from .views import EmployeeRegistration, EmployeeLogin, AddProduct, UpdateRemoveProduct, AddCustomer, UpdateRemoveCustomer, CustomerBill, GetBill

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", EmployeeRegistration.as_view()),
    path("login/", EmployeeLogin.as_view()),
    path("add-product/", AddProduct.as_view()),
    path("edit-remove-product/<int:pk>/", UpdateRemoveProduct.as_view()),
    path("add-customer/", AddCustomer.as_view()),
    path("update-remove-customer/<int:pk>/", UpdateRemoveCustomer.as_view()),
    path("generate-bill/", CustomerBill.as_view()),
    path("get-bill-details/<int:pk>/", GetBill.as_view()),
]