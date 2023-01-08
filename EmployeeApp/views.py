from django.shortcuts import render

# The following statement imports a symbol,
# which will be used to allow other domains to access "our API methods".
from django.views.decorators.csrf import csrf_exempt

# The following statent imports a symbol,
# which will be used to parse the incoming data into "data model".
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from EmployeeApp.models import Departments, Employees
from EmployeeApp.serializers import DepartmentSerializer, EmployeeSerializer

# Create your views here.


@csrf_exempt
def departmentApi(request, id=0):
    if request.method == "GET":
        departments = Departments.objects.all()
        d_s = DepartmentSerializer(departments, many=True)
        return JsonResponse(d_s.data, safe=False)
    elif request.method == "POST":
        department_data = JSONParser().parse(request)
        d_s = DepartmentSerializer(data=department_data)

        # If the model [instance] is valid, save it into the database.
        if d_s.is_valid():
            d_s.save()
            return JsonResponse("Added successfully.", safe=False)

        return JsonResponse("Failed to add.", safe=False)
    elif request.method == "PUT":
        department_data = JSONParser().parse(request)
        department = Departments.objects.get(
            DepartmentId=department_data["DepartmentId"]
        )
        d_s = DepartmentSerializer(department, data=department_data)

        # If the model [instance] is valid, save it into the database.
        if d_s.is_valid():
            d_s.save()
            return JsonResponse("Updated successfully.", safe=False)

        return JsonResponse("Failed to update.", safe=False)
    elif request.method == "DELETE":
        department = Departments.objects.get(DepartmentId=id)
        department.delete()
        return JsonResponse("Deleted successfully.", safe=False)
