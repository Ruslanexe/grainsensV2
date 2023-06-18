from rest_framework import serializers

from GrainSense.models import Storage, Entry, Gateway, Stick, SeedTypes, Owner
from GrainSense.my_token import AccessToken


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('id', 'owner_id', 'address', 'seed_types_id')


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('send_id', 'height_level', 'stick_id', 'temp', 'time')


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('storage_id', 'id')


class StickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stick
        fields = ('id', 'storage_id', 'gateway_id')


class SeedTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedTypes
        fields = ('id', 'lower_bound', 'upper_bound', 'name')


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ('user', 'value', 'expires')
