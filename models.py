from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def str(self):
        return self.name

# الجدول الجديد لسجل الحركات
class Transaction(models.Model):
    TYPES = (('IN', 'وارد'), ('OUT', 'صادر'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPES)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.product.name} - {self.type} - {self.amount}"