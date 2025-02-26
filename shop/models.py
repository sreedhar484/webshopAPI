from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    category_values = (('clothing', 'Clothing'), ('shoes', 'Shoes'),('electronic', 'Electronic'), ('books', 'Books'))
    product_category = models.CharField(max_length=100, choices=category_values, default='clothing')
    def __str__(self):
        return self.name
    

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.stock_quantity} in stock"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    address = models.CharField(max_length=1000,default="null")
    city = models.CharField(max_length=1000,default="null")
    zip_code = models.CharField(max_length=1000,default="null")
    country = models.CharField(max_length=1000,default="null")
    payment_method = models.CharField(max_length=1000,default="null")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} - {self.status}"

# Order Item Model (Many-to-Many between Order & Product)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
