from rest_framework import serializers
from .models import Category, Expense, Budget

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source= 'category.name')

    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
