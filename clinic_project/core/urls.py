from django.urls import path
from . import views



urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("followups/create/", views.create_followup, name="create_followup"),
    path("followups/<int:pk>/edit/", views.edit_followup, name="edit_followup"),
    
    path("followups/<int:pk>/done/",views.mark_followup_done,name="mark_followup_done",),
    

path("p/<str:token>/", views.public_followup, name="public_followup"),
        path(
    "followups/<int:pk>/delete/",
    views.delete_followup,
    name="delete_followup",
),
    path(
    "followups/export/csv/",
    views.export_followups_csv,
    name="export_followups_csv",
),



]
