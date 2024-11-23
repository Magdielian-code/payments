
# Payments Tracker API

## Project Setup

1. Clone the repository

2. Create a virtual environment:
```bash
python -m venv venv_name
source venv/bin/activate  # If you are using Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django djangorestframework django-filter
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Core API Endpoints

### User Endpoints

```
GET /api/users/              # List all users
POST /api/users/             # Create a new user
GET /api/users/{id}/         # Retrieve a user
PUT /api/users/{id}/         # Update a user
DELETE /api/users/{id}/      # Delete a user
```

### Expense Endpoints

```
GET /api/expenses/           # List all expenses
POST /api/expenses/          # Create a new expense
GET /api/expenses/{id}/      # Retrieve an expense
PUT /api/expenses/{id}/      # Update an expense
DELETE /api/expenses/{id}/   # Delete an expense
```

### Special Endpoints

#### Date Range Filter
```
GET /api/expenses/date_range/?user={user_id}&start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}
```
Returns all expenses for a user within the specified date range.

#### Category Summary
```
GET /api/expenses/category_summary/?user={user_id}&month={YYYY-MM}
```
Returns the total expenses per category for a given month and user.

## Enhanced Features

### New User Statistics Endpoint
```
GET /api/users/{id}/statistics/
```
Returns comprehensive statistics including:
- Total expenses
- Category-wise breakdown
- Transaction counts per category

### Advanced Filtering Options
Available query parameters for `/api/expenses/`:
```
min_amount={value}          # Filter expenses >= amount
max_amount={value}          # Filter expenses <= amount
start_date={YYYY-MM-DD}     # Filter expenses from date
end_date={YYYY-MM-DD}       # Filter expenses until date
category={CATEGORY_NAME}    # Filter by specific category
search={text}              # Search in title and description
ordering={field_name}      # Sort by any field (prefix with - for descending)
```

### Expanded Categories
Now supporting more expense categories:
- Food
- Travel
- Utilities
- Entertainment
- Shopping
- Healthcare
- Education
- Transport
- Rent
- Insurance
- Other

### Enhanced Validation Rules
- Expense amount must be positive (greater than 0)
- Date cannot be in the future
- User email must be valid and unique
- Username must be unique
- Category must be one of the predefined choices

### Search and Sorting
- Search expenses by title and description
- Sort expenses by:
  - Date
  - Amount
  - Category
  - Creation date

## Data Formats

### User Object
```json
{
    "id": integer,
    "username": string,
    "email": string,
    "total_expenses": decimal,
    "created_at": datetime
}
```

### Expense Object
```json
{
    "id": integer,
    "user": integer,
    "user_username": string,
    "title": string,
    "amount": decimal,
    "date": string (YYYY-MM-DD),
    "category": string,
    "description": string,
    "created_at": datetime,
    "updated_at": datetime
}
```

### Category Summary Response
```json
{
    "month": "YYYY-MM",
    "total": decimal,
    "categories": [
        {
            "category": string,
            "total": decimal,
            "count": integer
        }
    ]
}
```

### User Statistics Response
```json
{
    "total_expenses": decimal,
    "category_breakdown": [
        {
            "category": string,
            "total": decimal,
            "count": integer
        }
    ]
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 400: Bad Request (invalid data)
- 404: Not Found
- 500: Server Error

Error response format:
```json
{
    "error": "Error message description"
}
```

## Testing

Run the test suite:
```bash
python manage.py test
```

Tests cover:
- User creation and validation
- Expense creation and validation
- Date range filtering
- Category summaries
- Invalid data handling
- Future date validation
- Negative amount validation