from django.http import JsonResponse

from .sql_tools.kpi import kpi_dashboard


def kpi_view(request):

    total, delivered, cancelled, returned, avg_cycle = kpi_dashboard()

    return JsonResponse({

        "total_orders": total,

        "delivered_orders": delivered,

        "cancelled_orders": cancelled,

        "returned_orders": returned,

        "average_cycle_time": str(avg_cycle)

    })