import datetime
import hashlib
import pytz

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, schema

from GrainSense.models import Gateway, Owner, SeedTypes, Storage, Stick, Entry
from django.http import JsonResponse
from django.views.generic import View
from GrainSense.my_token import *

from GrainSense.serializers import *

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def str_to_datetime(date_string):
    a = datetime.datetime.strptime(date_string, DATETIME_FORMAT)
    return a


def hashed_password(email, password):
    password_with_salt = password + email
    return hashlib.md5(password_with_salt.encode()).hexdigest()


@swagger_auto_schema(method='post')
@api_view(['POST'])
def login(request, email, password):
    remove_old_tokens()
    owner = Owner.objects.filter(email=email, password=hashed_password(email, password))
    if len(owner) == 0:
        return JsonResponse({'message': 'wrong email/password'}, status=403)
    token = AccessToken(owner[0].id)
    token.validate()
    print(active_tokens)
    return JsonResponse(str(token), safe=False, status=200)


@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
def register(request):
    remove_old_tokens()
    args = request.data
    owner = Owner.objects.filter(email=args['email'])
    if len(owner) > 0:
        return JsonResponse({'message': 'owner with such email already exists!'}, status=403)

    owner = Owner(username=args['username'], password=hashed_password(args['email'], args['password']), first_name=args['first_name'], last_name=args['last_name'], email=args['email'])
    owner.save()
    return JsonResponse({'message': f"Owner {args['last_name']} created successfully"})

@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_owner(request, http_user, http_token, http_expires):
    remove_old_tokens()
    expires = str_to_datetime(http_expires)
    token = AccessToken(http_user, http_token, expires)
    if not (token in active_tokens):
        return JsonResponse({'message': 'Token expired'}, status=304)
    return JsonResponse(OwnerSerializer(Owner.objects.get(id=http_user)).data, safe=False)


@swagger_auto_schema(method='post', request_body=PostSeedTypesSerializer)
@api_view(['POST'])
def post_seed_type(request):
    args = request.data
    seed_type = SeedTypes(lower_bound=args['lower_bound'], upper_bound=args['upper_bound'], name=args['name'])
    seed_type.save()
    return JsonResponse({'message': f"Seed type {args['name']} created successfully"})

@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_seed_type(request, id=None):
    objects = SeedTypes.objects.all()
    if id:
        objects = objects.filter(id=id)
    serial = SeedTypesSerializer(objects, many=True)
    return JsonResponse(serial.data, safe=False)

@swagger_auto_schema(method='post', request_body=PostStorageSerializer)
@api_view(['POST'])
def post_storage(request, http_user, http_token, http_expires):
    remove_old_tokens()
    args = request.data
    storage = Storage(address=args['address'], owner_id=args['owner_id'], seed_types_id=args['seed_types_id'])
    try:
        expires = str_to_datetime(http_expires)
        token = AccessToken(http_user, http_token, expires)
        if not (token in active_tokens):
            return JsonResponse({'message': 'Token expired'}, status=304)
        if http_user != int(args['owner_id']):
            return JsonResponse({'message': 'Permission denied'}, status=304)
        storage.save()
    except:
        return JsonResponse({'message': "No such owner or seed type exists"}, status=404)
    return JsonResponse({'message': "Storage created successfully"}, status=201)

@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_storage(request, http_user, http_token, http_expires):
    remove_old_tokens()
    expires = str_to_datetime(http_expires)
    token = AccessToken(http_user, http_token, expires)
    if not (token in active_tokens):
        return JsonResponse({'message': 'Token expired'}, status=304)
    objects = Storage.objects.all()
    objects = objects.filter(owner_id=http_user)
    serial = StorageSerializer(objects, many=True)
    return JsonResponse(serial.data, safe=False)


@swagger_auto_schema(method='post')
@api_view(['POST'])
def post_gateway(request, http_user, http_token, http_expires):
    remove_old_tokens()
    gateway = Gateway(owner_id=http_user)
    try:
        expires = str_to_datetime(http_expires)
        token = AccessToken(http_user, http_token, expires)
        if not (token in active_tokens):
            return JsonResponse({'message': 'Token expired'}, status=304)
        gateway.save()
    except:
        return JsonResponse({'message': "No such owner exists"}, status=404)
    return JsonResponse({'message': "Gateway created successfully"}, status=201)

@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_gateway(request, http_user, http_token, http_expires):
    remove_old_tokens()
    expires = str_to_datetime(http_expires)
    token = AccessToken(http_user, http_token, expires)
    if not (token in active_tokens):
        return JsonResponse({'message': 'Token expired'}, status=304)
    objects = Gateway.objects.all()
    objects = objects.filter(owner_id=http_user)
    serial = GatewaySerializer(objects, many=True)
    return JsonResponse(serial.data, safe=False)


@swagger_auto_schema(method='post', request_body=PostStickSerializer)
@api_view(['POST'])
def post_stick(request, http_user, http_token, http_expires):
    remove_old_tokens()
    args = request.data
    stick = Stick(gateway_id=args['gateway_id'], storage_id=args['storage_id'])
    try:
        expires = str_to_datetime(http_expires)
        token = AccessToken(http_user, http_token, expires)
        if not (token in active_tokens):
            print('token error')
            return JsonResponse({'message': 'Token expired'}, status=304)
        storage = Storage.objects.get(id=args['storage_id'])
        if http_user != int(storage.owner_id):
            print('invalid owner of storage')
            return JsonResponse({'message': 'Permission denied'}, status=304)
        gateway = Gateway.objects.get(id=args['gateway_id'])
        if http_user != int(gateway.owner_id):
            print('invalid owner of gateway')
            return JsonResponse({'message': 'Permission denied'}, status=304)
        stick.save()
    except:
        return JsonResponse({'message': "No such storage or gateway exists"}, status=404)
    return JsonResponse({'message': "Stick created successfully"}, status=201)

@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_sticks(request, gateway_id, http_user, http_token, http_expires) :
    remove_old_tokens()
    sticks = Stick.objects.all()
    try:
        expires = str_to_datetime(http_expires)
        token = AccessToken(http_user, http_token, expires)
        if not (token in active_tokens):
            print('token error')
            return JsonResponse({'message': 'Token expired'}, status=304)
        gateway = Gateway.objects.get(id=gateway_id)
        if http_user != int(gateway.owner_id):
            print('invalid owner of gateway')
            return JsonResponse({'message': 'Permission denied'}, status=304)
        sticks = sticks.filter(gateway_id=gateway_id)
        return JsonResponse(StickSerializer(sticks, many=True).data, safe=False)
    except:
        return JsonResponse({'message': "Error"}, status=404)

@swagger_auto_schema(methods=['get'])
@api_view(['GET'])
def get_entry(request, storage_id, http_user, http_token, http_expires):
    remove_old_tokens()
    sticks = Stick.objects.filter(storage_id=storage_id)
    expires = str_to_datetime(http_expires)
    token = AccessToken(http_user, http_token, expires)
    if not (token in active_tokens):
        print('token error')
        return JsonResponse({'message': 'Token expired'}, status=304)
    storage = Storage.objects.get(id=storage_id)
    if http_user != int(storage.owner_id):
        print('invalid owner of storage')
        return JsonResponse({'message': 'Permission denied'}, status=304)
    response = []
    for stick in sticks:
        entries = Entry.objects.filter(stick_id=stick.id)
        for entry in entries :
            response.append(entry)
    return JsonResponse(EntrySerializer(response, many=True).data, safe=False)

@swagger_auto_schema(method='post', request_body=EntrySerializer)
@api_view(['POST'])
def post_entry(request, http_user, http_token, http_expires):
    remove_old_tokens()
    args = request.data
    try:
        expires = str_to_datetime(http_expires)
        token = AccessToken(http_user, http_token, expires)
        if not (token in active_tokens):
            print('token error')
            return JsonResponse({'message': 'Token expired'}, status=304)
        storage_id = Stick.objects.get(id=args['stick_id']).storage_id
        storage = Storage.objects.get(id=storage_id)
        if http_user != int(storage.owner_id):
            print('invalid owner of storage')
            return JsonResponse({'message': 'Permission denied'}, status=304)

        entry = Entry(send_id=args['send_id'], temp=args['temp'], height_level=args['height_level'], stick_id=args['stick_id'], time=args['time'])
        entry.save()
        return JsonResponse({'message': 'Entry was created successfully'}, status=201)
    except:
        return JsonResponse({'message': f'Stick with id={args["stick_id"]} doesnt exist'}, status=404)
