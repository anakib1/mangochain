# messages/serializers.py
from rest_framework import serializers
from .models import Block, User, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userName', 'signature')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('from_id', 'to_id', 'tr_id', 'amount', 'signature')


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('content',)
