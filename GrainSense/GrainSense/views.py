import datetime

from passlib.hash import bcrypt
from getpass import getpass

import pytz

from GrainSense.models import Gateway, Owner, SeedTypes, Storage, Stick, Entry
from django.http import JsonResponse
from django.views.generic import View

from GrainSense.serializers import StorageSerializer, SeedTypesSerializer, OwnerSerializer, EntrySerializer, StickSerializer

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

hasher = bcrypt.using(rounds=13)


class OwnerView(View):
    http_method_names = ['post', 'get']

    @staticmethod
    def post(request):
        args = request.POST
        owner = Owner.objects.filter(email=args['email'])
        if len(owner) > 0:
            return JsonResponse({'message': 'owner with such email already exists!'}, status=403)
        owner = Owner(username=args['username'], password=hasher.hash(args['password']), first_name=args['first_name'], last_name=args['last_name'], email=args['email'])
        owner.save()
        return JsonResponse({'message': f"Owner {args['last_name']} created successfully"})

    @staticmethod
    def get(request, id=None):
        objects = Owner.objects.all()
        if id is not None:
            objects = objects.filter(id=id)
        return JsonResponse(OwnerSerializer(objects, many=True).data, safe=False)


class SeedTypesView(View):
    http_method_names = ['post', 'get', 'delete']

    @staticmethod
    def post(request, id=None):
        args = request.POST
        if id:
            try:
                seed_type = SeedTypes.objects.get(id=id)
                if 'lower_bound' in args.keys():
                    seed_type.lower_bound = args['lower_bound']
                if 'upper_bound' in args.keys():
                    seed_type.upper_bound = args['upper_bound']
                if 'name' in args.keys():
                    seed_type.name = args['name']
                seed_type.save()
                return JsonResponse(SeedTypesSerializer(seed_type).data)
            except:
                return JsonResponse({'message': f"Seed type with id={id} doesn't exist"}, status=404)
        else:
            seed_type = SeedTypes(lower_bound=args['lower_bound'], upper_bound=args['upper_bound'], name=args['name'])
            seed_type.save()
            return JsonResponse({'message': f"Seed type {args['name']} created successfully"})

    @staticmethod
    def delete(request, id):
        try:
            SeedTypes.objects.get(id=id).delete()
            return JsonResponse({'message': f"Seed type with id={id} was deleted successfully"}, status=200)
        except:
            return JsonResponse({'message': f"Seed type with id={id} doesn't exist"}, status=404)

    @staticmethod
    def get(request, id=None):
        objects = SeedTypes.objects.all()
        if id:
            objects = objects.filter(id=id)
        serial = SeedTypesSerializer(objects, many=True)
        return JsonResponse(serial.data)


class StorageView(View):
    http_method_names = ['post', 'get', 'delete']

    @staticmethod
    def post(request):
        args = request.POST
        storage = Storage(address=args['address'], owner_id=args['owner_id'], seed_types_id=args['seed_types_id'])
        try:
            storage.save()
        except:
            return JsonResponse({'message': "No such owner or seed type exists"}, status=404)
        return JsonResponse({'message': "Storage created successfully"}, status=201)

    @staticmethod
    def get(request, owner_id):
        objects = Storage.objects.all()
        objects = objects.filter(owner_id=owner_id)
        serial = StorageSerializer(objects, many=True)
        return JsonResponse(serial.data, safe=False)


class GatewayView(View):
    http_method_names = ['post', 'get', 'delete']

    @staticmethod
    def post(request):
        args = request.POST
        gateway = Gateway(owner_id=args['owner_id'])
        try:
            gateway.save()
        except:
            return JsonResponse({'message': "No such owner exists"}, status=404)
        return JsonResponse({'message': "Gateway created successfully"}, status=201)

