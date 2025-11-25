from django.shortcuts import render
from plants.models import Plant
from .models import Location


def location_tree(request, plant_id=None):
    plants = Plant.objects.all()
    locations = Location.objects.filter(plant_id=plant_id) if plant_id else Location.objects.all()
    return render(request, 'locations/location_tree.html', {'plants': plants, 'locations': locations, 'plant_id': plant_id})