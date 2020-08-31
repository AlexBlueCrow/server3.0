from rest_framework import serializers
from .models import AppUser, Item, Order, Prepay_Order, Comments, Captain, FarmUser, Sell, Adopt
from homepage.serializers import VIMapSerializer
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'


class AdoptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopt
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    Sell = SellSerializer(many=False, read_only=True)
    Adopt = AdoptSerializer(many=False, read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    itemname = serializers.CharField(source='item.name')
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
