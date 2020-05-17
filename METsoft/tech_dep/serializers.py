from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Order, OrderStatus


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name"]


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ["id", "status"]


class OrderSerializers(serializers.ModelSerializer):
    status = OrderStatusSerializer()
    tech_memb = UserSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "numer_met",
            "company",
            "cast_name",
            "pict_number",
            "cast_pcs",
            "cust_material",
            "termin_klienta",
            "model",
            "rawcast",
            "painting",
            "mechrough",
            "mechfine",
            "marketing",
            "ord_in",
            "ord_out",
            "uwagi",
            "status",
            "tech_memb",
            "get_working_time",
        ]
