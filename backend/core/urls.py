from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterCustomerView.as_view()),
    path('check-eligibility', views.CheckEligibilityView.as_view()),
    path('create-loan', views.CreateLoanView.as_view()),
    path('view-loan/<int:loan_id>', views.ViewLoanDetail.as_view()),
    path('view-loans/<int:customer_id>', views.ViewAllLoans.as_view()),
]