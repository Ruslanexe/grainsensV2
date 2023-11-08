import datetime
import hashlib
import pytz

from GrainSense.models import Gateway, Owner, SeedTypes, Storage, Stick, Entry
from django.http import JsonResponse
from django.views.generic import View
from GrainSense.my_token import *

from GrainSense.serializers import StorageSerializer, SeedTypesSerializer, OwnerSerializer, EntrySerializer, StickSerializer, GatewaySerializer

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def str_to_datetime(date_string):
    a = datetime.datetime.strptime(date_string, DATETIME_FORMAT)
    return a


def hashed_password(email, password):
    password_with_salt = password + email
    return hashlib.md5(password_with_salt.encode()).hexdigest()


class LoginView(View):
    http_method_names = ['post']

    @staticmethod
    def post(request):
        remove_old_tokens()
        args = request.POST
        owner = Owner.objects.filter(email=args['email'], password=hashed_password(args['email'], args['password']))
        if len(owner) == 0:
            return JsonResponse({'message': 'wrong email/password'}, status=403)
        token = AccessToken(owner[0].id)
        token.validate()
        print(active_tokens)
        return JsonResponse(str(token), safe=False, status=200)


class OwnerView(View):
    http_method_names = ['post', 'get']

    @staticmethod
    def post(request):
        remove_old_tokens()
        args = request.POST
        owner = Owner.objects.filter(email=args['email'])
        if len(owner) > 0:
            return JsonResponse({'message': 'owner with such email already exists!'}, status=403)

        owner = Owner(username=args['username'], password=hashed_password(args['email'], args['password']), first_name=args['first_name'], last_name=args['last_name'], email=args['email'])
        owner.save()
        return JsonResponse({'message': f"Owner {args['last_name']} created successfully"})

    @staticmethod
    def get(request):
        remove_old_tokens()
        try:
            id = request.GET['owner_id']
        except:
            return JsonResponse({'message': 'No owner id specified'}, status=404)
        try:
            token_value = request.META['HTTP_TOKEN']
            user = int(request.META['HTTP_USER'])
            expires = str_to_datetime(request.META['HTTP_EXPIRES'])
            token = AccessToken(user, token_value, expires)
            if not (token in active_tokens):
                return JsonResponse({'message': 'Token expired'}, status=304)
            if user != int(id):
                return JsonResponse({'message': 'Permission denied'}, status=304)
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
        remove_old_tokens()
        args = request.POST
        storage = Storage(address=args['address'], owner_id=args['owner_id'], seed_types_id=args['seed_types_id'])
        try:
            token_value = request.META['HTTP_TOKEN']
            user = int(request.META['HTTP_USER'])
            expires = str_to_datetime(request.META['HTTP_EXPIRES'])
            token = AccessToken(user, token_value, expires)
            if not (token in active_tokens):
                return JsonResponse({'message': 'Token expired'}, status=304)
            if user != int(args['owner_id']):
                return JsonResponse({'message': 'Permission denied'}, status=304)
            storage.save()
        except:
            return JsonResponse({'message': "No such owner or seed type exists"}, status=404)
        return JsonResponse({'message': "Storage created successfully"}, status=201)

    @staticmethod
    def get(request):
        remove_old_tokens()
        params = request.GET
        try:
            owner_id = params['owner_id']
            token_value = request.META['HTTP_TOKEN']
            user = int(request.META['HTTP_USER'])
            expires = str_to_datetime(request.META['HTTP_EXPIRES'])
            token = AccessToken(user, token_value, expires)
            if not (token in active_tokens):
                return JsonResponse({'message': 'Token expired'}, status=304)
            if user != int(owner_id):
                return JsonResponse({'message': 'Permission denied'}, status=304)
            objects = Storage.objects.all()
            objects = objects.filter(owner_id=owner_id)
            serial = StorageSerializer(objects, many=True)
            return JsonResponse(serial.data, safe=False)
        except:
            return JsonResponse({"message": "No owner specified"}, status=404)


class GatewayView(View):
    http_method_names = ['post', 'get', 'delete']

    @staticmethod
    def post(request):
        remove_old_tokens()
        args = request.POST
        gateway = Gateway(owner_id=args['owner_id'])
        try:
            token_value = request.META['HTTP_TOKEN']
            user = int(request.META['HTTP_USER'])
            expires = str_to_datetime(request.META['HTTP_EXPIRES'])
            token = AccessToken(user, token_value, expires)
            if not (token in active_tokens):
                return JsonResponse({'message': 'Token expired'}, status=304)
            if user != int(args['owner_id']):
                return JsonResponse({'message': 'Permission denied'}, status=304)
            gateway.save()
        except:
            return JsonResponse({'message': "No such owner exists"}, status=404)
        return JsonResponse({'message': "Gateway created successfully"}, status=201)

    @staticmethod
    def get(request):
        remove_old_tokens()
        args = request.GET
        try:
            gateway_id = args['gateway_id']
            gateway = Gateway.objects.get(id=gateway_id)
            print(gateway.owner_id)
            token_value = request.META['HTTP_TOKEN']
            user = int(request.META['HTTP_USER'])
            expires = str_to_datetime(request.META['HTTP_EXPIRES'])
            token = AccessToken(user, token_value, expires)
            if not (token in active_tokens):
                print('token error')
                return JsonResponse({'message': 'Token expired'}, status=304)
            if user != int(gateway.owner_id):
                print('invalid owner of gateway')
                return JsonResponse({'message': 'Permission denied'}, status=304)
            serial = GatewaySerializer(gateway)
            data = serial.data
            print("Aboba")
            return JsonResponse(data, safe=False)
        except:
            return JsonResponse({'message': "Invalid gateway id"}, status=404)


class StickView(View):
    http_method_names = ['post', 'get', 'delete']

    @staticmethod
    def post(request):
        remove_old_tokens()
        args = request.POST
        stick = Stick(gateway_id=args['gateway_id'], storage_id=args['storage_id'])
        try:
            token_value = request.META['HTTP_TOKEN']
            user = int(request.META['HTTP_USER'])
            expires = str_to_datetime(request.META['HTTP_EXPIRES'])
            token = AccessToken(user, token_value, expires)
            if not (token in active_tokens):
                print('token error')
                return JsonResponse({'message': 'Token expired'}, status=304)
            storage = Storage.objects.get(id=args['storage_id'])
            if user != int(storage.owner_id):
                print('invalid owner of storage')
                return JsonResponse({'message': 'Permission denied'}, status=304)
            gateway = Gateway.objects.get(id=args['gateway_id'])
            if user != int(gateway.owner_id):
                print('invalid owner of gateway')
                return JsonResponse({'message': 'Permission denied'}, status=304)
            stick.save()
        except:
            return JsonResponse({'message': "No such storage or gateway exists"}, status=404)
        return JsonResponse({'message': "Stick created successfully"}, status=201)

    @staticmethod
    def get(request):
        remove_old_tokens()
        sticks = Stick.objects.all()
        try:
            id = request.GET['gateway_id']
            token_value = request.META['HTTP_TOKEN']
            user = int(request.META['HTTP_USER'])
            expires = str_to_datetime(request.META['HTTP_EXPIRES'])
            token = AccessToken(user, token_value, expires)
            if not (token in active_tokens):
                print('token error')
                return JsonResponse({'message': 'Token expired'}, status=304)
            gateway = Gateway.objects.get(id=id)
            if user != int(gateway.owner_id):
                print('invalid owner of gateway')
                return JsonResponse({'message': 'Permission denied'}, status=304)
            sticks = sticks.filter(gateway_id=id)
            return JsonResponse(StickSerializer(sticks, many=True).data, safe=False)
        except:
            return JsonResponse({'message': "Error"}, status=404)

class EntryView(View):
    http_method_names = ['post', 'get']

    @staticmethod
    def get(request):
        remove_old_tokens()
        params = request.GET
        sticks = Stick.objects.all()
        try:
            storage_id = params['storage_id']
            sticks = Stick.objects.filter(storage_id=storage_id)
        except:
            return JsonResponse({'message': "No storage specified"}, status=404)
        token_value = request.META['HTTP_TOKEN']
        user = int(request.META['HTTP_USER'])
        expires = str_to_datetime(request.META['HTTP_EXPIRES'])
        token = AccessToken(user, token_value, expires)
        if not (token in active_tokens):
            print('token error')
            return JsonResponse({'message': 'Token expired'}, status=304)
        storage = Storage.objects.get(id=storage_id)
        if user != int(storage.owner_id):
            print('invalid owner of storage')
            return JsonResponse({'message': 'Permission denied'}, status=304)
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
        remove_old_tokens()
        args = request.POST
        try:
            token_value = request.META['HTTP_TOKEN']
            user = int(request.META['HTTP_USER'])
            expires = str_to_datetime(request.META['HTTP_EXPIRES'])
            token = AccessToken(user, token_value, expires)
            if not (token in active_tokens):
                print('token error')
                return JsonResponse({'message': 'Token expired'}, status=304)
            storage_id = Stick.objects.get(id=args['stick_id']).storage_id
            storage = Storage.objects.get(id=storage_id)
            if user != int(storage.owner_id):
                print('invalid owner of storage')
                return JsonResponse({'message': 'Permission denied'}, status=304)

            entry = Entry(send_id=args['send_id'], temp=args['temp'], height_level=args['height_level'], stick_id=args['stick_id'], time=args['time'])
            entry.save()
            return JsonResponse({'message': 'Entry was created successfully'}, status=201)
        except:
            return JsonResponse({'message': f'Stick with id={args["stick_id"]} doesnt exist'}, status=404)
