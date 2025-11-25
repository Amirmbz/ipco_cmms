from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey('plants.Plant', on_delete=models.CASCADE)
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.plant})"


class PartCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Part(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(PartCategory, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.CharField(max_length=50, default='pcs')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class PartStock(models.Model):
    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('USED', 'Used'),
        ('DAMAGED', 'Damaged'),
    ]

    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('part', 'warehouse', 'condition')

    def __str__(self):
        return f"{self.part} - {self.warehouse} ({self.condition})"


class PartTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
        ('TRANSFER', 'Transfer'),
    ]
    CONDITION_CHOICES = PartStock.CONDITION_CHOICES

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    warehouse_from = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_out')
    warehouse_to = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_in')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    quantity = models.IntegerField()
    work_order = models.ForeignKey('work_orders.WorkOrder', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.transaction_type} {self.part} ({self.quantity})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.apply_stock_change()

    def apply_stock_change(self):
        def adjust(part, warehouse, condition, delta):
            if warehouse is None:
                return
            stock, _ = PartStock.objects.get_or_create(part=part, warehouse=warehouse, condition=condition)
            stock.quantity = stock.quantity + delta
            stock.save()

        if self.transaction_type == 'IN':
            adjust(self.part, self.warehouse_to, self.condition, self.quantity)
        elif self.transaction_type == 'OUT':
            adjust(self.part, self.warehouse_from, self.condition, -self.quantity)
        elif self.transaction_type == 'TRANSFER':
            adjust(self.part, self.warehouse_from, self.condition, -self.quantity)
            adjust(self.part, self.warehouse_to, self.condition, self.quantity)