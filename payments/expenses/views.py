from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Expense
from .serializers import UserSerializer, ExpenseSerializer
from .filters import ExpenseFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'created_at']

    @action(detail=True, methods=['GET'])
    def statistics(self, request, pk=None):
        """Get user statistics including total expenses and category breakdown."""
        user = self.get_object()
        total_expenses = user.expenses.aggregate(total=Sum('amount'))
        category_breakdown = user.expenses.values('category').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')

        return Response({
            'total_expenses': total_expenses['total'] or 0,
            'category_breakdown': category_breakdown
        })

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'amount', 'category', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @action(detail=False, methods=['GET'])
    def date_range(self, request):
        """Filter expenses by date range for a specific user."""
        try:
            user_id = request.query_params.get('user')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            if not user_id:
                return Response(
                    {"error": "User ID is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset = self.get_queryset().filter(user_id=user_id)

            if start_date:
                try:
                    datetime.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(date__gte=start_date)
                except ValueError:
                    return Response(
                        {"error": "Invalid start_date format. Use YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            if end_date:
                try:
                    datetime.strptime(end_date, '%Y-%m-%d')
                    queryset = queryset.filter(date__lte=end_date)
                except ValueError:
                    return Response(
                        {"error": "Invalid end_date format. Use YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['GET'])
    def category_summary(self, request):
        """Calculate total expenses per category for a given month and user."""
        try:
            user_id = request.query_params.get('user')
            month = request.query_params.get('month')

            if not user_id:
                return Response(
                    {"error": "User ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not month:
                month = datetime.now().strftime('%Y-%m')

            try:
                year, month = map(int, month.split('-'))
            except ValueError:
                return Response(
                    {"error": "Invalid month format. Use YYYY-MM"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset = self.get_queryset().filter(
                user_id=user_id,
                date__year=year,
                date__month=month
            )

            summary = queryset.values('category').annotate(
                total=Sum('amount'),
                count=Count('id')
            ).order_by('-total')

            total = queryset.aggregate(total=Sum('amount'))

            return Response({
                'month': f"{year}-{month:02d}",
                'total': total['total'] or 0,
                'categories': summary
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )