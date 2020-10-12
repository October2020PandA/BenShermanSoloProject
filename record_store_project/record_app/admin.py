from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(User)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(Order)
admin.site.register(Payment)
