from django.db import models

class Category(models.Model):
    categoryName = models.CharField(max_length=30)

    def __str__(self):
        return self.categoryName

# Create your models here.
class Asset(models.Model):
    productName = models.CharField(max_length=100)
    # categoryName = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    choices_categoryName = (
                ('', '*************Choose Category************'),
                ('Laptops', 'Laptops'),
                ('Printers', 'Printers'),
                ('Furniture', 'Furniture'),
                ('Cars', 'Cars'),
                ('Trucks', 'Trucks'),
                ('Others', 'Others')
            )
    categoryName = models.CharField(max_length=30, choices=choices_categoryName, null=False, blank=False)
    model = models.CharField(max_length=30, blank=True)
    serialNumber = models.CharField(max_length=40, blank=True)
    acquiredDate = models.DateTimeField(null=True, blank=True)
    purchasePrice = models.FloatField(null=True, blank=True)
    condition = models.CharField(max_length=30,blank=True)
    location = models.CharField(max_length=30, blank=True)
    description = models.TextField(null=True, blank=True)
    assetImage = models.ImageField(null=True, blank=True)
    choices_rentStatusChoice = (
        ('Not Rented', '****Not Rented****'),
        ('Rented', 'This Asset is rented')
    )
    rentStatus = models.CharField(max_length=30, choices=choices_rentStatusChoice, default='Not Rented')
    choices_movementStatus = (
        ('No', '*******No*******'),
        ('Yes', 'Asset in Motion')
    )
    assetMovement = models.CharField(max_length=30, choices=choices_movementStatus, default='No')

    def get_absolute_url(self):
        return f"/asset/{self.id}"

    def get_absolute_delete_url(self):
        return f"/{self.id}/delete/"
    
    def get_absolute_update_url(self):
        return f"/{self.id}/update/"

    def __str__(self):
        return self.productName




