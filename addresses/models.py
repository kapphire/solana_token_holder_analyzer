from django.db import models


class Address(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100)

    class Meta:
        ordering = ['created']
