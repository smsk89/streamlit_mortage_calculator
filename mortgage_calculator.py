import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

class MortgageCalculator:
    def __init__(self):
        pass

    def render(self):
        st.title("Калькулятор ипотечных процентов")

        st.write("### Ввод данных")
        col1, col2 = st.columns(2)
        home_value = col1.number_input("Стоимость жилья", min_value=0, value=500000)
        deposit = col1.number_input("Первоначальный взнос", min_value=0, value=100000)
        interest_rate = col2.number_input("Процентная ставка (в %)", min_value=0.0, value=5.5)
        loan_term = col2.number_input("Срок кредита (в годах)", min_value=1, value=30)

        # Calculate the repayments.
        loan_amount = home_value - deposit
        monthly_interest_rate = (interest_rate / 100) / 12
        number_of_payments = loan_term * 12
        monthly_payment = (
            loan_amount
            * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
            / ((1 + monthly_interest_rate) ** number_of_payments - 1)
        )

        # Display the repayments.
        total_payments = monthly_payment * number_of_payments
        total_interest = total_payments - loan_amount

        st.write("### Выплаты")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Ежемесячные выплаты", value=f"${monthly_payment:,.2f}")
        col2.metric(label="Общая сумма выплат", value=f"${total_payments:,.0f}")
        col3.metric(label="Общие проценты", value=f"${total_interest:,.0f}")

        # Create a data-frame with the payment schedule.
        schedule = []
        remaining_balance = loan_amount

        for i in range(1, number_of_payments + 1):
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            year = math.ceil(i / 12)  # Calculate the year into the loan
            schedule.append(
                [
                    i,
                    monthly_payment,
                    principal_payment,
                    interest_payment,
                    remaining_balance,
                    year,
                ]
            )

        df = pd.DataFrame(
            schedule,
            columns=["Месяц", "Платеж", "Основной долг", "Проценты", "Остаток долга", "Год"],
        )

        # Display the data-frame as a chart.
        st.write("### График платежей")
        payments_df = df[["Год", "Остаток долга"]].groupby("Год").min()
        st.line_chart(payments_df)
