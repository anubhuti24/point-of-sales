from django.contrib import admin
from .models import Product, Customer, Bill, BillDetail


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "product_price", "description")


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "phone_number", "email")


class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_amount")


class BillDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "bill", "product", "quantity")


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(BillDetail, BillDetailAdmin)
