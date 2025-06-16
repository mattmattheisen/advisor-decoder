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
        "expense_ratio": (0.005, 0.025),
        "load_fees": (0.0, 0.0575),
        "12b1_fees": (0.0, 0.0075),
    },
    "annuities": {
        "mortality_expense": (0.005, 0.015),
        "administrative_fees": (0.001, 0.005),
        "surrender_charges": (0.0, 0.09),
        "rider_fees": (0.0025, 0.02),
    },
    "advisory_fees": {
        "aum_fees": (0.005, 0.02),
        "financial_planning": (1000, 5000),
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
    "proprietary products",
    "relationship pay based on account balances",
    "solutions pay for enrollments", 
    "referral bonuses",
    "asset consolidation incentives",
    "category-based compensation tiers",
    "variable compensation 55-80% of total pay",
    "higher rates for complex products",
    "annual engagement fees on client balances"
]

def main():
    st.markdown('<h1 class="main-header">🔍 Advisor Decoder</h1>', unsafe_allow_html=True)
    st.markdown("**Uncover hidden fees and conflicts of interest in your financial products**")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a tool:",
        ["🏠 Quick Start", "📄 Document Analysis", "🧮 Fee Calculator", "⚠️ Conflict Checker", "💰 Compensation Database", "📚 Advisor-Speak Decoder", "🎯 Sales Tactics Decoder", "🔧 Meeting Prep Tool"]
    )
    
    if page == "🏠 Quick Start":
        quick_start_page()
    elif page == "📄 Document Analysis":
        document_analysis_page()
    elif page == "🧮 Fee Calculator":
        fee_calculator_page()
    elif page == "⚠️ Conflict Checker":
        conflict_checker_page()
    elif page == "💰 Compensation Database":
        compensation_database_page()
    elif page == "📚 Advisor-Speak Decoder":
        glossary_page()
    elif page == "🎯 Sales Tactics Decoder":
        sales_tactics_page()
    elif page == "🔧 Meeting Prep Tool":
        meeting_prep_page()

def quick_start_page():
    st.header("🏠 Quick Start Guide")
    st.write("**New to financial advice?** Start here to understand the basics.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Before Meeting an Advisor")
        st.write("**Essential Questions to Ask:**")
        st.write("• How are you compensated?")
        st.write("• Are you a fiduciary?")
        st.write("• What are all the fees I'll pay?")
        st.write("• Do you sell proprietary products?")
        
        st.subheader("📋 What to Bring")
        st.write("• Recent statements from all accounts")
        st.write("• List of current investments")
        st.write("• Your financial goals written down")
        st.write("• Questions about anything you don't understand")
    
    with col2:
        st.subheader("🚨 Immediate Red Flags")
        st.write("• Won't clearly explain their compensation")
        st.write("• Pressures you to 'act quickly'")
        st.write("• Dismisses your questions about fees")
        st.write("• Only recommends their firm's products")
        
        st.subheader("✅ Green Flags")
        st.write("• Welcomes your questions")
        st.write("• Explains fees clearly in writing")
        st.write("• Discusses low-cost alternatives")
        st.write("• Focuses on your goals, not products")
    
    st.write("---")
    st.subheader("🎯 Quick Fee Reality Check")
    
    investment_amount = st.number_input("How much are you investing?", min_value=1000, value=100000, step=10000)
    
    if investment_amount:
        fee_scenarios = {
            "Low-Cost Index Fund (0.05%)": investment_amount * 0.0005,
            "Typical Managed Account (1.0%)": investment_amount * 0.01,
            "High-Fee Product (2.5%)": investment_amount * 0.025
        }
        
        st.write("**Annual fees you might pay:**")
        for scenario, annual_fee in fee_scenarios.items():
            st.write(f"• {scenario}: **${annual_fee:,.0f}** per year")
        
        difference = fee_scenarios["High-Fee Product (2.5%)"] - fee_scenarios["Low-Cost Index Fund (0.05%)"]
        st.markdown(f'<div class="alert-box">💡 <strong>The difference between high and low fees: ${difference:,.0f} per year</strong></div>', unsafe_allow_html=True)

def sales_tactics_page():
    st.header("🎯 Sales Tactics Decoder")
    st.write("**How advisors are trained to sell** - recognize the techniques and stay in control.")
    
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.write("**💡 Key Insight:** Financial advisors receive extensive sales training using proven psychological techniques.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔄 Sales Process", "🧠 Psychology", "💬 Scripts", "🏦 Annuities", "🛡️ Defense"])
    
    with tab1:
        st.subheader("The 5-Stage Sales Framework")
        
        with st.expander("**1. PREPARE**"):
            st.write("**What they do:**")
            st.write("• Set primary objective (get you to commit)")
            st.write("• Research your background and assets")
            st.markdown('<div class="alert-box"><strong>What this means:</strong> They have decided what to sell before you arrive.</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your counter:</strong> Come with YOUR agenda written down.</div>', unsafe_allow_html=True)
        
        with st.expander("**2. CONNECT**"):
            st.write("**What they do:**")
            st.write("• Build rapport through personal conversation")
            st.write("• Manage impressions to appear trustworthy")
            st.markdown('<div class="alert-box"><strong>What this means:</strong> Everything feels natural but is calculated.</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your counter:</strong> Stay focused on your questions.</div>', unsafe_allow_html=True)
        
        with st.expander("**3. EXPLORE**"):
            st.write("**What they do:**")
            st.write("• Ask questions to uncover your assets")
            st.write("• Listen for emotional triggers")
            st.markdown('<div class="alert-box"><strong>What this means:</strong> They are gathering ammunition for their pitch.</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your counter:</strong> Ask them about their compensation.</div>', unsafe_allow_html=True)
        
        with st.expander("**4. PRESENT**"):
            st.write("**What they do:**")
            st.write("• Position solutions based on your stated needs")
            st.write("• Use your own words against you")
            st.markdown('<div class="alert-box"><strong>What this means:</strong> They make the sale feel inevitable.</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your counter:</strong> Ask about index fund alternatives.</div>', unsafe_allow_html=True)
        
        with st.expander("**5. DEVELOP**"):
            st.write("**What they do:**")
            st.write("• Gain commitment through small steps")
            st.write("• Secure agreement on next meeting")
            st.markdown('<div class="alert-box"><strong>What this means:</strong> Small commitments lead to big ones.</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your counter:</strong> Say you need time to think.</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Psychological Manipulation Techniques")
        
        techniques = {
            "Reciprocity": "Free advice creates obligation to buy",
            "Social Proof": "Everyone else is doing this",
            "Scarcity": "Limited time offer pressure",
            "Authority": "Credentials and reputation emphasis",
            "Consistency": "Small agreements lead to big ones",
            "Loss Aversion": "Focus on what you will lose"
        }
        
        for technique, description in techniques.items():
            with st.expander(f"**{technique}**"):
                st.write(f"**How it works:** {description}")
                st.markdown('<div class="success-box"><strong>Your response:</strong> Recognize the technique and ask direct questions about costs.</div>', unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Scripted Responses")
        
        with st.expander("**When you ask about fees**"):
            st.write("**Their script:**")
            st.write("• The value we provide exceeds the cost")
            st.write("• Our fees are competitive")
            st.markdown('<div class="warning-box"><strong>What they are not saying:</strong> How much they personally earn</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your comeback:</strong> Show me all fees in writing</div>', unsafe_allow_html=True)
        
        with st.expander("**When you want to think about it**"):
            st.write("**Their script:**")
            st.write("• The best time to start was yesterday")
            st.write("• You are missing opportunities")
            st.markdown('<div class="warning-box"><strong>What they are not saying:</strong> Research will find cheaper options</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your comeback:</strong> Good decisions take time</div>', unsafe_allow_html=True)
    
    with tab4:
        st.subheader("🏦 Annuity Sales Tactics")
        st.write("**Annuities pay the highest commissions (4-8%) and use the most aggressive tactics:**")
        
        with st.expander("**The Fear Approach**"):
            st.write("**What they say:**")
            st.write("• You could outlive your money")
            st.write("• Market crashes could ruin retirement")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> Most people do not need 2-3% annual fee products</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> Show me costs vs diversified portfolio</div>', unsafe_allow_html=True)
        
        with st.expander("**Free Lunch Seminars**"):
            st.write("**What they say:**")
            st.write("• Free dinner and education")
            st.write("• No sales presentation")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> These exist only to generate sales leads</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> Decide beforehand to make no commitments</div>', unsafe_allow_html=True)
        
        with st.expander("**Bonus Bait**"):
            st.write("**What they say:**")
            st.write("• Get 10% bonus on deposit")
            st.write("• Free money for signing up")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> Bonuses are paid through higher fees</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> What are surrender charges?</div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("🔍 Annuity Red Flags")
        
        red_flags = [
            "Focuses on benefits, avoids fees",
            "Pressure to move 401k money immediately",
            "Promises guaranteed high returns",
            "Will not explain surrender charges",
            "Targets elderly or recent widows"
        ]
        
        selected = []
        for flag in red_flags:
            if st.checkbox(flag, key=f"flag_{flag[:20]}"):
                selected.append(flag)
        
        if selected:
            risk = len(selected)
            if risk >= 3:
                st.markdown('<div class="alert-box">🚨 <strong>HIGH RISK - Do not proceed</strong></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ <strong>MEDIUM RISK - Get second opinion</strong></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("💡 Questions That Stop Annuity Sales")
        
        questions = [
            "What are total annual fees including all charges?",
            "What surrender charges and how long?",
            "What caps and participation rates limit returns?",
            "How much commission do you earn?",
            "Why not index funds and term insurance?"
        ]
        
        for i, q in enumerate(questions, 1):
            st.write(f"**{i}.** {q}")
    
    with tab5:
        st.subheader("🛡️ Your Defense Strategy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Before Meeting:**")
            st.write("• Write questions in advance")
            st.write("• Set time limit")
            st.write("• Decide not to buy that day")
            
            st.write("**During Meeting:**")
            st.write("• Stick to YOUR agenda")
            st.write("• Take notes")
            st.write("• Ask compensation early")
        
        with col2:
            st.write("**Magic Phrases:**")
            st.write("• I never decide in meetings")
            st.write("• Put that in writing")
            st.write("• How does your pay change?")
            
            st.write("**Leave If They:**")
            st.write("• Refuse to explain compensation")
            st.write("• Will not put in writing")
            st.write("• Get defensive about questions")
    
    st.write("---")
    st.subheader("🧪 Test Your Knowledge")
    
    scenario = st.selectbox("Choose scenario:", [
        "Select...",
        "Most people your age have started planning",
        "I can only offer this rate today",
        "Free retirement analysis",
        "You agree planning is important?",
        "You could outlive your money"
    ])
    
    if scenario == "Most people your age have started planning":
        st.markdown('<div class="alert-box"><strong>Technique:</strong> Social Proof</div>', unsafe_allow_html=True)
        st.markdown('<div class="success-box"><strong>Counter:</strong> What evidence for my situation?</div>', unsafe_allow_html=True)
    elif scenario == "I can only offer this rate today":
        st.markdown('<div class="alert-box"><strong>Technique:</strong> Scarcity</div>', unsafe_allow_html=True)
        st.markdown('<div class="success-box"><strong>Counter:</strong> Good options stay good</div>', unsafe_allow_html=True)

def meeting_prep_page():
    st.header("🔧 Meeting Prep Tool")
    st.write("Prepare for your advisor meeting with the right questions.")
    
    meeting_type = st.selectbox("Meeting type:", [
        "First meeting", "Annual review", "New investment", "Fee discussion"
    ])
    
    if meeting_type == "First meeting":
        st.subheader("Essential Questions")
        questions = [
            "How are you compensated?",
            "Are you a fiduciary?", 
            "What are all fees?",
            "Do you get money from fund companies?"
        ]
        for i, q in enumerate(questions, 1):
            st.write(f"{i}. {q}")
    
    st.write("---")
    st.subheader("Red Flags")
    flags = [
        "Refuses to explain fees",
        "Pressures quick decisions",
        "Will not put in writing",
        "Gets defensive about questions"
    ]
    for flag in flags:
        st.write(f"• {flag}")

def document_analysis_page():
    st.header("📄 Document Analysis")
    st.write("Upload financial documents to analyze fees.")
    
    uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file:
        st.success("File uploaded!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Analyze Fees"):
                st.write("**Estimated Annual Fees:** 2.45%")
                st.write("• Management: 1.25%")
                st.write("• Fund expenses: 0.68%") 
                st.write("• Other fees: 0.52%")
        
        with col2:
            if st.button("Check Conflicts"):
                st.write("**Conflicts Found:**")
                st.write("• Commission compensation")
                st.write("• Revenue sharing")
        
        with col3:
            if st.button("Generate Report"):
                st.json({
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Total_Fees": "2.45%",
                    "Risk_Level": "Medium"
                })

def fee_calculator_page():
    st.header("🧮 Fee Calculator")
    st.write("Calculate investment fees over time.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Investment ($)", value=100000)
        contribution = st.number_input("Annual addition ($)", value=12000)
        years = st.slider("Years", 1, 30, 20)
    
    with col2:
        return_rate = st.slider("Expected return (%)", 1.0, 15.0, 7.0)
        fees = st.slider("Total fees (%)", 0.0, 3.0, 1.0)
    
    if st.button("Calculate"):
        net_return = return_rate - fees
        
        # Simple calculation
        final_with_fees = amount * (1 + net_return/100) ** years
        final_without_fees = amount * (1 + return_rate/100) ** years
        difference = final_without_fees - final_with_fees
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("With Fees", f"${final_with_fees:,.0f}")
        with col2:
            st.metric("Without Fees", f"${final_without_fees:,.0f}")
        with col3:
            st.metric("Fee Cost", f"${difference:,.0f}")

def conflict_checker_page():
    st.header("⚠️ Conflict Checker")
    st.write("Check for advisor conflicts.")
    
    conflicts = [
        "Commission compensation",
        "Proprietary products",
        "Revenue sharing",
        "Sales incentives"
    ]
    
    selected = []
    for conflict in conflicts:
        if st.checkbox(conflict):
            selected.append(conflict)
    
    if st.button("Analyze"):
        if selected:
            risk = len(selected)
            if risk >= 3:
                st.error(f"High risk: {risk} conflicts")
            else:
                st.warning(f"Medium risk: {risk} conflicts")
        else:
            st.success("No conflicts identified")

def compensation_database_page():
    st.header("💰 Compensation Database")
    st.write("Real advisor compensation data.")
    
    firm = st.selectbox("Firm", ["Fidelity", "Schwab", "Both"])
    
    if firm == "Fidelity":
        st.write("**Fidelity Structure:**")
        st.write("• 55-80% variable compensation")
        st.write("• 0.001 rate for wealth management")
        st.write("• 0.0004 rate for mutual funds")
        
    elif firm == "Schwab":
        st.write("**Schwab Structure:**")
        st.write("• 32-42 basis points for managed accounts")
        st.write("• $200 per $100k for advisory enrollment")
        st.write("• Various referral bonuses")
    
    else:
        st.write("**Key Differences:**")
        st.write("• Fidelity: Product-based tiers")
        st.write("• Schwab: Category-based pay")
        st.write("• Both: Higher pay for complex products")

def glossary_page():
    st.header("📚 Advisor-Speak Decoder")
    st.write("Decode what advisors really mean.")
    
    tab1, tab2 = st.tabs(["What They Said", "Fee Terms"])
    
    with tab1:
        phrases = {
            "Diversify your portfolio": "I want fees from multiple products",
            "Sophisticated strategy": "Complex = higher fees for me",
            "Professional management": "I earn more from managed accounts",
            "Consolidate accounts": "I get paid when you transfer money"
        }
        
        for phrase, meaning in phrases.items():
            with st.expander(f'"{phrase}"'):
                st.write(f"**Translation:** {meaning}")
    
    with tab2:
        terms = {
            "12b-1 Fee": "Fund marketing fee (0.25-0.75% annually)",
            "Advisory Fee": "Fee for investment advice and management", 
            "Expense Ratio": "Annual fund fee (0.015-1.25%)",
            "Revenue Sharing": "Payments from funds to advisors"
        }
        
        for term, definition in terms.items():
            with st.expander(f"**{term}**"):
                st.write(definition)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Advisor Decoder v1.0 | Built to promote financial transparency</p>
    <p><small>Disclaimer: Educational purposes only. Consult professionals for advice.</small></p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
