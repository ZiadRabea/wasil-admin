from django.db import models

# Create your models here.

class Lead(models.Model):
    name = models.CharField(max_length=100)
    order = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=100)
    order_type = models.CharField(max_length=10)
    states = (("Lead", "Lead"),("Prospect", "Prospect"), ("Customer", "Customer"))
    state = models.CharField(choices=states, max_length=10)
    governorate = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-created_at"]
    