from django.db import models
import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First name is required"
        elif len(postData['first_name']) < 2 or postData['first_name'].isalpha() != True:
            errors['first_name'] = "First name must be at least 2 characters, letters only"
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last name is required"
        elif len(postData['last_name']) < 2 or postData['last_name'].isalpha() != True:
            errors['last_name'] = "Last name must be at least 2 characters, letters only"
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address"
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) > 0:
            errors['email'] = "Email already in use"
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match"
        return errors
        
    def log_in_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif len(existing_user) != 1:
            errors['email'] = "User not found"
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        if existing_user:
            logged_user = existing_user[0]
            if bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
                errors['email'] = "Email and password do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BillingAddressManager(models.Manager):
    def billing_address_validator(self, postData):
        errors = {}
        if len(postData['billing_first_name']) == 0:
            errors['billing_first_name'] = "Billing First name is required"
        elif len(postData['billing_first_name']) < 2 or postData['billing_first_name'].isalpha() != True:
            errors['billing_first_name'] = "First name must be at least 2 characters, letters only"
        if len(postData['billing_last_name']) == 0:
            errors['billing_last_name'] = "Billing Last name is required"
        elif len(postData['billing_last_name']) < 2 or postData['billing_last_name'].isalpha() != True:
            errors['billing_last_name'] = "Last name must be at least 2 characters, letters only"
        if len(postData['billing_street_address']) == 0:
            errors['billing_street_address'] = "Street address is required"
        elif len(postData['billing_street_address']) < 2:
            errors['billing_street_address'] = "Street address must be at least 2 characters"
        if len(postData['billing_city']) == 0:
            errors['billing_city'] = "City is required"
        elif len(postData['billing_city']) < 2 or postData['billing_city'].isalpha() != True:
            errors['billing_city'] = "City must be at least 2 characters, letters only"
        if len(postData['billing_state']) == 0:
            errors['billing_state'] = "State is required"
        elif len(postData['billing_state']) != 2 or postData['billing_state'].isalpha() != True:
            errors['billing_state'] = "State must be exactly 2 characters, letters only"
        if len(postData['billing_zip_code']) == 0:
            errors['billing_zip_code'] = "Zip code is required"
        elif len(postData['billing_zip_code']) != 5 or postData['billing_zip_code'].isalpha() == True:
            errors['billing_zip_code'] = "Zip must be exactly 5 characters, numbers only"
        return errors

class BillingAddress(models.Model):
    STATE_CHOICES = (
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
    )
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=None)
    zip_code = models.IntegerField()
    charge_to = models.ManyToManyField(User, related_name="billing_address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BillingAddressManager()


class ShippingAddressManager(models.Manager):
    def shipping_address_validator(self, postData):
        errors = {}
        if len(postData['shipping_first_name']) == 0:
            errors['shipping_first_name'] = "First name is required"
        elif len(postData['shipping_first_name']) < 2 or postData['shipping_first_name'].isalpha() != True:
            errors['shipping_first_name'] = "First name must be at least 2 characters, letters only"
        if len(postData['shipping_last_name']) == 0:
            errors['shipping_last_name'] = "Last name is required"
        elif len(postData['shipping_last_name']) < 2 or postData['shipping_last_name'].isalpha() != True:
            errors['shipping_last_name'] = "Last name must be at least 2 characters, letters only"
        if len(postData['shipping_street_address']) == 0:
            errors['shipping_street_address'] = "Street address is required"
        elif len(postData['shipping_street_address']) < 2:
            errors['shipping_street_address'] = "Street address must be at least 2 characters"
        if len(postData['shipping_city']) == 0:
            errors['shipping_city'] = "City is required"
        elif len(postData['shipping_city']) < 2 or postData['shipping_city'].isalpha() != True:
            errors['shipping_city'] = "City must be at least 2 characters, letters only"
        if len(postData['shipping_state']) == 0:
            errors['shipping_state'] = "State is required"
        elif len(postData['shipping_state']) != 2 or postData['shipping_state'].isalpha() != True:
            errors['shipping_state'] = "State must be exactly 2 characters, letters only"
        if len(postData['shipping_zip_code']) == 0:
            errors['shipping_zip_code'] = "Zip code is required"
        elif len(postData['shipping_zip_code']) != 5 or postData['shipping_zip_code'].isalpha() == True:
            errors['shipping_zip_code'] = "Zip must be exactly 5 characters, numbers only"
        return errors

class ShippingAddress(models.Model):
    STATE_CHOICES = (
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
    )
    first_name = models.CharField(max_length=60, default=None)
    last_name = models.CharField(max_length=60, default=None)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=None)
    zip_code = models.IntegerField()
    phone_number = models.IntegerField(default=None, blank=True, null=True)
    delivery_instructions = models.TextField(default=None, blank=True, null=True)
    residents = models.ManyToManyField(User, related_name="shipping_address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShippingAddressManager()

class ProductManager(models.Manager):
    def product_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = "Title is required"
        elif len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters"
        if len(postData['artist']) == 0:
            errors['artist'] = "Artist is required"
        elif len(postData['artist']) < 2:
            errors['artist'] = "Artist must be at least 2 characters"
        if len(postData['price']) == 0:
            errors['price'] = "Price is required"
        elif len(postData['price']) < 1:
            errors['price'] = "Price must be at least 1 characters"
        if len(postData['quantity']) == 0:
            errors['quantity'] = "Quantity is required"
        if len(postData['description']) == 0:
            errors['description'] = "Description is required"
        elif len(postData['description']) < 3:
            errors['description'] = "Description must be at least 3 characters"
        return errors


class Product(models.Model):
    GENRE_CHOICES = (
        ("BL", "Blues"),
        ("CO", "Country"),
        ("CL", "Classical"),
        ("HH", "Hip-Hop/Rap"),
        ("JZ", "Jazz"),
        ("RK", "Rock"),
        ("RB", "R&B/Soul"),
    )
    title = models.CharField(max_length=60)
    artist = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    album_art = models.ImageField(upload_to="album_art")
    description = models.TextField()
    genre = models.CharField(max_length=2, choices=GENRE_CHOICES, default=GENRE_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

class PaymentManager(models.Manager):
    def payment_validator(self, postData):
        errors = {}
        if len(postData['payment_first_name']) == 0:
            errors['payment_first_name'] = "Payment First name is required"
        elif len(postData['payment_first_name']) < 2 or postData['payment_first_name'].isalpha() != True:
            errors['payment_first_name'] = "First name must be at least 2 characters, letters only"
        if len(postData['payment_last_name']) == 0:
            errors['payment_last_name'] = "Payment Last name is required"
        elif len(postData['payment_last_name']) < 2 or postData['payment_last_name'].isalpha() != True:
            errors['shipping_last_name'] = "Last name must be at least 2 characters, letters only"
        if len(postData['card_number']) == 0:
            errors['card_number'] = "Card number is required"
        elif len(postData['card_number']) != 19 or postData['card_number'].isalpha() == True:
            errors['card_number'] = "Card number must be in 0000 0000 0000 0000 format, numbers only"
        if len(postData['expiration_date']) == 0:
            errors['expiration_date'] = "Expiration date is required"
        elif len(postData['expiration_date']) != 5 or postData['expiration'].isalpha() == True:
            errors['expiration_date'] = "Expiration date must be in 00/00 format, numbers only"
        if len(postData['security_code']) == 0:
            errors['security_code'] = "Security code is required"
        elif len(postData['security_code']) != 3 or postData['security_code'].isalpha() == True:
            errors['security_code'] = "Security code must be exactly 3 characters, numbers only"

class Payment(models.Model):
    first_name = models.CharField(max_length=60, default=None)
    last_name = models.CharField(max_length=60, default=None)
    card_number = models.CharField(max_length=19)
    expiration = models.CharField(max_length=5)
    security_code = models.CharField(max_length=3)
    card_owner = models.ForeignKey(User, related_name="payment_card", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PaymentManager()

class Order(models.Model):
    is_complete = models.BooleanField(default=False)
    ordered_by = models.ForeignKey(User, related_name="shopping_cart", on_delete=models.CASCADE)
    ship_to = models.ForeignKey(ShippingAddress, related_name="location_of", on_delete=models.CASCADE, null=True)
    charged_to = models.ForeignKey(Payment, related_name="charged_by", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
        
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total