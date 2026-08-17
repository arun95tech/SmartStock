import uuid
from django.db import models
from master_data.models import Item, Supplier


class ForecastRun(models.Model):
    METHOD_CHOICES = [
        ('MOVING_AVG', 'Moving Average'),
        ('EXP_SMOOTHING', 'Exponential Smoothing'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='forecast_runs')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    forecasted_qty = models.DecimalField(max_digits=10, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.sku} forecast: {self.forecasted_qty} ({self.method})"


class ReorderRecommendation(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('ACTIONED', 'Actioned'),
        ('DISMISSED', 'Dismissed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='reorder_recommendations')
    forecast_run = models.ForeignKey(ForecastRun, on_delete=models.PROTECT, related_name='recommendations', null=True, blank=True)
    current_stock = models.IntegerField()
    reorder_point = models.IntegerField()
    recommended_qty = models.IntegerField()
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reorder {self.item.sku}: {self.recommended_qty} ({self.status})"


class ABCClassificationRun(models.Model):
    CLASS_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='abc_runs')
    abc_class = models.CharField(max_length=1, choices=CLASS_CHOICES)
    annual_value = models.DecimalField(max_digits=12, decimal_places=2)
    run_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.sku}: class {self.abc_class}"


class SupplierKPI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='kpis')
    period = models.DateField()
    otif_score = models.DecimalField(max_digits=5, decimal_places=2)
    avg_lead_time = models.DecimalField(max_digits=5, decimal_places=2)
    defect_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.supplier.name} KPI ({self.period})"


class SupplierRiskScore(models.Model):
    RISK_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='risk_scores')
    risk_rating = models.CharField(max_length=10, choices=RISK_CHOICES)
    contributing_factors = models.CharField(max_length=255)
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.supplier.name}: {self.risk_rating} risk"