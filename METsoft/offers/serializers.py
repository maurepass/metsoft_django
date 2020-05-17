from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Detail, MachiningType, Material, MaterialGroup, Offer, OfferStatus


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
        )


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferStatus
        fields = ("id", "offer_status")


class OfferSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    user_mark = UserSerializer()
    user_tech = UserSerializer()

    class Meta:
        model = Offer
        fields = (
            "id",
            "offer_no",
            "client",
            "user_mark",
            "user_tech",
            "date_tech_in",
            "date_tech_out",
            "positions_amount",
            "status",
            "get_days_amount",
        )


class MaterialGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialGroup
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    mat_group = MaterialGroupSerializer()

    class Meta:
        model = Material
        fields = ["id", "material", "mat_group"]


class MachiningSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachiningType
        fields = ["id", "machining"]


class DetailSerializer(serializers.ModelSerializer):
    mat = MaterialSerializer()
    machining = MachiningSerializer()
    offer = OfferSerializer()

    class Meta:
        model = Detail
        fields = [
            "id",
            "offer",
            "cast_name",
            "drawing_no",
            "mat",
            "cast_weight",
            "pieces_amount",
            "detail_yield",
            "difficulty",
            "pattern",
            "heat_treat",
            "machining",
            "tolerances",
            "tapers",
            "atest",
            "required",
            "quality_class",
        ]
