from rest_framework import serializers
from .models import User,Item,Order,Prepay_Order,Comments,Captain,FarmUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class Prepay_OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prepay_Order
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class CaptainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captain
        fields = '__all__'

class FarmUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmUser
        fields = '__all__'