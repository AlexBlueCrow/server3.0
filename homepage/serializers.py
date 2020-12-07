from rest_framework import serializers
from . import models
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminUser
        fields = '__all__'

class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankInfo
        fields = '__all__'

class TcVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TcVideo
        fields = '__all__'

class VideoFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoFiles
        fields = '__all__'

class PicFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PicFiles
        fields = '__all__'

class VIMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VIMap
        fields = '__all__'
class tcVideo2ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.tcVideo2Item
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'

class PlatformAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlatformAccount
        fields = '__all__'

class TransactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transact
        fields = '__all__'

class CashingRequestSerializer(serializers.ModelSerializer):
    
    bankinfo =  BankInfoSerializer(source = 'account.owner.bankinfo')
    owner = serializers.CharField(source='account.owner.farminfo.name')
    class Meta:
        model = models.CashingRequest
        fields = '__all__'

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Key
        fields = '__all__'

class VIMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VIMap
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'