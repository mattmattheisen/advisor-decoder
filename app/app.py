import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime
import base64
from io import BytesIO
import json

# Page configuration
st.set_page_config(
    page_title="Advisor Decoder",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .alert-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sample fee data for common investments
COMMON_FEES = {
    "mutual_funds": {
        "expense_ratio": (0.005, 0.025),  # 0.5% to 2.5%
        "load_fees": (0.0, 0.0575),      # 0% to 5.75%
        "12b1_fees": (0.0, 0.0075),      # 0% to 0.75%
    },
    "annuities": {
        "mortality_expense": (0.005, 0.015),
        "administrative_fees": (0.001, 0.005),
        "surrender_charges": (0.0, 0.09),
        "rider_fees": (0.0025, 0.02),
    },
    "advisory_fees": {
        "aum_fees": (0.005, 0.02),  # 0.5% to 2%
        "financial_planning": (1000, 5000),  # Fixed fees
    }
}

# Sample conflict of interest indicators
CONFLICT_INDICATORS = [
    "commission-based compensation",
    "revenue sharing",
    "12b-1 fees",
    "trail commissions",
    "sales contests",
    "incentive trips",
    "preferred vendor relationships",
    "proprietary products"
]

def main():
    st.markdown('<h1 class="main-header">🔍 Advisor Decoder</h1>', unsafe_allow_html=True)
    st.markdown("**Uncover hidden fees and conflicts of interest in your financial products**")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a tool:",
        ["Document Analysis", "Fee Calculator", "Conflict Checker", "Compensation Database", "Glossary"]
    )
    
    if page == "Document Analysis":
        document_analysis_page()
    elif page == "Fee Calculator":
        fee_calculator_page()
    elif page == "Conflict Checker":
        conflict_checker_page()
    elif page == "Compensation Database":
        compensation_database_page()
    elif page == "Glossary":
        glossary_page()

def document_analysis_page():
    st.header("📄 Document Analysis")
    st.write("Upload your financial documents to analyze fees and terms.")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx', 'txt', 'jpg', 'png'],
        help="Upload financial statements, investment proposals, or annuity contracts"
    )
    
    if uploaded_file is not None:
        st.success("✅ File uploaded successfully!")
        
        # File info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        st.write("**File Details:**")
        for key, value in file_details.items():
            st.write(f"- {key}: {value}")
        
        # Analysis buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Analyze Fees"):
                analyze_fees(uploaded_file)
        
        with col2:
            if st.button("⚠️ Check Conflicts"):
                check_conflicts(uploaded_file)
        
        with col3:
            if st.button("📊 Generate Report"):
                generate_report(uploaded_file)

def analyze_fees(file):
    """Simulate fee analysis"""
    st.subheader("Fee Analysis Results")
    
    # Simulate extraction of fees
    with st.spinner("Analyzing document for hidden fees..."):
        import time
        time.sleep(2)  # Simulate processing time
        
        # Mock results
        fees_found = {
            "Management Fee": "1.25%",
            "Administrative Fee": "0.15%",
            "12b-1 Fee": "0.25%",
            "Expense Ratio": "0.68%",
            "Transaction Costs": "0.12%"
        }
        
        total_annual_cost = 2.45
        
        st.markdown('<div class="alert-box">', unsafe_allow_html=True)
        st.write(f"**Total Annual Cost: {total_annual_cost}%**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("**Fees Identified:**")
        for fee, rate in fees_found.items():
            st.write(f"• {fee}: {rate}")
        
        # Cost projection
        st.subheader("Cost Impact Analysis")
        investment_amount = st.number_input("Enter investment amount ($)", min_value=1000, value=100000, step=1000)
        years = st.slider("Investment period (years)", 1, 30, 10)
        
        annual_cost = investment_amount * (total_annual_cost / 100)
        total_cost = annual_cost * years
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Annual Cost", f"${annual_cost:,.0f}")
        with col2:
            st.metric("Total Cost Over Period", f"${total_cost:,.0f}")

def check_conflicts(file):
    """Check for conflicts of interest"""
    st.subheader("Conflict of Interest Analysis")
    
    with st.spinner("Scanning for potential conflicts..."):
        import time
        time.sleep(1.5)
        
        conflicts_found = [
            "Document mentions commission-based compensation",
            "Revenue sharing arrangements detected",
            "Proprietary product recommendations found"
        ]
        
        if conflicts_found:
            st.markdown('<div class="alert-box">', unsafe_allow_html=True)
            st.write("**⚠️ Potential Conflicts Identified:**")
            for conflict in conflicts_found:
                st.write(f"• {conflict}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("**Recommendations:**")
            st.write("• Ask your advisor about their compensation structure")
            st.write("• Request disclosure of all fees and commissions")
            st.write("• Consider fee-only advisors for unbiased advice")
        else:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.write("✅ No obvious conflicts detected")
            st.markdown('</div>', unsafe_allow_html=True)

def generate_report(file):
    """Generate comprehensive report"""
    st.subheader("📋 Comprehensive Analysis Report")
    
    report_data = {
        "Analysis Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Document": file.name,
        "Total Fees Identified": "2.45%",
        "Conflicts Found": 3,
        "Risk Level": "Medium",
        "Recommendations": [
            "Request fee-only consultation",
            "Compare with low-cost index funds",
            "Negotiate management fees"
        ]
    }
    
    st.json(report_data)
    
    # Download button for report
    report_json = json.dumps(report_data, indent=2)
    st.download_button(
        label="📥 Download Report",
        data=report_json,
        file_name=f"advisor_decoder_report_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

def fee_calculator_page():
    st.header("🧮 Fee Calculator")
    st.write("Calculate the true cost of your investments over time.")
    
    # Investment details
    col1, col2 = st.columns(2)
    
    with col1:
        investment_amount = st.number_input("Initial Investment ($)", min_value=100, value=100000, step=1000)
        annual_contribution = st.number_input("Annual Contribution ($)", min_value=0, value=12000, step=1000)
        years = st.slider("Investment Period (years)", 1, 40, 20)
    
    with col2:
        expected_return = st.slider("Expected Annual Return (%)", 1.0, 15.0, 7.0, 0.1)
        management_fee = st.slider("Management Fee (%)", 0.0, 3.0, 1.0, 0.05)
        other_fees = st.slider("Other Fees (%)", 0.0, 2.0, 0.5, 0.05)
    
    total_fee = management_fee + other_fees
    net_return = expected_return - total_fee
    
    # Calculate projections
    if st.button("Calculate Impact"):
        # With fees
        value_with_fees = investment_amount
        total_contributions = investment_amount
        
        for year in range(years):
            value_with_fees = value_with_fees * (1 + net_return/100) + annual_contribution
            total_contributions += annual_contribution
        
        # Without fees
        value_without_fees = investment_amount
        for year in range(years):
            value_without_fees = value_without_fees * (1 + expected_return/100) + annual_contribution
        
        fee_impact = value_without_fees - value_with_fees
        
        # Display results
        st.subheader("💰 Fee Impact Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Value with Fees", f"${value_with_fees:,.0f}")
        with col2:
            st.metric("Value without Fees", f"${value_without_fees:,.0f}")
        with col3:
            st.metric("Cost of Fees", f"${fee_impact:,.0f}", delta=f"-{fee_impact/total_contributions*100:.1f}%")
        
        # Visualization
        years_list = list(range(years + 1))
        with_fees_values = []
        without_fees_values = []
        
        val_with = investment_amount
        val_without = investment_amount
        
        with_fees_values.append(val_with)
        without_fees_values.append(val_without)
        
        for year in range(years):
            val_with = val_with * (1 + net_return/100) + annual_contribution
            val_without = val_without * (1 + expected_return/100) + annual_contribution
            with_fees_values.append(val_with)
            without_fees_values.append(val_without)
        
        chart_data = pd.DataFrame({
            'Year': years_list,
            'With Fees': with_fees_values,
            'Without Fees': without_fees_values
        })
        
        st.line_chart(chart_data.set_index('Year'))

def conflict_checker_page():
    st.header("⚠️ Conflict of Interest Checker")
    st.write("Identify potential conflicts in advisor relationships.")
    
    st.subheader("Common Conflict Indicators")
    
    # Checklist of conflicts
    conflicts = {
        "Commission-based compensation": False,
        "Proprietary product sales": False,
        "Revenue sharing agreements": False,
        "Sales contests/incentives": False,
        "Third-party payments": False,
        "Dual registration (broker/advisor)": False,
        "Limited product offerings": False,
        "High-fee product emphasis": False
    }
    
    st.write("Check any that apply to your advisor relationship:")
    
    selected_conflicts = []
    for conflict, default in conflicts.items():
        if st.checkbox(conflict, value=default):
            selected_conflicts.append(conflict)
    
    if st.button("Analyze Conflicts"):
        if selected_conflicts:
            risk_level = len(selected_conflicts)
            
            if risk_level <= 2:
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.write(f"**⚠️ Low Risk Level** ({risk_level} conflicts identified)")
                st.markdown('</div>', unsafe_allow_html=True)
            elif risk_level <= 4:
                st.markdown('<div class="alert-box">', unsafe_allow_html=True)
                st.write(f"**🚨 Medium Risk Level** ({risk_level} conflicts identified)")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-box">', unsafe_allow_html=True)
                st.write(f"**🔴 High Risk Level** ({risk_level} conflicts identified)")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("**Actions to Consider:**")
            recommendations = [
                "Request full disclosure of compensation structure",
                "Ask about fiduciary responsibility",
                "Compare recommendations with independent sources",
                "Consider fee-only financial advisors",
                "Get second opinions on major decisions"
            ]
            
            for rec in recommendations[:min(len(selected_conflicts) + 1, len(recommendations))]:
                st.write(f"• {rec}")
        else:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.write("✅ No conflicts identified from the checklist")
            st.markdown('</div>', unsafe_allow_html=True)

def compensation_database_page():
    st.header("💰 Compensation Database")
    st.write("Explore how major firms compensate advisors.")
    
    # Sample compensation data
    compensation_data = {
        "Fidelity": {
            "Asset Management": "0.35% - 0.85%",
            "Trading Commissions": "$0 - $4.95",
            "Advisory Services": "0.50% - 1.50%",
            "Fund Expense Ratios": "0.015% - 1.25%"
        },
        "Schwab": {
            "Asset Management": "0.28% - 0.90%",
            "Trading Commissions": "$0",
            "Advisory Services": "0.60% - 1.85%",
            "Fund Expense Ratios": "0.03% - 1.15%"
        }
    }
    
    firm = st.selectbox("Select Firm", list(compensation_data.keys()))
    
    if firm:
        st.subheader(f"{firm} Compensation Structure")
        
        firm_data = compensation_data[firm]
        
        for service, fee in firm_data.items():
            st.write(f"**{service}:** {fee}")
        
        st.write("---")
        st.write("**Note:** This data is for educational purposes. Always verify current fees with the firm directly.")

def glossary_page():
    st.header("📚 Financial Terms Glossary")
    st.write("Understanding key terms in financial advice and investing.")
    
    glossary_terms = {
        "12b-1 Fee": "A fee charged by mutual funds to cover marketing and distribution costs, typically 0.25% to 0.75% annually.",
        "Advisory Fee": "Fee paid to a financial advisor for investment advice and portfolio management services.",
        "AUM": "Assets Under Management - the total value of investments managed by an advisor or firm.",
        "Commission": "A fee paid to a broker or advisor for executing trades or selling financial products.",
        "Conflict of Interest": "A situation where an advisor's personal interests may conflict with their client's best interests.",
        "Expense Ratio": "The annual fee charged by mutual funds and ETFs, expressed as a percentage of assets.",
        "Fiduciary": "A legal obligation to act in the client's best interest, putting client needs before one's own.",
        "Load Fee": "A sales charge on mutual funds, either paid upfront (front-load) or when selling (back-load).",
        "Management Fee": "Fee charged by investment managers for managing a portfolio or fund.",
        "Revenue Sharing": "Payments made by fund companies to brokers/advisors for selling their products.",
        "Surrender Charge": "A fee charged for early withdrawal from certain investment products like annuities.",
        "Trail Commission": "Ongoing payments to advisors for as long as a client holds a particular investment.",
        "Wrap Fee": "An all-inclusive fee that covers investment management, trading, and administrative costs."
    }
    
    # Search functionality
    search_term = st.text_input("Search for a term:", placeholder="Enter a financial term...")
    
    if search_term:
        filtered_terms = {k: v for k, v in glossary_terms.items() 
                         if search_term.lower() in k.lower() or search_term.lower() in v.lower()}
    else:
        filtered_terms = glossary_terms
    
    # Display terms
    for term, definition in filtered_terms.items():
        with st.expander(f"**{term}**"):
            st.write(definition)
    
    if not filtered_terms and search_term:
        st.write("No terms found matching your search.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Advisor Decoder v1.0 | Built to promote financial transparency</p>
    <p><small>Disclaimer: This tool is for educational purposes only. Always consult with qualified professionals for financial advice.</small></p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
