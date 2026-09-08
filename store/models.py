from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    description=models.TextField()
    quantity=models.PositiveIntegerField()
    is_avaliable=models.BooleanField(default=True)
    added_on=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.is_avaliable=True
        else:
            self.is_avaliable=False
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

