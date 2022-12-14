import json

from django.db import models


class Entry(models.Model):
    id = models.IntegerField(primary_key=True)
    send_id = models.IntegerField()
    height_level = models.IntegerField()
    stick_id = models.IntegerField()
    temp = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        db_table = "entry"

    def __repr__(self):
        return '{' + f"send_id: {self.send_id}, height_level: {self.height_level}, stick_id: {self.stick_id}, temperature: {self.temp}, " \
                     f"time: {self.time}" + '}'


class Gateway(models.Model):
    id = models.IntegerField(primary_key=True)
    owner_id = models.IntegerField()

    class Meta:
        db_table = "gateway"

    def __repr__(self):
        return '{' + f"id: {self.id}, owner_id: {self.owner_id}" + '}'


class Stick(models.Model):
    id = models.IntegerField(primary_key=True)
    gateway_id = models.IntegerField()
    storage_id = models.IntegerField()

    class Meta:
        db_table = "stick"

    def __repr__(self):
        return '{' + f"id: {self.id}, gateway_id: {self.gateway_id}, storage_id: {self.storage_id}" + '}'


class Storage(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=100)
    owner_id = models.IntegerField()
    seed_types_id = models.IntegerField()

    class Meta:
        db_table = "storage"

    def __repr__(self):
        return '{' + f"id: {self.id}, address: {self.address}, owner_id: {self.owner_id}, seed_types_id: {self.seed_types_id}" + '}'


class SeedTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    lower_bound = models.IntegerField()
    upper_bound = models.IntegerField()
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "seed_types"

    def __repr__(self):
        return '{' + f"id: {self.id}, lower_bound: {self.lower_bound}, upper_bound: {self.upper_bound}, name: {self.name}" + '}'


class Owner(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)

    class Meta:
        db_table = "owner"

    def __repr__(self):
        return '{' + f"id: {self.id}, username: {self.username}, first_name: {self.first_name}, last_name: {self.last_name}, email: {self.email}" + '}'

