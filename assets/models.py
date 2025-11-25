from django.db import models


class AssetCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('IDLE', 'Idle'),
        ('REPAIR', 'Repair'),
        ('RETIRED', 'Retired'),
    ]
    PM_SCHEDULE_CHOICES = [
        ('NONE', 'None'),
        ('DAY_BASED', 'Day Based'),
        ('RUNTIME_BASED', 'Runtime Based'),
    ]

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    plant = models.ForeignKey('plants.Plant', on_delete=models.CASCADE)
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    model = models.CharField(max_length=255, blank=True)
    manufacturer = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, blank=True)
    specs = models.TextField(blank=True)
    manufacture_year = models.IntegerField(null=True, blank=True)

    vendor = models.CharField(max_length=255, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    pm_schedule_type = models.CharField(max_length=20, choices=PM_SCHEDULE_CHOICES, default='NONE')
    pm_interval_days = models.IntegerField(null=True, blank=True)
    pm_interval_hours = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class AssetAttachment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='asset_attachments/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or self.file.name


class AssetSparePartLink(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='spare_parts')
    part = models.ForeignKey('inventory.Part', on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.asset} - {self.part}"