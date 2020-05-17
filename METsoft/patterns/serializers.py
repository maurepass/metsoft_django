from rest_framework import serializers

from .models import Pattern, PatternHistory, PatternStatus


class PatternStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = PatternStatus
        fields = ["status"]


class PatternSerializers(serializers.ModelSerializer):
    status = PatternStatusSerializers()

    class Meta:
        model = Pattern
        fields = (
            "id",
            "customer",
            "drawing_number",
            "pattern_name",
            "last_order",
            "orders_amount",
            "area",
            "layer_number",
            "layer_place",
            "material",
            "cart_number",
            "pattern_index",
            "verification",
            "remarks",
            "verification_date",
            "surname",
            "status",
            "move_in",
            "get_not_using_time",
        )


class PatternHistorySerializers(serializers.ModelSerializer):
    pattern = PatternSerializers()
    status = PatternStatusSerializers()

    class Meta:
        model = PatternHistory
        fields = ("pattern", "status", "date")
