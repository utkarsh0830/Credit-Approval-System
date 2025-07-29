from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField(default=18)
    monthly_salary = models.BigIntegerField()
    approved_limit = models.BigIntegerField() 
    current_debt = models.FloatField(default=0.0)

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.FloatField()
    tenure = models.IntegerField() 
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    emis_paid_on_time = models.IntegerField()
