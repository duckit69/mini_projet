from django.urls import path

from .Views.article_views import CreateArticle, UpdateArticle, RetrieveArticle, DestroyArticle, ListArticle
from .Views.vehicule_views import CreateVehicule, UpdateVehicule, RetrieveVehicule, DestroyVehicule, ListVehicule
from .Views.driver_views import CreateDriver, UpdateDriver, RetrieveDriver, DestroyDriver, ListDriver
from .Views.tag_views import CreateTag, UpdateTag, RetrieveTag, DestroyTag, ListTag
from .Views.warehouse_views import CreateWarehouse, UpdateWarehouse, RetrieveWarehouse, DestroyWarehouse, ListWarehouse
from .Views.mission_views import CreateMission, UpdateMission, RetrieveMission, DestroyMission, ListMission

urlpatterns = [
    # ARTICLE endpoints
    path('article/create', CreateArticle.as_view()),
    path('article/update/<int:pk>', UpdateArticle.as_view()),
    path('article/retreive/<int:pk>', RetrieveArticle.as_view()),
    path('article/delete/<int:pk>', DestroyArticle.as_view()),
    path('article/list', ListArticle.as_view()),
    
    # VEHICULE endpoints
    path('vehicule/create', CreateVehicule.as_view()),
    path('vehicule/update/<int:pk>', UpdateVehicule.as_view()),
    path('vehicule/retreive/<int:pk>', RetrieveVehicule.as_view()),
    path('vehicule/delete/<int:pk>', DestroyVehicule.as_view()),
    path('vehicule/list', ListVehicule.as_view()),
    
    # DRIVER endpoints
    path('driver/create', CreateDriver.as_view()),
    path('driver/update/<int:pk>', UpdateDriver.as_view()),
    path('driver/retreive/<int:pk>', RetrieveDriver.as_view()),
    path('driver/delete/<int:pk>', DestroyDriver.as_view()),
    path('driver/list', ListDriver.as_view()),
    
    # TAG endpoints
    path('tag/create', CreateTag.as_view()),
    path('tag/update/<int:pk>', UpdateTag.as_view()),
    path('tag/retreive/<int:pk>', RetrieveTag.as_view()),
    path('tag/delete/<int:pk>', DestroyTag.as_view()),
    path('tag/list', ListTag.as_view()),
    
    # WAREHOUSE endpoints
    path('warehouse/create', CreateWarehouse.as_view()),
    path('warehouse/update/<int:pk>', UpdateWarehouse.as_view()),
    path('warehouse/retreive/<int:pk>', RetrieveWarehouse.as_view()),
    path('warehouse/delete/<int:pk>', DestroyWarehouse.as_view()),
    path('warehouse/list', ListWarehouse.as_view()),
    
    # MISSION endpoints
    path('mission/create', CreateMission.as_view()),
    path('mission/update/<int:pk>', UpdateMission.as_view()),
    path('mission/retreive/<int:pk>', RetrieveMission.as_view()),
    path('mission/delete/<int:pk>', DestroyMission.as_view()),
    path('mission/list', ListMission.as_view()),
]