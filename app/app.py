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

# Sample conflict of interest indicators (enhanced with real data)
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
        # Show what different fee levels cost
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
    st.write("**How advisors are trained to sell** - recognize the techniques and stay in control of the conversation.")
    
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.write("**💡 Key Insight:** Financial advisors receive extensive sales training using proven psychological techniques. Understanding their playbook helps you maintain control and make better decisions.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for different aspects of the sales process
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔄 The Sales Process", "🧠 Psychological Tactics", "💬 Scripted Responses", "🏦 Annuity Sales Tactics", "🛡️ Your Defense"])
    
    with tab1:
        st.subheader("The 5-Stage Sales Framework")
        st.write("**This is the exact process advisors are trained to follow:**")
        
        sales_stages = {
            "1. PREPARE": {
                "What they do": [
                    "Set primary objective (get you to commit)",
                    "Create secondary objective (fallback goal)",
                    "Research your background and potential assets"
                ],
                "What this means": "They've already decided what to sell you before you walk in the door.",
                "Your counter": "Come with YOUR agenda written down. Know exactly what questions you want answered."
            },
            
            "2. CONNECT": {
                "What they do": [
                    "Build rapport through personal conversation",
                    "Manage impressions to appear trustworthy",
                    "Seek common ground to establish likability",
                    "Propose a 'targeted agenda' (their agenda)",
                    "Value agenda items to create urgency"
                ],
                "What this means": "Everything feels natural, but it's calculated to make you like and trust them.",
                "Your counter": "Stay friendly but focused. Redirect conversation back to your questions and needs."
            },
            
            "3. EXPLORE": {
                "What they do": [
                    "Ask 'FIND' questions (Facts, Issues, Needs, Drivers)",
                    "Ask open-ended questions to uncover assets",
                    "Listen actively to identify emotional triggers",
                    "Confirm understanding to build agreement pattern"
                ],
                "What this means": "They're gathering ammunition - your fears, desires, and financial details to use in their pitch.",
                "Your counter": "Ask them questions too. 'How are you compensated?' 'What do you earn from different products?'"
            },
            
            "4. PRESENT": {
                "What they do": [
                    "Position potential solutions based on your stated needs",
                    "Refer to and emphasize benefits you mentioned",
                    "Link to drivers (your emotional motivations)",
                    "Address concerns preemptively"
                ],
                "What this means": "They use your own words against you to make the sale feel inevitable.",
                "Your counter": "Ask about alternatives: 'What if I just bought index funds?' 'What's the simplest option?'"
            },
            
            "5. DEVELOP": {
                "What they do": [
                    "Gain commitment through trial closes",
                    "Propose action steps to move forward",
                    "Secure agreement on next meeting",
                    "Demonstrate appreciation for your time",
                    "Check interest level constantly",
                    "Gain referrals from satisfied interaction"
                ],
                "What this means": "They're closing the sale through small commitments that lead to big ones.",
                "Your counter": "Always say you need time to think. 'I never make financial decisions in meetings.'"
            }
        }
        
        for stage, details in sales_stages.items():
            with st.expander(f"**{stage}**"):
                st.write("**What They're Trained To Do:**")
                for action in details["What they do"]:
                    st.write(f"• {action}")
                
                st.markdown(f'<div class="alert-box"><strong>What This Means For You:</strong> {details["What this means"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="success-box"><strong>Your Counter-Strategy:</strong> {details["Your counter"]}</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Psychological Manipulation Techniques")
        st.write("**Recognize these proven sales psychology tactics:**")
        
        psych_tactics = {
            "Reciprocity Principle": {
                "How it works": "They provide free advice, planning, or materials to make you feel obligated to buy.",
                "What to watch for": "Free financial plans, complimentary reviews, educational seminars",
                "Your response": "Remember: free advice from someone who earns commissions isn't actually free."
            },
            
            "Social Proof": {
                "How it works": "They mention other clients, success stories, or popularity to make you feel like everyone is doing it.",
                "What to watch for": "'Most of my clients choose this', 'This is our most popular option'",
                "Your response": "'What would be best for my specific situation, regardless of what others do?'"
            },
            
            "Scarcity & Urgency": {
                "How it works": "Creating false deadlines or limited availability to pressure quick decisions.",
                "What to watch for": "'This rate is only available until...', 'I can only take on a few more clients'",
                "Your response": "Any legitimate opportunity will still be good after you've had time to research."
            },
            
            "Authority Positioning": {
                "How it works": "Emphasizing credentials, awards, or firm reputation to appear more credible.",
                "What to watch for": "Certificates on walls, name-dropping, industry rankings",
                "Your response": "Credentials don't eliminate conflicts of interest. Still ask about compensation."
            },
            
            "Commitment Consistency": {
                "How it works": "Getting you to agree to small things that lead to bigger commitments.",
                "What to watch for": "'Do you agree that planning is important?' leading to larger commitments",
                "Your response": "Recognize when agreement questions are building toward a sale."
            },
            
            "Loss Aversion": {
                "How it works": "Focusing on what you'll lose if you don't act, rather than what you'll gain.",
                "What to watch for": "'You're missing out on...', 'You can't afford not to...'",
                "Your response": "'What exactly am I missing, and what does it cost?'"
            }
        }
        
        for tactic, details in psych_tactics.items():
            with st.expander(f"**{tactic}**"):
                st.write(f"**How It Works:** {details['How it works']}")
                st.write(f"**Watch For:** {details['What to watch for']}")
                st.markdown(f'<div class="success-box"><strong>Your Response:</strong> {details["Your response"]}</div>', unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Scripted Responses to Your Questions")
        st.write("**Advisors are trained with specific responses to common objections. Here's what they're taught to say:**")
        
        scripted_responses = {
            "When you ask about fees": {
                "Their script": [
                    "'The value we provide far exceeds the cost'",
                    "'You can't afford NOT to have professional management'", 
                    "'Our fees are competitive with the industry'",
                    "'The real cost is missing opportunities without us'"
                ],
                "What they're not saying": "Exactly how much they personally earn from your account",
                "Your comeback": "'Please show me all fees in writing, including what you earn from my investments.'"
            },
            
            "When you want to think about it": {
                "Their script": [
                    "'What specifically do you need to think about?'",
                    "'The best time to start was yesterday, the second best time is now'",
                    "'While you're thinking, you're missing opportunities'",
                    "'What would have to happen for you to feel comfortable moving forward?'"
                ],
                "What they're not saying": "Taking time to research will likely lead you to cheaper alternatives",
                "Your comeback": "'I always research major financial decisions. If this is right for me, it will still be right in a week.'"
            },
            
            "When you mention low-cost alternatives": {
                "Their script": [
                    "'You get what you pay for'",
                    "'Index funds don't provide personalized advice'",
                    "'There's more to investing than just low fees'",
                    "'Our active management can outperform in down markets'"
                ],
                "What they're not saying": "Most actively managed funds underperform index funds after fees",
                "Your comeback": "'Can you show me data proving your recommendations beat low-cost index funds after all fees?'"
            },
            
            "When you ask about conflicts of interest": {
                "Their script": [
                    "'We're fiduciaries, so we always act in your best interest'",
                    "'All financial professionals have some form of compensation'",
                    "'Our interests are aligned because we want you to succeed'",
                    "'Industry regulations ensure we treat you fairly'"
                ],
                "What they're not saying": "Even fiduciaries can have conflicts, and 'best interest' doesn't mean lowest cost",
                "Your comeback": "'Specifically, how does your compensation change based on what you recommend to me?'"
            },
            
            "When you want to compare options": {
                "Their script": [
                    "'Analysis paralysis prevents people from taking action'",
                    "'You can always make changes later'",
                    "'I've already done the comparison work for you'",
                    "'Shopping around will just confuse you with conflicting advice'"
                ],
                "What they're not saying": "Comparison shopping will likely reveal better deals elsewhere",
                "Your comeback": "'I appreciate your analysis, but I make all major decisions after comparing multiple options.'"
            }
        }
        
        for question, response_data in scripted_responses.items():
            with st.expander(f"**{question}**"):
                st.write("**Their Trained Responses:**")
                for script in response_data["Their script"]:
                    st.write(f"• {script}")
                
                st.markdown(f'<div class="warning-box"><strong>What They\'re Not Saying:</strong> {response_data["What they\'re not saying"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="success-box"><strong>Your Comeback:</strong> {response_data["Your comeback"]}</div>', unsafe_allow_html=True)
    
    with tab4:
        st.subheader("🏦 Annuity Sales Tactics")
        st.write("**Annuities are sold, not bought** - here are the specific tactics used to sell these complex products:")
        
        st.markdown('<div class="alert-box">', unsafe_allow_html=True)
        st.write("**⚠️ Reality Check:** Annuities often pay the highest commissions (4-8%) and have the most aggressive sales tactics. Here's their playbook:")
        st.markdown('</div>', unsafe_allow_html=True)
        
        annuity_tactics = {
            "The Fear Approach": {
                "Common phrases": [
                    "You could outlive your money",
                    "What if the market crashes right when you retire?",
                    "Social Security won't be enough",
                    "You need guaranteed income you can't outlive"
                ],
                "What they're doing": "Creating fear about market volatility and longevity to justify complex, high-fee products",
                "Reality check": "Most people don't need guaranteed income products with 2-3% annual fees",
                "Your response": "'Show me the total costs versus a diversified portfolio with a 4% withdrawal rate'"
            },
            
            "The 'Free' Lunch Seminar": {
                "Common phrases": [
                    "Free dinner and financial education",
                    "Learn about protecting your retirement",
                    "No sales presentation, just education",
                    "Bring your spouse - you'll both learn something"
                ],
                "What they're doing": "Using reciprocity principle - free meal creates obligation to listen to sales pitch",
                "Reality check": "These seminars exist solely to generate annuity sales leads",
                "Your response": "If you attend, decide beforehand that you won't make any commitments that day"
            },
            
            "The Urgency Close": {
                "Common phrases": [
                    "This rate is only guaranteed until [date]",
                    "I can only reserve this bonus for a few more days",
                    "Interest rates are rising - lock in now",
                    "The insurance company is limiting these sales"
                ],
                "What they're doing": "Creating false scarcity to prevent comparison shopping",
                "Reality check": "Good financial products don't require immediate decisions",
                "Your response": "'If this is truly the best option for me, it will still be best after I research alternatives'"
            },
            
            "The Complexity Confusion": {
                "Common phrases": [
                    "This is a sophisticated retirement strategy",
                    "It's complicated, but I'll handle the details",
                    "Don't worry about understanding everything",
                    "Trust me, this is what wealthy people do"
                ],
                "What they're doing": "Using complexity to hide fees and prevent comparison",
                "Reality check": "If you can't understand it, you shouldn't buy it",
                "Your response": "'Please explain this in simple terms and show me all fees in writing'"
            },
            
            "The Tax Deferral Pitch": {
                "Common phrases": [
                    "Grow your money tax-free",
                    "Defer taxes until retirement when you'll be in a lower bracket",
                    "It's like a 401k without contribution limits",
                    "The government wants you to save this way"
                ],
                "What they're doing": "Emphasizing tax benefits while hiding high fees that often outweigh tax advantages",
                "Reality check": "Tax deferral means nothing if fees are eating your returns",
                "Your response": "'How do the total fees compare to the tax benefits over time?'"
            },
            
            "The Bonus Bait": {
                "Common phrases": [
                    "Get a 10% bonus on your deposit",
                    "Free money just for signing up",
                    "This bonus is only available for new customers",
                    "The insurance company is paying you to invest"
                ],
                "What they're doing": "Using upfront bonuses to distract from high ongoing fees and surrender charges",
                "Reality check": "Bonuses are marketing gimmicks - they're paid for through higher fees",
                "Your response": "'What are the surrender charges and how long do they last?'"
            },
            
            "The Market Protection Story": {
                "Common phrases": [
                    "Participate in market gains without market risk",
                    "Your principal is protected",
                    "You can't lose money in this product",
                    "Get market returns with insurance company backing"
                ],
                "What they're doing": "Emphasizing protection while downplaying caps, fees, and limited returns",
                "Reality check": "Protection comes at a cost - usually 2-3% in annual fees",
                "Your response": "'What caps, spreads, and participation rates limit my returns?'"
            }
        }
        
        for tactic, details in annuity_tactics.items():
            with st.expander(f"**{tactic}**"):
                st.write("**What They Say:**")
                for phrase in details["Common phrases"]:
                    st.write(f"• \"{phrase}\"")
                
                st.write(f"**What They're Doing:** {details['What they\'re doing']}")
                
                st.markdown(f'<div class="warning-box"><strong>Reality Check:</strong> {details["Reality check"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="success-box"><strong>Your Response:</strong> {details["Your response"]}</div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("🔍 Annuity Red Flags Checklist")
        st.write("**Watch out for these specific annuity warning signs:**")
        
        annuity_red_flags = [
            "Salesperson focuses on benefits, avoids discussing fees",
            "Pressure to move money from 401k or IRA immediately", 
            "Promises of 'guaranteed' high returns",
            "Won't explain surrender charges clearly",
            "Emphasizes bonus while minimizing restrictions",
            "Claims product is 'just like a CD but better'",
            "Refuses to provide prospectus or detailed documentation",
            "Targets recent widows, retirees, or elderly individuals",
            "Makes appointment at your home instead of office",
            "Discourages you from consulting family or other advisors"
        ]
        
        st.write("**Check any that apply to your situation:**")
        selected_flags = []
        for flag in annuity_red_flags:
            if st.checkbox(flag, key=f"annuity_{flag[:20]}"):
                selected_flags.append(flag)
        
        if selected_flags:
            risk_level = len(selected_flags)
            if risk_level >= 5:
                st.markdown('<div class="alert-box">', unsafe_allow_html=True)
                st.write(f"**🚨 HIGH RISK SITUATION** ({risk_level} red flags)")
                st.write("**Recommendation:** Do not proceed. Seek independent financial advice before making any decisions.")
                st.markdown('</div>', unsafe_allow_html=True)
            elif risk_level >= 3:
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.write(f"**⚠️ MEDIUM RISK** ({risk_level} red flags)")
                st.write("**Recommendation:** Take time to research. Get a second opinion from a fee-only advisor.")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.write(f"**⚠️ SOME CONCERNS** ({risk_level} red flags)")
                st.write("**Recommendation:** Ask for all documentation in writing and compare with alternatives.")
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("---")
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
        st.write("**💡 Pro Tip:** A legitimate annuity salesperson will welcome these questions. Anyone who gets defensive, changes the subject, or refuses to answer clearly is showing you their true intentions.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.subheader("🛡️ Your Defense Strategy")
        st.write("**Stay in control with these proven counter-techniques:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Before the Meeting:**")
            st.write("• Write down your questions in advance")
            st.write("• Set a maximum time limit for the meeting")
            st.write("• Tell someone your plan beforehand")
            st.write("• Research average fees for what you need")
            st.write("• Decide you WON'T make decisions that day")
            
            st.write("**During the Meeting:**")
            st.write("• Stick to YOUR agenda, not theirs")
            st.write("• Take notes on everything they say")
            st.write("• Ask the compensation question early")
            st.write("• Request all information in writing")
            st.write("• Don't be afraid of awkward silences")
        
        with col2:
            st.write("**Magic Phrases That Work:**")
            st.write("• 'I never make financial decisions in meetings'")
            st.write("• 'Please put that in writing for me to review'")
            st.write("• 'How does your compensation change based on what I choose?'")
            st.write("• 'What would you recommend if you weren't paid differently for different products?'")
            st.write("• 'I need to compare this with other options'")
            
            st.write("**Red Flags to Leave Immediately:**")
            st.write("• Refuses to explain compensation clearly")
            st.write("• Won't put recommendations in writing") 
            st.write("• Gets defensive about your questions")
            st.write("• Uses high-pressure tactics")
            st.write("• Dismisses low-cost alternatives without data")
    
    st.write("---")
    st.subheader("🧪 Test Your Knowledge")
    st.write("**Can you spot the sales technique?**")
    
    scenario = st.selectbox("Choose a scenario:", [
        "Select a scenario...",
        "Advisor says: 'Most successful people your age have already started this type of planning'",
        "Advisor says: 'I can only offer this rate if we set this up today'", 
        "Advisor says: 'Let me give you this free retirement analysis to review'",
        "Advisor says: 'You agree that saving for retirement is important, right?'",
        "Advisor says: 'Without proper planning, you could outlive your money'"
    ])
    
    scenario_answers = {
        "Advisor says: 'Most successful people your age have already started this type of planning'": {
            "technique": "Social Proof",
            "explanation": "They're making you feel like you're behind or missing out compared to your peers.",
            "counter": "Ask: 'What specific evidence do you have that this is right for my situation?'"
        },
        "Advisor says: 'I can only offer this rate if we set this up today'": {
            "technique": "Scarcity & Urgency",
            "explanation": "Creating false time pressure to prevent you from researching alternatives.",
            "counter": "Response: 'If this is truly the best option for me, it will still be best after I've had time to compare.'"
        },
        "Advisor says: 'Let me give you this free retirement analysis to review'": {
            "technique": "Reciprocity Principle", 
            "explanation": "Creating a sense of obligation by providing something 'free' that will later justify their sales pitch.",
            "counter": "Remember: Nothing is truly free when it comes from someone earning commissions from your decisions."
        },
        "Advisor says: 'You agree that saving for retirement is important, right?'": {
            "technique": "Commitment Consistency",
            "explanation": "Getting you to agree to obvious statements that will later justify their specific recommendations.",
            "counter": "Recognize: 'Yes, retirement planning is important, but that doesn't mean YOUR specific product is right for me.'"
        },
        "Advisor says: 'Without proper planning, you could outlive your money'": {
            "technique": "Loss Aversion",
            "explanation": "Focusing on negative outcomes to create fear and urgency around their solution.",
            "counter": "Ask: 'What data do you have showing your approach prevents this better than low-cost alternatives?'"
        }
    }
    
    if scenario != "Select a scenario..." and scenario in scenario_answers:
        answer = scenario_answers[scenario]
        st.markdown(f'<div class="alert-box">', unsafe_allow_html=True)
        st.write(f"**Technique Used:** {answer['technique']}")
        st.write(f"**What's Happening:** {answer['explanation']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="success-box">', unsafe_allow_html=True)
        st.write(f"**Your Counter-Move:** {answer['counter']}")
        st.markdown('
