from django.db import models

class Asset(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OHLCV(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='ohlcv_data')
    timestamp = models.DateTimeField()
    open = models.DecimalField(max_digits=20, decimal_places=8)
    high = models.DecimalField(max_digits=20, decimal_places=8)
    low = models.DecimalField(max_digits=20, decimal_places=8)
    close = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=30, decimal_places=10)

    class Meta:
        unique_together = ('asset', 'timestamp')
        ordering = ['-timestamp']
