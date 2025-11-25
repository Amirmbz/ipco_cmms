from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Asset, AssetCategory, AssetAttachment, AssetSparePartLink
from plants.models import Plant
from locations.models import Location


def asset_list(request):
    assets = Asset.objects.select_related('plant', 'location', 'category')
    plants = Plant.objects.all()
    categories = AssetCategory.objects.all()
    locations = Location.objects.all()

    code = request.GET.get('code')
    name = request.GET.get('name')
    plant_id = request.GET.get('plant')
    location_id = request.GET.get('location')
    category_id = request.GET.get('category')

    if code:
        assets = assets.filter(code__icontains=code)
    if name:
        assets = assets.filter(name__icontains=name)
    if plant_id:
        assets = assets.filter(plant_id=plant_id)
    if location_id:
        assets = assets.filter(location_id=location_id)
    if category_id:
        assets = assets.filter(category_id=category_id)

    return render(request, 'assets/asset_list.html', {
        'assets': assets,
        'plants': plants,
        'categories': categories,
        'locations': locations,
    })


def asset_detail(request, pk):
    asset = get_object_or_404(Asset.objects.select_related('plant', 'location', 'category'), pk=pk)
    attachments = asset.attachments.all()
    spare_parts = asset.spare_parts.select_related('part').all()
    return render(request, 'assets/asset_detail.html', {
        'asset': asset,
        'attachments': attachments,
        'spare_parts': spare_parts,
    })