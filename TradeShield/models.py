from django.db import models

'''Add a simple model to store route data (optional, for caching or future use)'''
class SupplyChainRoute(models.Model):
    origin_country = models.CharField(max_length=100)
    destination_country = models.CharField(max_length=100)
    route_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin_country} to {self.destination_country}"