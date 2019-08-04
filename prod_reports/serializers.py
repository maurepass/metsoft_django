from rest_framework import serializers

from .models import (AccordanceDict, Cast, Material, Operation, OperationDict,
                     Pocastord, Porder, User)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class PorderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Porder
        fields = ['met_no']


class PocastordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pocastord
        fields = ['id', 'cast_pcs']


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ['materialname', 'calcgroup']


class CastSerializer(serializers.ModelSerializer):
    porder = PorderSerializer()
    cast_material = MaterialSerializer()
    tech = UserSerializer()

    class Meta:
        model = Cast
        fields = ['id', 'porder', 'cast_name', 'tech', 'picture_number', 'customer', 'cast_material', 'cast_weight',
                  'created_at', 'material_need', 'tech_maker']


class AccordanceDictSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccordanceDict
        fields = ['accname']


class OperationDictSerializer(serializers.ModelSerializer):

    class Meta:
        model = OperationDict
        fields = ['operationname']


class OperationSerializer(serializers.ModelSerializer):
    cast = CastSerializer()
    opdict = OperationDictSerializer()
    accordance = AccordanceDictSerializer()

    class Meta:
        model = Operation
        fields = ['cast', 'opdict', 'parameter_value1', 'parameter_value2', 'completion_date1', 'confirmed_by1',
                  'notes', 'accordance']
