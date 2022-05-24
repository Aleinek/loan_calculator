import math
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--type', choices=['annuity', 'diff'], required=True, help="type")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--payment")

args = parser.parse_args()


# i = nominal interest rate // n = number of payments
# this function calculates pattern found in formulas
def pattern_calc(i, n):
    pattern = (i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)

    return pattern


# i = nominal interest rate // a = annuity payment // p = loan principal
# this function calculates number of month needed to pay off
def number_of_payments_calc(p, a, i):
    i = i / 1200

    n = round(math.log(a / (a - i * p), 1 + i))

    return n


# p = loan principal // i = interest rate // n = number of periods
# this function calculates annuity payment value
def annuity_payment_calc(p, n, i):
    i = i / 1200

    a = p * pattern_calc(i, n)

    return a


# a = annuity payment // i = interest rate // n = number of periods
def loan_principal_calc(a, n, i):
    i = i / 1200

    p = a / (pattern_calc(i, n))

    return p


def differentiated_payment(p, n, i):
    i = i / 1200
    payment = 0

    for m in range(n):
        d = math.ceil(p/n + i * (p - (p * m) / n))
        print(f'Month {m + 1}: payment is {d}')
        payment += d

    return payment

try:
    if args.type == 'diff':
        loan_principal = int(args.principal)
        number_of_periods = int(args.periods)
        loan_interest = float(args.interest)

        overpayment = differentiated_payment(loan_principal, number_of_periods, loan_interest) - loan_principal
        print(f'\nOverpayment = {overpayment}')
    if args.type == 'annuity':
        if args.principal is None:
            annuity_payment = int(args.payment)
            number_of_periods = int(args.periods)
            loan_interest = float(args.interest)

            loan_principal = math.floor(loan_principal_calc(annuity_payment, number_of_periods, loan_interest))
            overpayment = math.floor(annuity_payment * number_of_periods - loan_principal)

            print(f'Your loan principal = {loan_principal}!')
            print(f'Overpayment = {overpayment}')
        elif args.payment is None:
            loan_principal = int(args.principal)
            number_of_periods = int(args.periods)
            loan_interest = float(args.interest)

            annuity_payment = math.ceil(annuity_payment_calc(loan_principal, number_of_periods, loan_interest))
            overpayment = math.floor(annuity_payment * number_of_periods - loan_principal)

            print(f'Your annuity payment = {annuity_payment}!')
            print(f'Overpayment = {overpayment}')
        elif args.principal and args.payment is not None:
            loan_principal = int(args.principal)
            annuity_payment = int(args.payment)
            loan_interest = float(args.interest)

            number_of_months = number_of_payments_calc(loan_principal, annuity_payment, loan_interest)
            overpayment = math.floor(annuity_payment * number_of_months - loan_principal)

            if number_of_months == 1:
                print('It will take 1 month to repay this loan!')
            elif number_of_months % 12 == 0:
                years = math.floor(number_of_months / 12)

                print(f'It will take {years} years to repay this loan!')
            elif number_of_months > 12:
                years = math.floor(number_of_months / 12)
                months = number_of_months % 12 + 1

                print(f'It will take {years} years and {months} months to repay this loan!')
            else:
                print(f'It will take {number_of_months} months to repay this loan!')

            print(f'Overpayment = {overpayment}')
except TypeError:
    print('Incorrect parameters.')
