from django.shortcuts import render


def workorder_status_summary(request):
    return render(request, 'reports/workorder_status_summary.html')


def workorder_by_asset(request):
    return render(request, 'reports/workorder_by_asset.html')


def workorder_by_technician(request):
    return render(request, 'reports/workorder_by_technician.html')


def asset_history(request):
    return render(request, 'reports/asset_history.html')


def pm_compliance(request):
    return render(request, 'reports/pm_compliance.html')


def mtbf_mttr(request):
    return render(request, 'reports/mtbf_mttr.html')


def inventory_consumption(request):
    return render(request, 'reports/inventory_consumption.html')