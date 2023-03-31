import datetime
import hashlib
import pytz

from GrainSense.models import Gateway, Owner, SeedTypes, Storage, Stick, Entry
from django.http import JsonResponse
from django.views.generic import View

from django.contrib.auth.models import AnonymousUser as Anonymous

from GrainSense.serializers import StorageSerializer, SeedTypesSerializer, OwnerSerializer, EntrySerializer, StickSerializer

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def auth_decorator(func):
    def wrapper(request, *args, **kwargs):
        kwargs['error'] = False
        if request.user == Anonymous:
            kwargs['error'] = True
        func(request, *args, **kwargs)
    return wrapper


class OwnerView(View):
    http_method_names = ['post', 'get']

    @staticmethod
    def post(request):
        args = request.POST
        owner = Owner.objects.filter(email=args['email'])
        if len(owner) > 0:
            return JsonResponse({'message': 'owner with such email already exists!'}, status=403)
        password_with_salt = args['password'] + args['email']
        owner = Owner(username=args['username'], password=hashlib.md5(password_with_salt.encode()).hexdigest(), first_name=args['first_name'], last_name=args['last_name'], email=args['email'])
        owner.save()
        return JsonResponse({'message': f"Owner {args['last_name']} created successfully"})

    @staticmethod
    def get(request):
        id = -1
        try:
            id = request.GET['owner_id']
        except:
            object = Owner.objects.all()
            return JsonResponse(OwnerSerializer(object, many=True).data, safe=False)
        try:
            return JsonResponse(OwnerSerializer(Owner.objects.get(id=id)).data, safe=False)
        except:
            return JsonResponse({'message': f"Owner with id={id} doesn't exist"}, status=404)


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
    def get(request):
        objects = SeedTypes.objects.all()
        try:
            id = request.GET['seed_type_id']
            objects = objects.filter(id=id)
        finally:
            serial = SeedTypesSerializer(objects, many=True)
            return JsonResponse(serial.data, safe=False)


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
    def get(request):
        params = request.GET
        try:
            owner_id = params['owner_id']
            objects = Storage.objects.all()
            objects = objects.filter(owner_id=owner_id)
            serial = StorageSerializer(objects, many=True)
            return JsonResponse(serial.data, safe=False)
        except:
            return JsonResponse({"message": "No owner specified"}, status = 404)


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


class StickView(View):
    http_method_names = ['post', 'get', 'delete']

    @staticmethod
    def post(request):
        args = request.POST
        stick = Stick(gateway_id=args['gateway_id'], storage_id=args['storage_id'])
        try:
            stick.save()
        except:
            return JsonResponse({'message': "No such storage or gateway exists"}, status=404)
        return JsonResponse({'message': "Stick created successfully"}, status=201)

    @staticmethod
    def get(request):
        sticks = Stick.objects.all()
        try:
            id = request.GET['gateway_id']
            sticks = sticks.filter(gateway_id=id)
        finally:
            return JsonResponse(StickSerializer(sticks, many=True).data, safe=False)


class EntryView(View):
    http_method_names = ['post', 'get']

    @staticmethod
    def get(request):
        params = request.GET
        sticks = Stick.objects.all()
        try:
            storage_id = params['storage_id']
            sticks = Stick.objects.filter(storage_id=storage_id)
        except:
            return JsonResponse({'message': "No storage specified"}, status=404)
        response = []
        start = None
        try:
            start = params['start']
        finally:
            finish = None
            try:
                finish = params['finish']
            finally:
                for stick in sticks:
                    objects = Entry.objects.filter(stick_id=stick.id)
                    for entry in objects:
                        if start is None or pytz.utc.localize(datetime.datetime.strptime(start, DATETIME_FORMAT))\
                                <= entry.time <=\
                                pytz.utc.localize(datetime.datetime.strptime(finish, DATETIME_FORMAT)):
                            response.append(entry)
                return JsonResponse(EntrySerializer(response, many=True).data, safe=False)

    @staticmethod
    def post(request):
        args = request.POST
        try:
            entry = Entry(send_id=args['send_id'], temp=args['temp'], height_level=args['height_level'], stick_id=args['stick_id'], time=args['time'])
            entry.save()
            return JsonResponse({'message': 'Entry was created successfully'}, status=201)
        except:
            return JsonResponse({'message': f'Stick with id={args["stick_id"]} doesnt exist'}, status=404)
