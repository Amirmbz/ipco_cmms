import csv
from datetime import datetime, timedelta

from django.db.models import Count, Sum, Avg
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import routers
from django.urls import path

from work_orders.models import WorkOrder
from inventory.models import PartTransaction


router = routers.DefaultRouter()


def _parse_date(value):
    try:
        return datetime.fromisoformat(value).date()
    except Exception:
        return None


def _maybe_export_csv(request, headers, rows, filename):
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        writer = csv.writer(response)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        return response
    return None


class WorkorderStatusSummaryView(APIView):
    def get(self, request):
        qs = WorkOrder.objects.all()
        plant = request.GET.get('plant')
        department = request.GET.get('department')
        status_param = request.GET.get('status')
        start = _parse_date(request.GET.get('start'))
        end = _parse_date(request.GET.get('end'))
        if plant:
            qs = qs.filter(plant_id=plant)
        if department:
            qs = qs.filter(department_id=department)
        if status_param:
            qs = qs.filter(status=status_param)
        if start:
            qs = qs.filter(created_at__date__gte=start)
        if end:
            qs = qs.filter(created_at__date__lte=end)
        data = list(qs.values('status').annotate(count=Count('id')))
        csv_resp = _maybe_export_csv(request, ['status', 'count'], [(d['status'], d['count']) for d in data], 'workorder_status_summary')
        if csv_resp:
            return csv_resp
        return Response(data)


class WorkorderByAssetView(APIView):
    def get(self, request):
        asset = request.GET.get('asset')
        start = _parse_date(request.GET.get('start'))
        end = _parse_date(request.GET.get('end'))
        qs = WorkOrder.objects.filter(asset_id=asset) if asset else WorkOrder.objects.none()
        if start:
            qs = qs.filter(created_at__date__gte=start)
        if end:
            qs = qs.filter(created_at__date__lte=end)
        data = list(qs.values('code', 'status', 'downtime_minutes', 'type'))
        csv_resp = _maybe_export_csv(request, ['code', 'status', 'downtime', 'type'], [(d['code'], d['status'], d['downtime_minutes'], d['type']) for d in data], 'workorder_by_asset')
        if csv_resp:
            return csv_resp
        return Response(data)


class WorkorderByTechnicianView(APIView):
    def get(self, request):
        technician = request.GET.get('technician')
        start = _parse_date(request.GET.get('start'))
        end = _parse_date(request.GET.get('end'))
        qs = WorkOrder.objects.filter(assigned_to__id=technician) if technician else WorkOrder.objects.none()
        if start:
            qs = qs.filter(created_at__date__gte=start)
        if end:
            qs = qs.filter(created_at__date__lte=end)
        done = qs.filter(status='COMPLETED')
        data = {
            'total_done': done.count(),
            'average_downtime': done.aggregate(avg=Avg('downtime_minutes'))['avg'],
            'open': qs.exclude(status='COMPLETED').count(),
        }
        csv_resp = _maybe_export_csv(request, ['metric', 'value'], data.items(), 'workorder_by_technician')
        if csv_resp:
            return csv_resp
        return Response(data)


class AssetHistoryView(APIView):
    def get(self, request):
        asset = request.GET.get('asset')
        qs = WorkOrder.objects.filter(asset_id=asset) if asset else WorkOrder.objects.none()
        data = list(qs.values('code', 'status', 'downtime_minutes', 'type', 'created_at', 'completed_at'))
        totals = {
            'total_downtime': qs.aggregate(total=Sum('downtime_minutes'))['total'],
            'breakdowns': qs.filter(type='BREAKDOWN').count(),
        }
        response_data = {'work_orders': data, 'totals': totals}
        csv_resp = _maybe_export_csv(request, ['code', 'status', 'downtime', 'type'], [(d['code'], d['status'], d['downtime_minutes'], d['type']) for d in data], 'asset_history')
        if csv_resp:
            return csv_resp
        return Response(response_data)


class PMComplianceView(APIView):
    def get(self, request):
        plant = request.GET.get('plant')
        start = _parse_date(request.GET.get('start'))
        end = _parse_date(request.GET.get('end'))
        qs = WorkOrder.objects.filter(type='PREVENTIVE')
        if plant:
            qs = qs.filter(plant_id=plant)
        if start:
            qs = qs.filter(created_at__date__gte=start)
        if end:
            qs = qs.filter(created_at__date__lte=end)
        done = qs.filter(status='COMPLETED').count()
        planned = qs.count()
        overdue = qs.filter(due_date__lt=datetime.now().date(), status__in=['SUBMITTED', 'UNDER_REVIEW', 'ASSIGNED', 'IN_PROGRESS']).count()
        data = {'planned': planned, 'done': done, 'overdue': overdue}
        csv_resp = _maybe_export_csv(request, ['planned', 'done', 'overdue'], [(planned, done, overdue)], 'pm_compliance')
        if csv_resp:
            return csv_resp
        return Response(data)


class MTBFMTTRView(APIView):
    def get(self, request):
        asset = request.GET.get('asset')
        start = _parse_date(request.GET.get('start'))
        end = _parse_date(request.GET.get('end'))
        qs = WorkOrder.objects.filter(asset_id=asset) if asset else WorkOrder.objects.none()
        if start:
            qs = qs.filter(created_at__date__gte=start)
        if end:
            qs = qs.filter(created_at__date__lte=end)
        failures = qs.filter(type='BREAKDOWN')
        failure_count = failures.count()
        downtime = failures.aggregate(total=Sum('downtime_minutes'))['total'] or 0
        total_time = failure_count * 24 * 60  # placeholder operating time
        mtbf = (total_time / failure_count) if failure_count else None
        mttr = (downtime / failure_count) if failure_count else None
        data = {'mtbf': mtbf, 'mttr': mttr, 'failures': failure_count}
        csv_resp = _maybe_export_csv(request, ['mtbf', 'mttr', 'failures'], [(mtbf, mttr, failure_count)], 'mtbf_mttr')
        if csv_resp:
            return csv_resp
        return Response(data)


class InventoryConsumptionView(APIView):
    def get(self, request):
        plant = request.GET.get('plant')
        start = _parse_date(request.GET.get('start'))
        end = _parse_date(request.GET.get('end'))
        qs = PartTransaction.objects.filter(transaction_type='OUT')
        if start:
            qs = qs.filter(created_at__date__gte=start)
        if end:
            qs = qs.filter(created_at__date__lte=end)
        if plant:
            qs = qs.filter(warehouse_from__plant_id=plant)
        data = list(qs.values('part__code', 'part__name').annotate(total=Sum('quantity')))
        csv_resp = _maybe_export_csv(request, ['part', 'name', 'total'], [(d['part__code'], d['part__name'], d['total']) for d in data], 'inventory_consumption')
        if csv_resp:
            return csv_resp
        return Response(data)


urlpatterns = [
    path('workorder-status-summary/', WorkorderStatusSummaryView.as_view()),
    path('workorder-by-asset/', WorkorderByAssetView.as_view()),
    path('workorder-by-technician/', WorkorderByTechnicianView.as_view()),
    path('asset-history/', AssetHistoryView.as_view()),
    path('pm-compliance/', PMComplianceView.as_view()),
    path('mtbf-mttr/', MTBFMTTRView.as_view()),
    path('inventory-consumption/', InventoryConsumptionView.as_view()),
]
