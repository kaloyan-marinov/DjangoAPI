from django.conf.urls import url
from EmployeeApp import views


urlpatterns = [
    url(r"^departments$", views.departmentApi),
    url(r"^departments/([0-9]+)$", views.departmentApi),
]
