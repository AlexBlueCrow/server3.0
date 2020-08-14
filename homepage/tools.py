from .models import Key
from .serializers import KeySerializer

def getKeys():
    key = Key.objects.get(account='qj')
    key_ser = KeySerializer(key,many=False)
    print(key_ser)
    return key_ser