from django.db.models import Sum
from django.shortcuts import render, get_object_or_404

from .models import Warehouse, Part, PartStock


def warehouse_list(request):
    warehouses = Warehouse.objects.select_related('plant').all()
    return render(request, 'inventory/warehouse_list.html', {'warehouses': warehouses})


def warehouse_detail(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    stock = PartStock.objects.filter(warehouse=warehouse).select_related('part')
    return render(request, 'inventory/warehouse_detail.html', {'warehouse': warehouse, 'stock': stock})


def part_list(request):
    parts = Part.objects.all()
    return render(request, 'inventory/part_list.html', {'parts': parts})


def part_detail(request, pk):
    part = get_object_or_404(Part, pk=pk)
    stock = PartStock.objects.filter(part=part).select_related('warehouse')
    totals = stock.values('condition').annotate(total=Sum('quantity'))
    return render(request, 'inventory/part_detail.html', {'part': part, 'stock': stock, 'totals': totals})