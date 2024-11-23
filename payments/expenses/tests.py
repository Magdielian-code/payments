from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from datetime import date, timedelta
from .models import User, Expense

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        self.user = User.objects.create(**self.user_data)

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'new@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_duplicate_email(self):
        url = reverse('user-list')
        data = {
            'username': 'another',
            'email': 'test@example.com'  # Same email as setUp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ExpenseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com'
        )
        self.expense_data = {
            'user': self.user.id,
            'title': 'Test Expense',
            'amount': '50.00',
            'date': date.today().isoformat(),
            'category': 'FOOD'
        }

    def test_create_expense(self):
        url = reverse('expense-list')
        response = self.client.post(url, self.expense_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)

    def test_negative_amount(self):
        url = reverse('expense-list')
        data = self.expense_data.copy()
        data['amount'] = '-50.00'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_future_date(self):
        url = reverse('expense-list')
        data = self.expense_data.copy()
        data['date'] = (date.today() + timedelta(days=1)).isoformat()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_date_range_filter(self):
        # Create some test expenses
        Expense.objects.create(**self.expense_data)
        
        url = reverse('expense-date-range')
        response = self.client.get(
            url,
            {'user': self.user.id,
             'start_date': (date.today() - timedelta(days=7)).isoformat(),
             'end_date': date.today().isoformat()
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_category_summary(self):
        Expense.objects.create(**self.expense_data)
        
        url = reverse('expense-category-summary')
        response = self.client.get(
            url,
            {'user': self.user.id,
             'month': date.today().strftime('%Y-%m')
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('categories' in response.data)