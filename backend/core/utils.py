import math
from datetime import date

def calculate_emi(principal, rate, time):
    monthly_rate = rate / (12 * 100)
    emi = (principal * monthly_rate * (1 + monthly_rate) ** time) / ((1 + monthly_rate) ** time - 1)
    return round(emi, 2)

def calculate_credit_score(customer, loans):
    score = 100

    total_loans = loans.count()
    if total_loans == 0:
        return score

    paid_on_time_ratio = sum([l.emis_paid_on_time for l in loans]) / (total_loans * max(l.tenure for l in loans))
    if paid_on_time_ratio < 0.5:
        score -= 40
    elif paid_on_time_ratio < 0.8:
        score -= 20

    current_year = date.today().year
    recent_loans = [l for l in loans if l.start_date.year == current_year]
    score -= len(recent_loans) * 2

    total_approved_volume = sum([l.loan_amount for l in loans])
    if total_approved_volume > customer.approved_limit:
        return 0

    return max(0, score)


def corrected_interest_rate(score):
    if score > 50:
        return None
    elif 30 < score <= 50:
        return 12.1
    elif 10 < score <= 30:
        return 16.1
    else:
        return 100.0
