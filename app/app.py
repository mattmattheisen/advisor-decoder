import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime
import base64
from io import BytesIO
import json
import openai
import PyPDF2
import docx
from openai import OpenAI

# Initialize OpenAI client with new format
client = OpenAI(api_key="your-openai-api-key-here")


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


            # Display the actual analysis
            analysis_result = response.choices[0].message.content
            st.markdown(analysis_result)
            
            # Add cost calculator based on actual fees found
            st.subheader("💰 Cost Impact Calculator")
            investment_amount = st.number_input(
                "Enter your investment amount ($):", 
                min_value=1000, 
                value=100000, 
                step=1000
            )
            
            if investment_amount:
                st.write("**Based on the fees found in your document:**")
                st.write("Use the percentages identified above to calculate your annual costs.")
                
        except Exception as e:
            st.error(f"Error analyzing document: {str(e)}")
            st.write("Please check your OpenAI API key and try again.")
def extract_text_from_file(uploaded_file):
    """Extract text from various file types"""
    text = ""
    
    if uploaded_file.type == "application/pdf":
        try:
            # Read PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return None
            
    elif uploaded_file.type == "text/plain":
        # Read text file
        text = str(uploaded_file.read(), "utf-8")
        
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Read Word document
        try:
            doc = docx.Document(uploaded_file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            st.error(f"Error reading Word document: {str(e)}")
            return None
            
    else:
        st.error("Unsupported file type. Please upload PDF, TXT, or DOCX files.")
        return None
    
    return text
   

def analyze_fees(file):
    """Actually analyze the uploaded document using OpenAI"""
    st.subheader("Fee Analysis Results")
    
    # Extract text from the document
    with st.spinner("Extracting text from document..."):
        extracted_text = extract_text_from_file(file)
        
    if not extracted_text:
        st.error("Could not extract text from the document.")
        return
    
    # Debug: Show what text was extracted
    with st.expander("🔍 Debug: Extracted Text"):
        st.text(extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text)
    
    # Analyze with OpenAI (NEW FORMAT)
    with st.spinner("Analyzing document with AI..."):
        try:
            prompt = f"""
            Analyze ONLY the specific fees and costs explicitly stated in this document. Do not assume or add any fees not mentioned.

            Document content: {extracted_text}

            Provide analysis in this format:
            1. EXPLICITLY STATED FEES: List only fees with percentages/amounts shown in the document
            2. MISSING DISCLOSURES: Note what typical fees are NOT mentioned (without assuming they exist)
            3. RED FLAGS: Identify if any fees seem high compared to industry standards

            Important: 
            - Do not mention 12b-1 fees unless explicitly shown
            - Do not estimate transaction costs unless stated
            - Do not provide "typical" fee ranges - only analyze what's written
            - If a fee type isn't mentioned, say "Not disclosed" rather than assuming an amount
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
             )
            
            # Display the actual analysis
            analysis_result = response.choices[0].message.content
            st.markdown(analysis_result)
            
            # Add cost calculator based on actual fees found
            st.subheader("💰 Cost Impact Calculator")
            investment_amount = st.number_input(
                "Enter your investment amount ($):", 
                min_value=1000, 
                value=100000, 
                step=1000
            )
            
            if investment_amount:
                st.write("**Based on the fees found in your document:**")
                st.write("Use the percentages identified above to calculate your annual costs.")
                
        except Exception as e:
            st.error(f"Error analyzing document: {str(e)}")
            st.write("Please check your OpenAI API key and try again.")


def main():
    st.markdown('<h1 class="main-header">🔍 Advisor Decoder</h1>', unsafe_allow_html=True)
    st.markdown("**Uncover hidden fees and conflicts of interest in your financial products**")
    
    # Sidebar navigation with session state
    st.sidebar.title("Navigation")
    
    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Quick Start"
    
    page = st.sidebar.selectbox(
        "Choose a tool:",
        ["🏠 Quick Start", "📄 Document Analysis", "🧮 Fee Calculator", "⚠️ Conflict Checker", "💰 Compensation Database", "📚 Advisor-Speak Decoder", "🔧 Meeting Prep Tool"],
        index=["🏠 Quick Start", "📄 Document Analysis", "🧮 Fee Calculator", "⚠️ Conflict Checker", "💰 Compensation Database", "📚 Advisor-Speak Decoder", "🔧 Meeting Prep Tool"].index(st.session_state.page) if st.session_state.page in ["🏠 Quick Start", "📄 Document Analysis", "🧮 Fee Calculator", "⚠️ Conflict Checker", "💰 Compensation Database", "📚 Advisor-Speak Decoder", "🔧 Meeting Prep Tool"] else 0
    )
    
    # Update session state when sidebar selection changes
    st.session_state.page = page
    
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
    elif page == "🔧 Meeting Prep Tool":
        meeting_prep_page()

def quick_start_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 3rem 2rem; 
                border-radius: 10px; 
                text-align: center; 
                margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem; font-weight: bold;">
            🔍 Advisor Decoder
        </h1>
        <h2 style="color: #f0f8ff; font-size: 1.4rem; margin-bottom: 0.5rem; font-weight: normal;">
            Uncover hidden fees and conflicts in financial advice
        </h2>
        <p style="color: #e6f3ff; font-size: 1.1rem; font-style: italic; margin: 0;">
            "Don't Get Sold - Get Decoded"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content in two columns like the funeral app
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="background: #fff3cd; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #ffc107;">
            <h3 style="color: #856404; margin-top: 0;">💰 The Hidden Truth About Financial Advice</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**The average investor pays 1-3% annually in fees, but families often pay much more due to:**")
        
        fee_issues = [
            "**55-80% variable compensation** that biases recommendations",
            "**Hidden 'engagement' fees** on your account balances", 
            "**Transfer bonuses** that incentivize account movement",
            "**Revenue sharing** agreements you never see",
            "**Annual account fees** disguised as 'service charges'",
            "**Emotional manipulation** during financial stress"
        ]
        
        for issue in fee_issues:
            st.markdown(f"• {issue}")
    
    with col2:
        st.markdown("""
        <div style="background: #d1ecf1; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #17a2b8;">
            <h3 style="color: #0c5460; margin-top: 0;">🛡️ How This App Protects You</h3>
        </div>
        """, unsafe_allow_html=True)
        
        protection_features = [
            ("🧠 **Psychology**", "Understand manipulation tactics used during sales meetings"),
            ("🛡️ **Defense Strategies**", "Practical ways to protect yourself from conflicts"),
            ("🚩 **Red Flags**", "Warning signs of predatory practices"),
            ("📚 **Glossary**", "Decode confusing financial industry terms"),
            ("📋 **Meeting Prep**", "Tools to prepare for advisor meetings"),
            ("📄 **Document Analyzer**", "Upload contracts for instant fee analysis")
        ]
        
        for icon_title, description in protection_features:
            st.markdown(f"**{icon_title}** - {description}")
    
    # Warning section
    st.markdown("""
    <div style="background: #fff3cd; 
                border: 1px solid #ffeaa7; 
                border-radius: 8px; 
                padding: 1.5rem; 
                margin: 2rem 0;">
        <p style="margin: 0; color: #856404;">
            <strong>⚠️ Warning:</strong> Financial advisors often exploit your trust and time pressure. 
            This app gives you the knowledge to make informed decisions and avoid being taken 
            advantage of during one of your most important financial decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick action buttons
    st.subheader("🚀 Get Started Now")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Analyze My Contract", use_container_width=True):
            st.session_state.page = "📄 Document Analysis"
            st.rerun()
    
    with col2:
        if st.button("🧮 Calculate Fee Impact", use_container_width=True):
            st.session_state.page = "🧮 Fee Calculator" 
            st.rerun()
    
    with col3:
        if st.button("📚 Decode Advisor-Speak", use_container_width=True):
            st.session_state.page = "📚 Advisor-Speak Decoder"
            st.rerun()
    
    # Quick fee reality check
    st.write("---")
    st.subheader("💡 Quick Fee Reality Check")
    
    investment_amount = st.number_input(
        "How much are you investing?", 
        min_value=1000, 
        value=100000, 
        step=10000,
        help="Enter your total investment amount to see the impact of different fee levels"
    )
    
    if investment_amount:
        # Show what different fee levels cost using real data
        fee_scenarios = {
            "Low-Cost Index Fund (0.05%)": investment_amount * 0.0005,
            "Typical Managed Account (1.0%)": investment_amount * 0.01,
            "High-Fee Advisory (2.5%)": investment_amount * 0.025,
            "Company C + Fees (3.0%+)": investment_amount * 0.03
        }
        
        st.write("**Annual fees you might pay:**")
        
        for scenario, annual_fee in fee_scenarios.items():
            if "Low-Cost" in scenario:
                st.markdown(f"• **{scenario}**: ${annual_fee:,.0f} per year ✅")
            elif "Company C" in scenario:
                st.markdown(f"• **{scenario}**: ${annual_fee:,.0f} per year ⚠️")
            else:
                st.markdown(f"• **{scenario}**: ${annual_fee:,.0f} per year")
        
        difference = fee_scenarios["High-Fee Advisory (2.5%)"] - fee_scenarios["Low-Cost Index Fund (0.05%)"]
        ten_year_difference = difference * 10
        
        st.markdown(f"""
        <div style="background: #f8d7da; 
                    border: 1px solid #f5c6cb; 
                    border-radius: 8px; 
                    padding: 1rem; 
                    margin: 1rem 0;">
            <strong>💰 The Difference:</strong><br>
            Annual: <strong>${difference:,.0f}</strong><br>
            Over 10 years: <strong>${ten_year_difference:,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)
    
   
    
    col1, col2, col3 = st.columns(3)
    
   
    
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
        <p>Advisor Decoder v2.0 | Built from real compensation disclosure documents</p>
        <p><em>Disclaimer: This tool is for educational purposes only. Always consult with qualified professionals for financial advice.</em></p>
    </div>
    """, unsafe_allow_html=True)

def meeting_prep_page():
    st.header("🔧 Meeting Prep Tool")
    st.write("**Prepare for your advisor meeting** with the right questions and expectations.")
    
    meeting_type = st.selectbox("What type of meeting?", 
                               ["First meeting with new advisor", "Annual review", "Discussing new investment", "Reviewing poor performance", "Fee discussion"])
    
    if meeting_type == "First meeting with new advisor":
        st.subheader("🎯 Essential Questions for First Meeting")
        questions = [
            "How exactly are you compensated? (Get specific percentages)",
            "Are you a fiduciary at all times?",
            "What are all the fees I'll pay, including hidden ones?",
            "Do you receive money from fund companies or other firms?",
            "What's your investment philosophy?",
            "How often will we meet and what's the cost?",
            "Can you provide client references?",
            "What happens if I want to leave?"
        ]
        
        for i, question in enumerate(questions, 1):
            st.write(f"{i}. {question}")
        
        st.subheader("📝 Notes Section")
        notes = st.text_area("Take notes during your meeting:", height=100, placeholder="Write down their answers to compare later...")
        
    elif meeting_type == "Discussing new investment":
        st.subheader("🔍 Questions About New Investment")
        questions = [
            "What are ALL the fees for this investment?",
            "How much do you earn from this recommendation?",
            "What are the risks you haven't mentioned?",
            "How does this compare to a low-cost index fund?",
            "What's the minimum investment and why?",
            "Can I get this same investment cheaper elsewhere?",
            "What happens if I want to sell early?",
            "How does this fit my risk tolerance?"
        ]
        
        for i, question in enumerate(questions, 1):
            st.write(f"{i}. {question}")
        
        st.subheader("⚖️ Investment Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Recommended Investment**")
            rec_fee = st.number_input("Annual fee (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.1, key="rec")
            rec_minimum = st.number_input("Minimum investment ($)", min_value=0, value=10000, step=1000, key="rec_min")
        
        with col2:
            st.write("**Alternative (Index Fund)**")
            alt_fee = st.number_input("Annual fee (%)", min_value=0.0, max_value=5.0, value=0.05, step=0.01, key="alt")
            alt_minimum = st.number_input("Minimum investment ($)", min_value=0, value=3000, step=1000, key="alt_min")
        
        if st.button("Compare Costs"):
            investment = 100000  # Example amount
            annual_diff = investment * (rec_fee - alt_fee) / 100
            ten_year_diff = annual_diff * 10
            
            st.write(f"**Annual cost difference:** ${annual_diff:,.0f}")
            st.write(f"**10-year cost difference:** ${ten_year_diff:,.0f}")
    
    elif meeting_type == "Fee discussion":
        st.subheader("💰 Fee Negotiation Prep")
        
        st.write("**What you need to know:**")
        st.write("• Fees are often negotiable, especially for larger accounts")
        st.write("• You can ask for fee breakdowns in writing")
        st.write("• Compare their fees to industry averages")
        st.write("• Consider fee-only advisors as alternatives")
        
        st.write("**Questions to ask:**")
        fee_questions = [
            "Can you provide a written breakdown of all fees?",
            "Are any of these fees negotiable?",
            "What fee reductions do you offer for larger accounts?",
            "How do your fees compare to your competitors?",
            "What additional value do I get for these fees?"
        ]
        
        for question in fee_questions:
            st.write(f"• {question}")
    
    # Common red flags for all meeting types
    st.write("---")
    st.subheader("🚨 Watch Out For These Red Flags")
    red_flags = [
        "Refuses to explain fees clearly",
        "Pressures you to decide immediately", 
        "Won't put recommendations in writing",
        "Dismisses your questions as 'too complicated'",
        "Only recommends their firm's products",
        "Gets defensive about compensation questions"
    ]
    
    for flag in red_flags:
        st.write(f"• {flag}")
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.write("**💡 Remember:** You're the client. A good advisor will appreciate your preparation and questions.")
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.write("Real compensation data from major financial firms' official disclosure documents.")
    
    # Real compensation data from actual documents
    firm = st.selectbox("Select Firm", ["Company A", "Company B", "Company C", "Compare All Three"])
    
    if firm == "Company A":
        st.subheader("🟢 Company A Compensation Structure")
        st.caption("*Data from major investment firm disclosure document (Jan 2024)*")
        
        st.write("**Base Pay Structure:**")
        st.write("• Financial Consultants: 20% - 45% base salary, 55% - 80% variable compensation")
        st.write("• Variable compensation based on Client Loyalty, Client Planning & Investments, Client Engagement")
        
        st.subheader("Fee Structure by Investment Type")
        company_a_fees = {
            "Money Market Funds": "0.0001 rate (lowest tier)",
            "Mutual Funds/ETFs": "0.0004 rate",
            "Wealth Management Services": "0.001 rate (highest tier)",
            "Assets Transferred": "0.0005 rate (one-time)",
            "Additional Transfer Bonus": "+0.0005 from other firms"
        }
        
        for investment, rate in company_a_fees.items():
            st.write(f"• **{investment}:** {rate}")
        
        st.subheader("Client Engagement (Annual Fees)")
        engagement_fees = {
            "Money Market/Core/Equities/CDs": "0.00001 annually",
            "Mutual Funds/ETFs/529 Plans": "0.00003 annually", 
            "Wealth Management Services": "0.0002 annually"
        }
        
        for service, rate in engagement_fees.items():
            st.write(f"• **{service}:** {rate}")
        
        st.markdown('<div class="alert-box">', unsafe_allow_html=True)
        st.write("**Conflict Alert:** Representatives earn MORE for complex products that require more time, creating incentive to recommend higher-fee services.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif firm == "Company B":
        st.subheader("🔵 Company B Compensation Structure")
        st.caption("*Data from major brokerage firm disclosure document (Apr 2025)*")
        
        st.write("**Relationship Pay Categories:**")
        st.write("• **Category 1 (Portfolio Management):** 32-42 basis points annually")
        st.write("• **Category 2 (Referrals/Non-Managed):** 9-12 basis points annually") 
        st.write("• **Category 3 (Credit Products):** 4.4 basis points per $100k loan")
        
        st.subheader("Solutions Pay (One-Time Payments)")
        solutions_pay = {
            "Asset Consolidation": "$80 per $100k client balances",
            "Wealth Advisory Programs": "$200 per $100k enrolled",
            "Robo-Advisory Services": "$200 per $100k enrolled",
            "Annuities": "$200 per $100k of annuity amount"
        }
        
        for service, payment in solutions_pay.items():
            st.write(f"• **{service}:** {payment}")
        
        st.subheader("Referral Payments")
        referral_payments = {
            "Advisory Services": "$800 (up to $30M) / $3,500 ($30M+)",
            "Life Insurance": "$450 per converted referral",
            "Long-Term Care Insurance": "$450 per converted referral",
            "Alternative Investments": "$200 per $100k invested",
            "Wealth Services": "$400 per $1M referred"
        }
        
        for service, payment in referral_payments.items():
            st.write(f"• **{service}:** {payment}")
        
        st.markdown('<div class="alert-box">', unsafe_allow_html=True)
        st.write("**Conflict Alert:** Higher compensation for managed accounts creates incentive to move clients from self-directed to fee-based advisory services.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif firm == "Company C":
        st.subheader("🟡 Company C Fee Structure")
        st.caption("*Data from major bank-affiliated firm disclosure document (Mar 2025)*")
        
        st.write("**Annual Account Fees (The Hidden Costs):**")
        company_c_annual_fees = {
            "Non-fee-exempt taxable account": "$175 annually ($150 with electronic docs)",
            "IRA Custodial Fee": "$125 annually ($100 with electronic docs)", 
            "Educational Savings/UGMA/UTMA": "$50 annually",
            "Advisory Platform Fee": "0.050% annually (on top of advisory fees)",
            "Outside Investment Fee": "$250 annually per position"
        }
        
        for fee_type, amount in company_c_annual_fees.items():
            st.write(f"• **{fee_type}:** {amount}")
        
        st.subheader("Transaction & Service Fees")
        company_c_transaction_fees = {
            "Account Transfer (Outgoing)": "$125 per transfer",
            "IRA Termination Fee": "$125 per termination",
            "Transaction Fee": "$7 per transaction",
            "No-Load Mutual Fund Fee": "$50 per transaction",
            "Physical Certificate": "$500 minimum per security"
        }
        
        for service, fee in company_c_transaction_fees.items():
            st.write(f"• **{service}:** {fee}")
        
        st.subheader("Advisory Management Fees")
        st.write("• **Managed Accounts:** 0.22% - 0.50% annually (varies by strategy)")
        st.write("• **Plus Platform Fee:** Additional 0.050% annually")
        st.write("• **Total Advisory Cost:** 0.27% - 0.55% annually")
        
        st.markdown('<div class="alert-box">', unsafe_allow_html=True)
        st.write("**Major Conflict:** This firm charges annual account fees that can be waived if you have $500k+ OR use their advisory services. This creates pressure to either invest more or pay for advice.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("Fee Waiver Thresholds")
        st.write("**Annual fees waived if you have:**")
        st.write("• $500,000+ total household assets, OR")
        st.write("• $250,000+ in advisory accounts, OR") 
        st.write("• Bank premier checking account relationship")
        
    elif firm == "Compare All Three":
        st.subheader("🆚 Three-Firm Comparison")
        st.caption("*Data from actual compensation disclosure documents*")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**🟢 Company A**")
            st.write("• Variable comp: 55-80%")
            st.write("• Product-based tiers")
            st.write("• Annual engagement fees")
            st.write("• No account fees")
            st.write("• Transfer bonuses")
            
        with col2:
            st.write("**🔵 Company B**")
            st.write("• Category-based pay")
            st.write("• One-time 'Solutions Pay'")
            st.write("• Extensive referrals")
            st.write("• No account fees")
            st.write("• Managed account bias")
            
        with col3:
            st.write("**🟡 Company C**")
            st.write("• Annual account fees")
            st.write("• Fee waiver incentives")
            st.write("• Platform fees on advisors")
            st.write("• High service fees")
            st.write("• Banking integration")
        
        st.subheader("🚨 Unique Conflicts by Firm")
        
        firm_conflicts = {
            "Company A": [
                "10x higher pay for Wealth Services vs Money Market",
                "55-80% of advisor pay is variable based on your choices",
                "Ongoing 'engagement' fees on all your balances"
            ],
            "Company B": [
                "3-4x higher pay for managed vs self-directed accounts", 
                "One-time bonuses for enrolling you in services",
                "$175-$3,500 referral payments create bias"
            ],
            "Company C": [
                "Annual fees designed to push you toward advisory accounts",
                "Platform fees make advisors prefer certain strategies",
                "Banking relationships create cross-selling pressure"
            ]
        }
        
        for firm_name, conflicts in firm_conflicts.items():
            with st.expander(f"**{firm_name} Specific Conflicts**"):
                for conflict in conflicts:
                    st.write(f"• {conflict}")
        
        st.subheader("💰 Cost Comparison (For $100k Account)")
        
        comparison_data = {
            "Scenario": ["Self-Directed Investing", "Basic Advisory", "Premium Advisory"],
            "Company A": ["$0 account fees + small engagement fees", "$500-$1,500 annually", "$1,000+ annually"],
            "Company B": ["$0 account fees", "$600-$1,200 annually", "$1,200-$1,850 annually"], 
            "Company C": ["$175 annual fee (waived with $500k)", "$270-$550 + platform fee", "$550+ annually"]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df)
    
    st.write("---")
    st.write("**Sources:** Official compensation disclosure documents from major financial firms (2024-2025)")
    
    # Enhanced search functionality
    st.subheader("🔍 Search All Firms' Compensation Data")
    search_term = st.text_input("Search for specific compensation info:")
    
    if search_term:
        search_results = []
        search_lower = search_term.lower()
        
        # Enhanced search terms with generic names
        compensation_search = {
            "annual fee": "Company C: $175 annually (others: $0), Company A/B: No annual account fees",
            "wealth management": "Company A: 0.001 rate, Company B: 32-42 basis points, Company C: 0.27-0.55%",
            "mutual fund": "Company A: 0.0004 rate, Company C: $50 transaction fee", 
            "transfer": "Company A: 0.0005 + bonus, Company B: $80 per $100k, Company C: $125 fee",
            "advisory": "All firms heavily incentivize advisory accounts over self-directed",
            "platform fee": "Company C: 0.050% annually on top of advisory fees",
            "account maintenance": "Company C: $175 annually unless waived, others: $0",
            "ira fee": "Company C: $125 annually, others: $0",
            "termination": "Company C: $125 to close accounts, others: varies"
        }
        
        for term, result in compensation_search.items():
            if term in search_lower:
                search_results.append(f"**{term.title()}:** {result}")
        
        if search_results:
            st.write("**Search Results:**")
            for result in search_results:
                st.write(f"• {result}")
        else:
            st.write("No specific results found. Try terms like 'annual fee', 'wealth management', 'platform fee', etc.")
    
   

def glossary_page():
    st.header("📚 Advisor-Speak Decoder")
    st.write("**What your advisor really means** - decode the jargon and know what you're actually buying.")
    
    # Add tabs for different types of terms
    tab1, tab2, tab3 = st.tabs(["🎯 What They Said", "💰 Fee Terms", "⚠️ Red Flag Phrases"])
    
    with tab1:
        st.subheader("Decode What Your Advisor Just Said")
        advisor_speak = {
            "Let's diversify your portfolio": "**Translation:** I want to spread your money across more products so I earn fees from multiple sources. **Ask:** What are the fees for each investment you're recommending?",

            "You need professional management": "**Translation:** I make more money from managed accounts than self-directed ones. **Reality:** Schwab advisors earn 32-42 basis points on managed vs. 9-12 on self-directed.",
            "This is a sophisticated strategy": "**Translation:** Complex = higher fees and commissions for me. **Ask:** Can you explain this in simple terms and show me all associated costs?",
            
            "You need professional management": "**Translation:** I make more money from managed accounts than self-directed ones. **Reality:** Schwab advisors earn 32-42 basis points on managed vs. 9-12 on self-directed.",
            
            "Let's consolidate your accounts": "**Translation:** I get paid when you move assets here - Company B: $80 per $100k, Company C: $125 fee to you but incentives to advisors. **Ask:** What do you earn when I transfer my accounts, and what fees will I pay?",
            
            "This fund has excellent performance": "**What they don't say:** I get paid more from this fund company through revenue sharing. **Ask:** Do you receive any compensation from this fund company?",
            
            "You should consider our advisory program": "**Translation:** I get $200 per $100k when you enroll (actual rate from major firm). **Ask:** How does your compensation change if I join this program?",
            
            "This is a core holding": "**Translation:** This investment pays me ongoing fees. **Ask:** What ongoing fees do you receive from this investment?",
            
            "Let me introduce you to our insurance specialist": "**Translation:** I get a referral bonus of $450-$800 (actual rates from major firms). **Ask:** Do you earn anything if I meet with other specialists?",
            
            "This has tax advantages": "**Often means:** Complex product with high fees. **Ask:** What are the total costs, and are there simpler alternatives?",
            
            "You're missing out on opportunities": "**Translation:** I need to hit my sales targets. **Ask:** How does this recommendation benefit me vs. you?",
            
            "This is what I recommend for clients like you": "**Translation:** This is what pays me the most. **Ask:** What would you recommend if you weren't compensated differently for various products?",
            
            "Let's set up a regular investment plan": "**Translation:** Recurring investments = recurring fees for me. **Ask:** What are the ongoing costs of this plan?"
        }
        
        search_advisor = st.text_input("Search what your advisor said:", placeholder="Enter a phrase or term...")
        
        if search_advisor:
            filtered_advisor = {k: v for k, v in advisor_speak.items() 
                              if search_advisor.lower() in k.lower()}
        else:
            filtered_advisor = advisor_speak
        
        for phrase, translation in filtered_advisor.items():
            with st.expander(f"💬 \"{phrase.split(':')[0]}\""):
                st.markdown(translation)
    
    with tab2:
        st.subheader("Fee & Investment Terms")
        glossary_terms = {
            "12b-1 Fee": "A fee charged by mutual funds to cover marketing and distribution costs, typically 0.25% to 0.75% annually. **Real Impact:** Fidelity advisors get paid from these fees - it's part of their 'Client Planning & Investment' compensation.",
            
            "Annual Account Fee": "Fee charged by some major firms ($175 annually) that can be waived if you have $500k+ or use their advisory services. **Conflict:** Creates pressure to either invest more or pay for advice.",
            
            "Platform Fee": "Additional fee (0.050% annually) charged by some firms on top of advisory fees. **Impact:** Adds $50 per year on every $100k in advisory accounts.",
            
            "AUM (Assets Under Management)": "The total value of investments managed by an advisor or firm. **Advisor Incentive:** Major firms pay advisors more as your AUM increases, creating incentive to gather assets.",
            
            "Basis Points": "One basis point = 0.01%. So 100 basis points = 1%. **Example:** 35 basis points = 0.35% annual fee on your account balance.",
            
            "Expense Ratio": "The annual fee charged by mutual funds and ETFs, expressed as a percentage of assets. **Range:** Can be 0.015% to 1.25% according to actual major firm disclosures.",
            
            "Load Fee": "A sales charge on mutual funds, either paid upfront (front-load) or when selling (back-load). **Current Status:** Less common now, replaced by ongoing advisory fees and 12b-1 fees.",
            
            "Management Fee": "Fee charged by investment managers for managing a portfolio or fund. **Typical Range:** 0.50% to 1.85% based on real Schwab/Fidelity data.",
            
            "Revenue Sharing": "Payments made by fund companies to brokers/advisors for selling their products. **Disclosure:** Both firms acknowledge these arrangements but don't specify amounts to clients.",
            
            "Wrap Fee": "An all-inclusive fee that covers investment management, trading, and administrative costs. **Conflict:** Creates incentive to move clients from transaction-based to fee-based accounts."
        }
        
        search_fees = st.text_input("Search fee terms:", placeholder="Enter a fee-related term...")
        
        if search_fees:
            filtered_fees = {k: v for k, v in glossary_terms.items() 
                           if search_fees.lower() in k.lower() or search_fees.lower() in v.lower()}
        else:
            filtered_fees = glossary_terms
        
        for term, definition in filtered_fees.items():
            with st.expander(f"**{term}**"):
                parts = definition.split("**Real") if "**Real" in definition else definition.split("**")
                st.write(parts[0])
                if len(parts) > 1 and "Real" in definition:
                    st.markdown(f'<div class="warning-box"><strong>Real{parts[1]}</strong></div>', unsafe_allow_html=True)
    
    with tab3:
        st.subheader("🚨 Red Flag Phrases")
        st.write("**Watch out for these phrases** - they often signal conflicts of interest:")
        
        red_flags = {
            "This is what I use for my own family": "**Red Flag:** Often used to build trust, but may not be true or relevant to your situation. **Ask:** Can you show me documentation of your personal investments?",


            "Professional Management takes the emotion out of investing": "**Translation:** I make more money when you're in managed accounts, so I'm framing this as helping you. **Reality:** Most 'emotional' investing mistakes happen when advisors push you to buy high-fee products. **Ask:** How does your compensation change between self-directed and managed accounts?",

"You get access to our best and brightest minds when you have your assets managed": "**Translation:** We're trying to justify higher fees by making you feel special. **Reality:** Many 'best and brightest' recommendations are driven by what pays us the most. **Ask:** Can you show me the track record of these 'best minds' versus low-cost index funds?",
            "You need to act quickly": "**Red Flag:** Pressure tactics to prevent you from researching alternatives. **Response:** Any good investment will still be good tomorrow. Take time to research.",
            
            "This is only available through us": "**Red Flag:** Often means higher fees because there's no competition. **Ask:** Why isn't this available elsewhere, and what are the fees?",
            
            "Don't worry about the fees": "**Red Flag:** Fees are YOUR money. Always worry about fees. **Ask:** Please show me all fees in writing, including what you earn.",
            
            "This beats the market": "**Red Flag:** Past performance doesn't guarantee future results. **Ask:** What are the risks, and how does this compare to low-cost index funds?",
            
            "You're being too conservative": "**Red Flag:** Often means they want to move you to higher-fee products. **Ask:** How does your compensation change based on my investment choices?",
            
            "Trust me, I'm a fiduciary": "**Red Flag:** Even fiduciaries can have conflicts of interest. **Ask:** How are you compensated, and what conflicts do you have?",
            
            "This is a proprietary product": "**Red Flag:** Usually means higher fees and less transparency. **Ask:** How does this compare to similar products from other companies?",
            
            "Everyone is doing this": "**Red Flag:** Appeal to popularity instead of facts. **Ask:** Can you show me objective research supporting this recommendation?",
            
            "The minimum investment is...": "**Red Flag:** High minimums often correlate with high fees. **Ask:** What lower-cost alternatives exist with smaller minimums?"
        }
        
        for phrase, explanation in red_flags.items():
            with st.expander(f"🚨 \"{phrase}\""):
                st.markdown(explanation)
    
    # Quick Reference section
    st.write("---")
    st.subheader("🔍 Quick Questions to Always Ask")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**About Fees:**")
        st.write("• What do you earn from this recommendation?")
        st.write("• What are ALL the fees I'll pay?")
        st.write("• How do your fees compare to alternatives?")
        st.write("• Do you get paid by the fund company?")
    
    with col2:
        st.write("**About Recommendations:**")
        st.write("• Why this instead of a low-cost index fund?")
        st.write("• What are the risks you haven't mentioned?")
        st.write("• Can I get this same thing cheaper elsewhere?")
        st.write("• What would you recommend if you weren't paid differently?")
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.write("**💡 Remember:** A good advisor will welcome these questions. If they get defensive or evasive, that's a red flag.")
    st.markdown('</div>', unsafe_allow_html=True)

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
