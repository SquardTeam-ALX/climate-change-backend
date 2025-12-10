from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capital = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    abbreviation = models.CharField(max_length=5, blank=True, null=True)  # e.g. LA for Lagos

    class Meta:
        ordering = ['name']
        verbose_name_plural = "States"

    def __str__(self):
        return self.name