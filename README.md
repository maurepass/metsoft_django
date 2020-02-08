### Application is deployed on the server and is in constant use in my current job.

### Application includes the following modules:
1.	offers: preparing technical requirement for clients requests, generate reports showing amount of prepared offers and processed casting by every employee, generate report showing amount of castings from specified material group
2.	patterns: managing patterns in the warehouse, generate report showing how long patterns for specified client where not used.
3.	prod_reports: generate many different reports from production process based on data from another server
4.  tech_dep: managing new orders in technology department, sending daily mail with task in progress and nonconformities since previous day
5.  users: authentication and password reset, logging of using specified paths by users

### Used functions:
- CRUD class-based views
- user authentication and authorization
- multiple databases
- template custom filters
- serialization
- middleware
- tests (unittest, mocking, pytest)
- send_mail
- job scheduling (django_extensions)

### Used tools:
- Django 2.2
- Django Rest Framework 3.9
- Datatables 1.10
- Django Crispy Forms
- Bootstrap 4.3
- jQuery 3.3
- HTML
- CSS
- MySQL
- Apache2
- Cron
