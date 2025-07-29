from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from .utils import calculate_emi, calculate_credit_score, corrected_interest_rate
from datetime import date, timedelta

class RegisterCustomerView(APIView):
    def post(self, request):
        data = request.data
        monthly_income = data.get("monthly_income")
        approved_limit = round((36 * monthly_income) / 100000) * 100000

        customer = Customer.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone_number=data.get("phone_number"),
            age=data.get("age"),
            monthly_salary=monthly_income,
            approved_limit=approved_limit
        )
        return Response({
            "customer_id": customer.customer_id,
            "name": f"{customer.first_name} {customer.last_name}",
            "age": customer.age,
            "monthly_income": customer.monthly_salary,
            "approved_limit": customer.approved_limit,
            "phone_number": customer.phone_number
        }, status=status.HTTP_201_CREATED)

class CheckEligibilityView(APIView):
    def post(self, request):
        data = request.data
        cid = data.get("customer_id")
        loan_amount = float(data.get("loan_amount"))
        interest_rate = float(data.get("interest_rate"))
        tenure = int(data.get("tenure"))

        try:
            customer = Customer.objects.get(customer_id=cid)
            loans = Loan.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        score = calculate_credit_score(customer, loans)

        corrected_rate = corrected_interest_rate(score)
        approval = True

        if corrected_rate is not None and interest_rate < corrected_rate:
            interest_rate = corrected_rate

        monthly_installment = calculate_emi(loan_amount, interest_rate, tenure)

        if customer.monthly_salary * 0.5 < monthly_installment:
            approval = False

        return Response({
            "customer_id": cid,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_rate if corrected_rate else interest_rate,
            "tenure": tenure,
            "monthly_installment": monthly_installment
        })

class CreateLoanView(APIView):
    def post(self, request):
        data = request.data
        cid = data.get("customer_id")
        loan_amount = float(data.get("loan_amount"))
        interest_rate = float(data.get("interest_rate"))
        tenure = int(data.get("tenure"))

        try:
            customer = Customer.objects.get(customer_id=cid)
            loans = Loan.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        score = calculate_credit_score(customer, loans)
        corrected_rate = corrected_interest_rate(score)

        if corrected_rate is not None and interest_rate < corrected_rate:
            interest_rate = corrected_rate

        monthly_installment = calculate_emi(loan_amount, interest_rate, tenure)

        if customer.monthly_salary * 0.5 < monthly_installment:
            return Response({
                "loan_id": None,
                "customer_id": cid,
                "loan_approved": False,
                "message": "EMI exceeds 50% of monthly income",
                "monthly_installment": monthly_installment
            })

        start_date = date.today()
        end_date = start_date + timedelta(days=30*tenure)
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=interest_rate,
            monthly_installment=monthly_installment,
            emis_paid_on_time=0,
            start_date=start_date,
            end_date=end_date,
        )

        return Response({
            "loan_id": loan.loan_id,
            "customer_id": cid,
            "loan_approved": True,
            "message": "Loan created successfully",
            "monthly_installment": monthly_installment
        })

class ViewLoanDetail(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.select_related('customer').get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=404)

        customer = loan.customer
        return Response({
            "loan_id": loan.loan_id,
            "customer": {
                "id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": customer.age,
            },
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "tenure": loan.tenure
        })

class ViewAllLoans(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        loans = Loan.objects.filter(customer=customer)
        loan_data = []
        for loan in loans:
            repayments_done = loan.emis_paid_on_time
            repayments_left = loan.tenure - repayments_done
            loan_data.append({
                "loan_id": loan.loan_id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "repayments_left": repayments_left
            })
        return Response(loan_data)