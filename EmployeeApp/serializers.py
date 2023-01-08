"""
Serializers basically help:

(a) to convert ... "complex types" [such as] model instances
    into native Python datatypes
    that can then be easily rendered into JSON or XML or other content types;

(b) in de-serialization,
    which is nothing but converting the passed data back into "complex types".

This module implements special serializers called _model serializers_.
"""

from rest_framework import serializers
from EmployeeApp.models import Departments, Employees


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = (
            "DepartmentId",
            "DepartmentName",
        )


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = (
            "EmployeeId",
            "EmployeeName",
            "Department",
            "DateOfJoining",
            "PhotoFileName",
        )
