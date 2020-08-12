from .models import Key
from .serializers import KeySerializer

def getKeys(e):
    key = Key.objects.get()
    key_ser = KeySerializer(key,many=False)
    return key_ser