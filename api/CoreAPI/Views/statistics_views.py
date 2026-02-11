from django.shortcuts import render 
from django.utils.safestring import mark_safe
import json

from ..Models.driver_model import DriverModel
from ..Models.vehicule_model import VehiculeModel
from ..Models.warehouse_model import WarehouseModel
from ..Models.tag_model import TagModel
from ..Models.article_model import ArticleModel
from ..Models.mission_model import MissionModel

def home(request):
    # fake example data
    total_drivers = DriverModel.objects.all().count()
    total_vehicules = VehiculeModel.objects.all().count()
    total_warehouses = WarehouseModel.objects.all().count()
    total_articles = ArticleModel.objects.all().count()
    active_missions = ArticleModel.objects.all().count()
    active_tags = TagModel.objects.all().count()

    # line chart data
    visits_dates = ["2026-01-20","2026-01-21","2026-01-22","2026-01-23","2026-01-24"]
    visits_counts = [150, 180, 170, 220, 260]

    # bar chart data
    sales_categories = ["Books","Electronics","Clothes","Food"]
    sales_values = [340, 2000, 1800, 1730]

    context = {
        "total_drivers": total_drivers,
        "total_vehicules": total_vehicules,
        "total_warehouses": total_warehouses,
        "total_articles": total_articles,
        "active_missions": active_missions,
        "active_tags": active_tags,
        "visits_dates": mark_safe(json.dumps(visits_dates)),
        "visits_counts": mark_safe(json.dumps(visits_counts)),
        "sales_categories": mark_safe(json.dumps(sales_categories)),
        "sales_values": mark_safe(json.dumps(sales_values)),
    }
    return render(request, 'CoreAPI/home.html', context)