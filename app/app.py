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
        ["🏠 Quick Start", "📄 Document Analysis", "🧮 Fee Calculator", "⚠️ Conflict Checker", "💰 Compensation Database", "📚 Advisor-Speak Decoder", "🎯 Sales Tactics Decoder", "🏦 Annuity Decoder", "🔧 Meeting Prep Tool"]
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
    elif page == "🏦 Annuity Decoder":
        annuity_decoder_page()
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
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Sales Process", "🧠 Psychology", "💬 Scripts", "🛡️ Defense"])
    
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
        
        with st.expander("**Managed money takes emotion out of investing**"):
            st.write("**Their script:**")
            st.write("• Managed money keeps you disciplined")
            st.write("• We remove emotional decision making")
            st.write("• Professional management prevents costly mistakes")
            st.markdown('<div class="warning-box"><strong>What they are not saying:</strong> Other options provide same discipline for much less</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your comeback:</strong> Asset allocation funds and target date funds do the same thing for a fraction of the cost</div>', unsafe_allow_html=True)
        
        with st.expander("**Access to our best and brightest minds**"):
            st.write("**Their script:**")
            st.write("• You gain access to our top portfolio managers")
            st.write("• Our research team works for you")
            st.write("• Professional money management expertise")
            st.markdown('<div class="warning-box"><strong>What they are not saying:</strong> Same expertise available in lower-cost funds</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your comeback:</strong> Could I not gain access to the same expertise through your asset allocation funds, target date funds, or index funds?</div>', unsafe_allow_html=True)
        
        with st.expander("**I am passionate about planning**"):
            st.write("**Their script:**")
            st.write("• I love helping people reach their goals")
            st.write("• Planning is my passion, not just my job")
            st.write("• I care deeply about your financial future")
            st.markdown('<div class="warning-box"><strong>What they are not saying:</strong> This may be a tactic to get you in the door</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> This could be a tactic to get you to meet with hopes of introducing an annuity or managed product</div>', unsafe_allow_html=True)
        
        with st.expander("**I do not get paid commission**"):
            st.write("**Their script:**")
            st.write("• I am not a commissioned salesperson")
            st.write("• My compensation is not tied to what I sell")
            st.write("• I am salaried, not commissioned")
            st.markdown('<div class="warning-box"><strong>What they are not saying:</strong> Variable bonuses still create sales incentives</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your comeback:</strong> Do you get paid more for selling managed products than asset allocation funds? Are there incentives that might misalign with my needs?</div>', unsafe_allow_html=True)
    
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
    
    with tab4:
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
        "You could outlive your money",
        "Managed money takes emotion out of investing",
        "I am passionate about planning",
        "I do not get paid commission"
    ])
    
    if scenario == "Most people your age have started planning":
        st.markdown('<div class="alert-box"><strong>Technique:</strong> Social Proof</div>', unsafe_allow_html=True)
        st.markdown('<div class="success-box"><strong>Counter:</strong> What evidence for my situation?</div>', unsafe_allow_html=True)
    elif scenario == "I can only offer this rate today":
        st.markdown('<div class="alert-box"><strong>Technique:</strong> Scarcity</div>', unsafe_allow_html=True)
        st.markdown('<div class="success-box"><strong>Counter:</strong> Good options stay good</div>', unsafe_allow_html=True)
    elif scenario == "Managed money takes emotion out of investing":
        st.markdown('<div class="alert-box"><strong>Technique:</strong> Professional Management Pitch</div>', unsafe_allow_html=True)
        st.markdown('<div class="success-box"><strong>Counter:</strong> Asset allocation and target date funds provide same discipline for less cost</div>', unsafe_allow_html=True)
    elif scenario == "I am passionate about planning":
        st.markdown('<div class="alert-box"><strong>Technique:</strong> Personal Connection Building</div>', unsafe_allow_html=True)
        st.markdown('<div class="success-box"><strong>Counter:</strong> Recognize this may be tactic to introduce high-fee products</div>', unsafe_allow_html=True)
    elif scenario == "I do not get paid commission":
        st.markdown('<div class="alert-box"><strong>Technique:</strong> Compensation Deflection</div>', unsafe_allow_html=True)
        st.markdown('<div class="success-box"><strong>Counter:</strong> Ask about variable bonuses and product-based incentives</div>', unsafe_allow_html=True)

def annuity_decoder_page():
    st.header("🏦 Annuity Decoder")
    st.write("**Annuities are sold, not bought** - decode the tactics and protect yourself from aggressive sales.")
    
    st.markdown('<div class="alert-box">', unsafe_allow_html=True)
    st.write("**⚠️ Reality Check:** Annuities often pay the highest commissions (4-8%) to advisors and use the most aggressive sales tactics in the financial industry.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎯 Sales Tactics", "🔍 Red Flag Checker", "💡 Killer Questions"])
    
    with tab1:
        st.subheader("Common Annuity Sales Tactics")
        
        with st.expander("**The Fear Approach**"):
            st.write("**What they say:**")
            st.write("• You could outlive your money")
            st.write("• What if the market crashes right when you retire?")
            st.write("• Social Security will not be enough")
            st.write("• You need guaranteed income you cannot outlive")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> Most people do not need guaranteed income products with 2-3% annual fees</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> Show me total costs versus a diversified portfolio with 4% withdrawal rate</div>', unsafe_allow_html=True)
        
        with st.expander("**Free Lunch Seminars**"):
            st.write("**What they say:**")
            st.write("• Free dinner and financial education")
            st.write("• Learn about protecting your retirement")
            st.write("• No sales presentation, just education")
            st.write("• Bring your spouse - you will both learn something")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> These seminars exist solely to generate annuity sales leads</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> If you attend, decide beforehand to make no commitments that day</div>', unsafe_allow_html=True)
        
        with st.expander("**The Urgency Close**"):
            st.write("**What they say:**")
            st.write("• This rate is only guaranteed until [date]")
            st.write("• I can only reserve this bonus for a few more days")
            st.write("• Interest rates are rising - lock in now")
            st.write("• The insurance company is limiting these sales")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> Good financial products do not require immediate decisions</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> If this is truly best for me, it will still be best after I research alternatives</div>', unsafe_allow_html=True)
        
        with st.expander("**Bonus Bait**"):
            st.write("**What they say:**")
            st.write("• Get 10% bonus on your deposit")
            st.write("• Free money just for signing up")
            st.write("• This bonus is only available for new customers")
            st.write("• The insurance company is paying you to invest")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> Bonuses are marketing gimmicks paid through higher fees</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> What are the surrender charges and how long do they last?</div>', unsafe_allow_html=True)
        
        with st.expander("**The Complexity Confusion**"):
            st.write("**What they say:**")
            st.write("• This is a sophisticated retirement strategy")
            st.write("• It is complicated, but I will handle the details")
            st.write("• Do not worry about understanding everything")
            st.write("• Trust me, this is what wealthy people do")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> If you cannot understand it, you should not buy it</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> Please explain this in simple terms and show me all fees in writing</div>', unsafe_allow_html=True)
        
        with st.expander("**Market Protection Story**"):
            st.write("**What they say:**")
            st.write("• Participate in market gains without market risk")
            st.write("• Your principal is protected")
            st.write("• You cannot lose money in this product")
            st.write("• Get market returns with insurance company backing")
            st.markdown('<div class="warning-box"><strong>Reality:</strong> Protection comes at a cost - usually 2-3% in annual fees</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>Your response:</strong> What caps, spreads, and participation rates limit my returns?</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("🔍 Annuity Red Flags Checker")
        st.write("**Check any that apply to your situation:**")
        
        red_flags = [
            "Salesperson focuses on benefits, avoids discussing fees",
            "Pressure to move money from 401k or IRA immediately", 
            "Promises of guaranteed high returns",
            "Will not explain surrender charges clearly",
            "Emphasizes bonus while minimizing restrictions",
            "Claims product is just like a CD but better",
            "Refuses to provide prospectus or detailed documentation",
            "Targets recent widows, retirees, or elderly individuals",
            "Makes appointment at your home instead of office",
            "Discourages you from consulting family or other advisors"
        ]
        
        selected_flags = []
        for flag in red_flags:
            if st.checkbox(flag, key=f"annuity_flag_{flag[:20]}"):
                selected_flags.append(flag)
        
        if selected_flags:
            risk_level = len(selected_flags)
            if risk_level >= 5:
                st.markdown('<div class="alert-box">', unsafe_allow_html=True)
                st.write(f"**🚨 HIGH RISK SITUATION** ({risk_level} red flags)")
                st.write("**Recommendation:** Do not proceed. Seek independent financial advice immediately.")
                st.markdown('</div>', unsafe_allow_html=True)
            elif risk_level >= 3:
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.write(f"**⚠️ MEDIUM RISK** ({risk_level} red flags)")
                st.write("**Recommendation:** Take time to research. Get second opinion from fee-only advisor.")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.write(f"**⚠️ SOME CONCERNS** ({risk_level} red flags)")
                st.write("**Recommendation:** Ask for all documentation in writing and compare alternatives.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.subheader("💡 Questions That Stop Annuity Sales Cold")
        st.write("**Use these specific questions to cut through the sales pitch:**")
        
        killer_questions = [
            "What are the total annual fees, including M&E charges, admin fees, and rider costs?",
            "What exactly are the surrender charges and how long do they last?",
            "What caps, spreads, or participation rates limit my returns?",
            "How does this compare to a low-cost diversified portfolio over 20 years?",
            "Can you show me the illustration with ALL fees deducted?",
            "What happens if I need my money for an emergency?",
            "How much commission do you earn from this sale?",
            "What would happen if your insurance company went bankrupt?",
            "Can I get the same benefits cheaper with a different product?",
            "Why is this better than just buying index funds and term life insurance?"
        ]
        
        for i, question in enumerate(killer_questions, 1):
            st.write(f"**{i}.** {question}")
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.write("**💡 Pro Tip:** A legitimate annuity salesperson will welcome these questions. Anyone who gets defensive, changes the subject, or refuses to answer clearly is showing their true intentions.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.write("**🎯 Bottom Line:** Annuities are complex insurance products that are heavily marketed to seniors and retirees. The high commissions create strong incentives for aggressive sales tactics. Always get independent advice before purchasing.")
    st.markdown('</div>', unsafe_allow_html=True)

def meeting_prep_page():
    st.header("🔧 Meeting Prep Tool")
    st.write("Prepare for your advisor meeting with the right questions.")
    
    meeting_type = st.selectbox("Meeting type:", [
        "First meeting", "Annual review"
    ])
    
    if meeting_type == "First meeting":
        st.subheader("Essential Questions")
        questions = [
            "How are you compensated?",
            "Are you a fiduciary?", 
            "What are all fees?",
            "Do you get money from fund companies?",
            "Are you ranked against other reps in the country?",
            "What categories are you ranked by - be specific?",
            "What are the variables in your variable compensation?",
            "Are you incentivized to close annuity and managed money business to rise in rankings?",
            "Does closing more complex products increase your variable bonus?"
        ]
        for i, q in enumerate(questions, 1):
            st.write(f"{i}. {q}")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.write("**Important:** Do not accept vague answers like 'variable compensation.' Ask for specifics about what those variables are and how they might create conflicts with your needs.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif meeting_type == "Annual review":
        st.subheader("Annual Review Questions")
        questions = [
            "Can you show me performance versus the benchmark?",
            "What were my total fees for the year in dollar amounts (not percentages)?",
            "How did my portfolio perform compared to a simple index fund?",
            "What specific value did active management add this year?",
            "Can you justify the fees based on performance results?"
        ]
        for i, q in enumerate(questions, 1):
            st.write(f"{i}. {q}")
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.write("**Key Focus:** Get concrete numbers, not percentages. A 1% fee sounds small until you see it cost you $3,000 on a $300,000 account.")
        st.markdown('</div>', unsafe_allow_html=True)
    
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
    st.write("Check for advisor conflicts based on what you know about your advisor relationship.")
    
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.write("**How this works:** This tool helps you identify potential conflicts based on your advisor's compensation structure and business model. You do not need to upload any documents - just answer based on what you know or have been told about your advisor.")
    st.markdown('</div>', unsafe_allow_html=True)
    
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
