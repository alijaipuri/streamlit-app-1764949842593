import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title='Personal Finance Dashboard', page_icon='💸')

st.title('📊 Personal Finance Dashboard')
st.markdown('Track and understand your financial activity with ease.')

# Sidebar inputs
with st.sidebar:
    st.header('Settings')
    uploaded_file = st.file_uploader('Upload your expenses and income CSV file', type=['csv'])
    savings_goal = st.number_input('Enter your monthly savings goal', min_value=0)
    category_map = {
        'Food': ['restaurant', 'grocery', 'dining'],
        'Bills': ['rent', 'utility', 'phone'],
        'Shopping': ['store', 'online', 'retail'],
        'Travel': ['hotel', 'flight', 'vacation']
    }
    st.info('Default category mapping:')
    for category, keywords in category_map.items():
        st.write(f'{category}: {", ".join(keywords)}')

# Main content
if uploaded_file:
    try:
        # Load data
        data = pd.read_csv(uploaded_file)
        st.write('Uploaded data:')
        st.dataframe(data.head())

        # Categorize transactions
        def categorize_transaction(description):
            for category, keywords in category_map.items():
                for keyword in keywords:
                    if keyword.lower() in description.lower():
                        return category
            return 'Miscellaneous'

        data['Category'] = data['Description'].apply(categorize_transaction)

        # Display spending patterns
        st.header('Spending Patterns')
        spending_by_category = data.groupby('Category')['Amount'].sum()
        fig, ax = plt.subplots()
        ax.pie(spending_by_category, labels=spending_by_category.index, autopct='%1.1f%%')
        st.pyplot(fig)

        spending_by_month = data.groupby(pd.Grouper(key='Date', freq='M'))['Amount'].sum()
        fig, ax = plt.subplots()
        ax.bar(spending_by_month.index, spending_by_month.values)
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Spending')
        st.pyplot(fig)

        # Savings goal tracker
        if savings_goal:
            st.header('Savings Goal Tracker')
            total_savings = data[data['Type'] == 'Income']['Amount'].sum() - data[data['Type'] == 'Expense']['Amount'].sum()
            progress = total_savings / savings_goal * 100
            st.metric('Savings Progress', f'{progress:.2f}%')
            if progress >= 100:
                st.success('You have reached your savings goal!')
            elif progress > 50:
                st.info('You are halfway to your savings goal.')
            else:
                st.warning('You still have a way to go to reach your savings goal.')
        else:
            st.error('Please enter a savings goal.')
    except Exception as e:
        st.error(f'Error processing uploaded file: {str(e)}')
else:
    st.info('Please upload a CSV file to get started.')
    st.write('Example CSV file structure:')
    st.write('Date,Type,Description,Amount')
    st.write('2022-01-01,Income,Salary,1000')
    st.write('2022-01-02,Expense,Rent,500')
    st.write('2022-01-03,Expense,Grocery,50')