from rest_framework import serializers
from .models import User, Expense
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    total_expenses = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True,
        required=False
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'total_expenses', 'created_at']
        read_only_fields = ['created_at']

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

class ExpenseSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'user_username', 'title', 'amount', 
            'date', 'category', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value

    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = dict(Expense.CATEGORY_CHOICES)[instance.category]
        return representation