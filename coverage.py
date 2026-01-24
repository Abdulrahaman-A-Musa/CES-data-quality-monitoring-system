# =============================================================================
# SARMAAN II COVERAGE EVALUATION DASHBOARD - Katsina STATE
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO, StringIO
import requests

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="SARMAAN II Coverage Evaluation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USERNAME = "Admin"

# LGA username to LGA name mapping (no passwords needed)
LGA_CREDENTIALS = {
    "ingawa": "Ingawa",
    "kankara": "Kankara",
    "kankia": "Kankia",
    "mani": "Mani",
    "musawa": "Musawa",
    "rimi": "Rimi",
}


KOBO_DATA_URL = "https://kf.kobotoolbox.org/api/v2/assets/ahaqJZxr7kvAbYRje7GMeP/export-settings/esmSMyurMwphmn8cFPFN4WQ/data.xlsx"

# ---------------- COMMUNITY MAPPING DATA ----------------
COMMUNITY_MAPPING_DATA = """Q2. Local Government Area	Q3.Ward	community_name	Q4. Community Name	Planned HH
Ingawa	Agayawa	80111	Mattallawa Unguwan Huri	30
Ingawa	Agayawa	80112	Yallami Gabas	30
Ingawa	Bareruwa	80121	Santa Ruruma	30
Ingawa	Bareruwa	80122	Kuringihi	30
Kankara	Burdugau	80211	Sunkui Sabauwa	30
Kankara	Burdugau	80212	Dankalgo Layin Rabe	30
Kankara	Dan Murabu	80221	Tsamiyar Sarki	30
Kankara	Dan Murabu	80222	Matsiga Kudu	30
Kankia	Fakuwa Kafin Dangi	80311	Rugar Allo	30
Kankia	Fakuwa Kafin Dangi	80312	Yamade	30
Kankia	Galadima A	80321	Bakin Kasuwar Halilu	30
Kankia	Galadima A	80322	Kauyen Dawa Layin Labo	30
Mani	Bagiwa	80411	Nasarawa Kainawa	30
Mani	Bagiwa	80412	Dungun Agala	30
Mani	Bujawa	80421	Kwangwama Galadinawa	30
Mani	Bujawa	80422	Nasarawa Bagawa	30
Musawa	Garu	80511	Gangara	30
Musawa	Garu	80512	Garu Unguwar Gabas	30
Musawa	Danjanku Karachi	80521	Gidan Lumu	30
Musawa	Danjanku Karachi	80522	Alkalawa	30
Rimi	Abukur	80611	Bayan Garin Malam Yau	30
Rimi	Abukur	80612	Bayan Garin Malam Basiru	30
Rimi	Fardami	80621	Makwalla Akatsaba	30
Rimi	Fardami	80622	Fardami Layin Sada Fari	30"""

# Parse community mapping data
COMMUNITY_DF = pd.read_csv(StringIO(COMMUNITY_MAPPING_DATA), sep='\t')
COMMUNITY_DF.columns = COMMUNITY_DF.columns.str.strip()

# Create mapping dictionaries
COMMUNITY_CODE_TO_NAME = dict(zip(COMMUNITY_DF['community_name'].astype(str), COMMUNITY_DF['Q4. Community Name']))
COMMUNITY_NAME_TO_CODE = dict(zip(COMMUNITY_DF['Q4. Community Name'], COMMUNITY_DF['community_name'].astype(str)))
COMMUNITY_PLANNED_HH = dict(zip(COMMUNITY_DF['community_name'].astype(str), COMMUNITY_DF['Planned HH']))

# ---------------- CUSTOM CSS STYLING ----------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main Header with Logo Style */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #0077B5 0%, #00A0DC 100%);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 119, 181, 0.3);
        letter-spacing: -0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #0077B5 0%, #00A0DC 100%);
        padding: 1.8rem 1rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.15);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 140px;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.95;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.3;
    }
    
    /* Premium Color Schemes */
    .card-green { 
        background: linear-gradient(135deg, #057642 0%, #0A8D4E 100%);
    }
    .card-blue { 
        background: linear-gradient(135deg, #0077B5 0%, #00A0DC 100%);
    }
    .card-orange { 
        background: linear-gradient(135deg, #E37B40 0%, #F29C50 100%);
    }
    .card-purple { 
        background: linear-gradient(135deg, #5E5CE6 0%, #7E7CE8 100%);
    }
    .card-red { 
        background: linear-gradient(135deg, #CC1016 0%, #E33238 100%);
    }
    .card-teal {
        background: linear-gradient(135deg, #00827C 0%, #00A49A 100%);
    }
    .card-indigo {
        background: linear-gradient(135deg, #4A5FBF 0%, #5A73D8 100%);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A5F;
        margin: 2.5rem 0 1.5rem 0;
        padding: 1rem 1.5rem;
        background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 15px;
        border-left: 6px solid #0077B5;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        letter-spacing: -0.3px;
    }
    
    /* Alert Boxes */
    .alert-box {
        padding: 1.2rem 1.5rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .alert-warning { 
        background: linear-gradient(135deg, #fff4e6 0%, #ffe8cc 100%);
        border-left: 5px solid #ff9800;
        color: #663c00;
    }
    .alert-danger { 
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 5px solid #f44336;
        color: #7f0000;
    }
    .alert-success { 
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 5px solid #4caf50;
        color: #1b5e20;
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #0077B5 0%, #00A0DC 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 119, 181, 0.3);
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 119, 181, 0.4);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Mobile-First Responsive Design */
    
    /* Tablets and small laptops (768px - 1024px) */
    @media (max-width: 1024px) {
        .main-header {
            font-size: 2.2rem;
            padding: 1.5rem 1rem;
        }
        .metric-card {
            padding: 1.5rem 0.8rem;
            min-height: 120px;
        }
        .metric-value {
            font-size: 2rem;
        }
        .metric-label {
            font-size: 0.75rem;
        }
        .section-header {
            font-size: 1.5rem;
            padding: 0.8rem 1rem;
        }
        .alert-box {
            padding: 1rem 1.2rem;
            font-size: 0.9rem;
        }
    }
    
    /* Mobile devices (max-width: 768px) */
    @media (max-width: 768px) {
        /* Make app container full width on mobile */
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
            max-width: 100%;
        }
        
        /* Header adjustments */
        .main-header {
            font-size: 1.6rem;
            padding: 1.2rem 0.8rem;
            margin-bottom: 1.5rem;
            border-radius: 12px;
        }
        
        /* Metric cards stack better on mobile */
        .metric-card {
            padding: 1.2rem 0.8rem;
            margin: 0.5rem 0;
            min-height: 100px;
            border-radius: 12px;
        }
        
        .metric-value {
            font-size: 1.8rem;
            margin-bottom: 0.3rem;
        }
        
        .metric-label {
            font-size: 0.7rem;
            line-height: 1.2;
        }
        
        /* Section headers */
        .section-header {
            font-size: 1.2rem;
            padding: 0.8rem 1rem;
            margin: 1.5rem 0 1rem 0;
            border-radius: 10px;
        }
        
        /* Alert boxes */
        .alert-box {
            padding: 0.8rem 1rem;
            font-size: 0.85rem;
            border-radius: 10px;
        }
        
        /* Buttons */
        .stButton > button {
            padding: 0.6rem 1.5rem;
            font-size: 0.9rem;
            border-radius: 10px;
        }
        
        /* Make tables scrollable on mobile */
        .dataframe {
            font-size: 0.75rem;
            overflow-x: auto;
        }
        
        /* Adjust sidebar on mobile */
        section[data-testid="stSidebar"] {
            width: 280px;
        }
        
        /* Make columns stack on mobile */
        .row-widget.stHorizontal {
            flex-direction: column;
        }
    }
    
    /* Small mobile devices (max-width: 480px) */
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.4rem;
            padding: 1rem 0.5rem;
        }
        
        .metric-card {
            padding: 1rem 0.5rem;
            min-height: 90px;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .metric-label {
            font-size: 0.65rem;
        }
        
        .section-header {
            font-size: 1.1rem;
            padding: 0.7rem 0.8rem;
        }
        
        .alert-box {
            padding: 0.7rem 0.8rem;
            font-size: 0.8rem;
        }
        
        .stButton > button {
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
        }
        
        /* Reduce padding on very small screens */
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
    }
    
    /* Landscape mode optimization for mobile */
    @media (max-width: 896px) and (orientation: landscape) {
        .main-header {
            font-size: 1.5rem;
            padding: 0.8rem 1rem;
            margin-bottom: 1rem;
        }
        
        .metric-card {
            min-height: 80px;
            padding: 0.8rem 0.5rem;
        }
        
        .section-header {
            font-size: 1.1rem;
            margin: 1rem 0 0.8rem 0;
        }
    }
    
    /* Touch-friendly improvements for mobile */
    @media (hover: none) and (pointer: coarse) {
        /* Make buttons and interactive elements larger for touch */
        .stButton > button {
            min-height: 44px;
            padding: 0.8rem 1.5rem;
        }
        
        /* Increase tap targets */
        select, input, textarea {
            min-height: 44px;
            font-size: 16px; /* Prevents zoom on iOS */
        }
        
        /* Remove hover effects on touch devices */
        .metric-card:hover {
            transform: none;
        }
        
        .stButton > button:hover {
            transform: none;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------- DATA LOADING ----------------
@st.cache_data(show_spinner="📊 Loading data from KoboToolbox...", ttl=600)
def load_data_from_kobo():
    """Load all sheets from KoboToolbox API and return as dictionary"""
    try:
        # Check if URL is configured
        if "YOUR_ASSET_ID" in KOBO_DATA_URL or "myurl_here" in KOBO_DATA_URL or "my url here" in KOBO_DATA_URL:
            st.warning("⚠️ KoboToolbox URL is not configured. Please update the KOBO_DATA_URL variable in the code.")
            return {
                'main': pd.DataFrame(),
                'child_info': pd.DataFrame(),
                'child_infoo': pd.DataFrame(),
                'net_repeat': pd.DataFrame()
            }
        
        response = requests.get(KOBO_DATA_URL, timeout=60)
        response.raise_for_status()
        excel_file = BytesIO(response.content)
        
        # Read all sheets
        sheets_dict = {}
        try:
            # Read main sheet (Coverage Evaluation Survey)
            sheets_dict['main'] = pd.read_excel(excel_file, sheet_name=0)
            
            # Try to read other sheets
            try:
                sheets_dict['child_info'] = pd.read_excel(excel_file, sheet_name='child_info')
            except Exception:
                sheets_dict['child_info'] = pd.DataFrame()
            
            try:
                sheets_dict['child_infoo'] = pd.read_excel(excel_file, sheet_name='child_infoo')
            except Exception:
                sheets_dict['child_infoo'] = pd.DataFrame()
            
            try:
                sheets_dict['net_repeat'] = pd.read_excel(excel_file, sheet_name='net_repeat')
            except Exception:
                sheets_dict['net_repeat'] = pd.DataFrame()
                
        except Exception as e:
            st.warning(f"⚠️ Could not read all sheets: {e}. Loading main sheet only.")
            sheets_dict = {
                'main': pd.read_excel(excel_file),
                'child_info': pd.DataFrame(),
                'child_infoo': pd.DataFrame(),
                'net_repeat': pd.DataFrame()
            }
        
        return sheets_dict
    
    except Exception as e:
        st.error(f"❌ Error loading data from KoboToolbox: {e}")
        st.info("Please check that your KOBO_DATA_URL is correct and accessible.")
        return {
            'main': pd.DataFrame(),
            'child_info': pd.DataFrame(),
            'child_infoo': pd.DataFrame(),
            'net_repeat': pd.DataFrame()
        }


def preprocess_data(sheets_dict):
    """Preprocess and map column names for all sheets"""
    if not sheets_dict or sheets_dict['main'].empty:
        return sheets_dict
    
    # Process main sheet
    df_main = sheets_dict['main'].copy()
    
    # Clean LGA, Ward, and Community columns - remove ALL trailing non-alphanumeric characters
    text_cols_to_clean = [
        'Q2. Local Government Area', 'lga', 'LGA', 'lgas',
        'Q3.Ward', 'Q3. Ward', 'ward', 'Ward', 'wards',
        'Q4. Community Name', 'community', 'Community', 'Community Name'
    ]
    for col in text_cols_to_clean:
        if col in df_main.columns:
            # Remove the � character and other problematic characters
            df_main[col] = df_main[col].astype(str).str.replace('�', '', regex=False)
            # Remove any trailing whitespace and non-printable characters
            df_main[col] = df_main[col].str.strip()
            # Remove any remaining non-alphanumeric characters from the end (except spaces in the middle)
            df_main[col] = df_main[col].str.replace(r'[^\w\s]+$', '', regex=True)
            df_main[col] = df_main[col].str.strip()
    
    # Map community codes to names - Q4. Community Name contains codes, we need to map them to actual names
    if 'Q4. Community Name' in df_main.columns:
        # Create a new column with actual community names
        df_main['Community Name'] = df_main['Q4. Community Name'].astype(str).map(COMMUNITY_CODE_TO_NAME)
        # Fill any NaN values with the original code if mapping fails
        df_main['Community Name'].fillna(df_main['Q4. Community Name'], inplace=True)
    
    # Convert date columns in main sheet
    date_cols = ['Q8. Date', '_submission_time', 'start', 'end']
    for col in date_cols:
        if col in df_main.columns:
            df_main[col] = pd.to_datetime(df_main[col], errors='coerce')
    
    # Process child_info sheet
    if not sheets_dict['child_info'].empty:
        df_child_info = sheets_dict['child_info'].copy()
        # Convert age to numeric
        if 'Age of child ${child_id} as at when MDA was done (19th to 25th July 2025)' in df_child_info.columns:
            df_child_info['age_months'] = pd.to_numeric(
                df_child_info['Age of child ${child_id} as at when MDA was done (19th to 25th July 2025)'], 
                errors='coerce'
            )
        sheets_dict['child_info'] = df_child_info
    
    # Process child_infoo sheet (children <5 years)
    if not sheets_dict['child_infoo'].empty:
        df_child_infoo = sheets_dict['child_infoo'].copy()
        # Convert age column
        age_col = 'Q88. Child name and age ${child_idd} as at when MDA was done (19th to 25th July 2025)'
        if age_col in df_child_infoo.columns:
            df_child_infoo['age_months'] = pd.to_numeric(df_child_infoo[age_col], errors='coerce')
        sheets_dict['child_infoo'] = df_child_infoo
    
    # Process net_repeat sheet
    if not sheets_dict['net_repeat'].empty:
        df_net = sheets_dict['net_repeat'].copy()
        # Convert months column to numeric
        months_col = 'Q81. Net ${net_id} :How many months ago did your household get the mosquito net?'
        if months_col in df_net.columns:
            df_net['months_since_net'] = pd.to_numeric(df_net[months_col], errors='coerce')
        sheets_dict['net_repeat'] = df_net
    
    sheets_dict['main'] = df_main
    return sheets_dict


# ---------------- HELPER FUNCTION FOR FLEXIBLE COLUMN MATCHING ----------------
def find_column(df, possible_names):
    """Find the first matching column from a list of possible names"""
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def format_display_text(text):
    """Format text for proper display - capitalize properly"""
    if pd.isna(text):
        return text
    text = str(text)
    # Convert to title case for better display
    return text.title()


# ---------------- METRICS CALCULATION ----------------
def calculate_metrics(df):
    """Calculate key metrics from the dataset"""
    metrics = {
        'total_submissions': len(df),
        'total_lgas': 0,
        'total_wards': 0,
        'total_communities': 0,
        'total_enumerators': 0,
        'approved': 0,
        'pending': 0,
        'rejected': 0,
        'total_eligible': 0,
    }
    
    if df.empty:
        return metrics
    
    # Flexible column name matching for LGA (case-insensitive)
    lga_cols = ['lgas', 'lga', 'Q2. Local Government Area', 'LGA', 'Local Government Area', 'Lgas']
    for col in lga_cols:
        if col in df.columns:
            metrics['total_lgas'] = df[col].nunique()
            break
    
    # Flexible column name matching for Ward (case-insensitive)
    ward_cols = ['wards', 'ward', 'Q3.Ward', 'Q3. Ward', 'Ward', 'Wards']
    for col in ward_cols:
        if col in df.columns:
            metrics['total_wards'] = df[col].nunique()
            break
    
    # Flexible column name matching for Community
    community_cols = ['Community Name', 'Q4. Community Name', 'community', 'Community']
    for col in community_cols:
        if col in df.columns:
            metrics['total_communities'] = df[col].nunique()
            break
    
    # Flexible column name matching for Enumerator - ADDED username
    enum_cols = ['username', 'Enumerator id', 'Type in your Name', 'enumerator', 'Enumerator']
    for col in enum_cols:
        if col in df.columns:
            metrics['total_enumerators'] = df[col].nunique()
            break
    
    if '_validation_status' in df.columns:
        status_counts = df['_validation_status'].value_counts()
        metrics['approved'] = status_counts.get('Approved', 0)
        metrics['pending'] = status_counts.get('Not Validated', 0) + status_counts.get('On Hold', 0)
        metrics['rejected'] = status_counts.get('Rejected', 0)
    
    if 'total_eligible' in df.columns:
        metrics['total_eligible'] = int(df['total_eligible'].sum())
    
    return metrics


def identify_data_quality_issues(df):
    """Identify data quality issues"""
    issues = []
    
    if df.empty:
        return issues
    
    # Check for missing values in key columns
    key_cols = ['Q2. Local Government Area', 'Q4. Community Name', 'Q8. Date', 'Enumerator id']
    for col in key_cols:
        if col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                issues.append({
                    'type': 'warning',
                    'message': f"Missing values in {col}: {missing} records ({missing/len(df)*100:.1f}%)"
                })
    
    # Check for duplicates
    if '_uuid' in df.columns:
        duplicates = df['_uuid'].duplicated().sum()
        if duplicates > 0:
            issues.append({
                'type': 'danger',
                'message': f"Potential duplicate submissions: {duplicates} records"
            })
    
    # Check for rejected submissions
    if '_validation_status' in df.columns:
        rejected = (df['_validation_status'] == 'Rejected').sum()
        if rejected > 0:
            issues.append({
                'type': 'danger',
                'message': f"Rejected submissions: {rejected} records need review"
            })
    
    return issues


# ---------------- COMMUNITY COVERAGE ANALYSIS ----------------
def create_community_coverage_table(df):
    """Create community coverage analysis comparing planned vs actual"""
    if df.empty:
        return None
    
    # Get actual submissions by community code
    if 'Community_Code_Original' in df.columns:
        actual_submissions = df.groupby('Community_Code_Original').size().reset_index(name='Actual_HH')
        actual_submissions['Community_Code_Original'] = actual_submissions['Community_Code_Original'].astype(str)
        
        # Merge with planned data
        coverage = COMMUNITY_DF.copy()
        coverage['community_name'] = coverage['community_name'].astype(str)
        
        coverage = coverage.merge(
            actual_submissions,
            left_on='community_name',
            right_on='Community_Code_Original',
            how='left'
        )
        
        coverage['Actual_HH'] = coverage['Actual_HH'].fillna(0).astype(int)
        coverage['Coverage_%'] = ((coverage['Actual_HH'] / coverage['Planned HH']) * 100).round(1)
        coverage['Status'] = coverage.apply(
            lambda row: '✅ Complete' if row['Actual_HH'] >= row['Planned HH'] 
            else '⚠️ Partial' if row['Actual_HH'] > 0 
            else '❌ Not Started', axis=1
        )
        
        return coverage
    
    return None


# ---------------- VISUALIZATION FUNCTIONS ----------------
def render_metric_card(label, value, card_class=""):
    return f"""
    <div class="metric-card {card_class}">
        <div class="metric-value">{value:,}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def create_lga_distribution_chart(df):
    if df.empty:
        return None
    
    # Flexible column name matching for LGA (including plural)
    lga_col = None
    lga_cols = ['lgas', 'lga', 'Q2. Local Government Area', 'LGA', 'Local Government Area', 'Lgas']
    for col in lga_cols:
        if col in df.columns:
            lga_col = col
            break
    
    if lga_col is None:
        return None
    
    lga_counts = df[lga_col].value_counts().reset_index()
    lga_counts.columns = ['LGA', 'Submissions']
    
    # Format LGA names to proper case
    lga_counts['LGA'] = lga_counts['LGA'].apply(format_display_text)
    
    fig = px.bar(
        lga_counts, x='LGA', y='Submissions',
        title='Submissions by Local Government Area',
        color='Submissions', color_continuous_scale='Blues'
    )
    fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=400)
    return fig


def create_validation_status_chart(df):
    if df.empty or '_validation_status' not in df.columns:
        return None
    
    status_counts = df['_validation_status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    color_map = {
        'Approved': '#28a745',
        'Not Validated': '#ffc107',
        'On Hold': '#fd7e14',
        'Rejected': '#dc3545'
    }
    
    fig = px.pie(
        status_counts, values='Count', names='Status',
        title='Validation Status Distribution',
        color='Status', color_discrete_map=color_map
    )
    fig.update_layout(height=400)
    return fig


def create_ward_distribution_chart(df):
    if df.empty:
        return None
    
    # Flexible column name matching for Ward (including plural)
    ward_col = None
    ward_cols = ['wards', 'ward', 'Q3.Ward', 'Q3. Ward', 'Ward', 'Wards']
    for col in ward_cols:
        if col in df.columns:
            ward_col = col
            break
    
    if ward_col is None:
        return None
    
    ward_counts = df[ward_col].value_counts().head(15).reset_index()
    ward_counts.columns = ['Ward', 'Submissions']
    
    # Format Ward names to proper case
    ward_counts['Ward'] = ward_counts['Ward'].apply(format_display_text)
    
    fig = px.bar(
        ward_counts, x='Ward', y='Submissions',
        title='Top 15 Wards by Submissions',
        color='Submissions', color_continuous_scale='Greens'
    )
    fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=400)
    return fig


def create_timeline_chart(df):
    if df.empty:
        return None
    
    # Flexible column name matching for date
    date_col = None
    date_cols = ['Q8. Date', '_submission_time', 'start', 'Date', 'date', 'submission_time']
    for col in date_cols:
        if col in df.columns:
            date_col = col
            break
    
    if date_col is None:
        return None
    
    df_timeline = df.copy()
    df_timeline[date_col] = pd.to_datetime(df_timeline[date_col], errors='coerce')
    df_timeline = df_timeline.dropna(subset=[date_col])
    
    if len(df_timeline) == 0:
        return None
    
    daily_counts = df_timeline.groupby(df_timeline[date_col].dt.date).size().reset_index()
    daily_counts.columns = ['Date', 'Submissions']
    
    fig = px.line(
        daily_counts, x='Date', y='Submissions',
        title='Data Collection Timeline', markers=True
    )
    fig.update_traces(line_color='#0077B5')
    fig.update_layout(height=400)
    return fig


# ---------------- QC CHECKS FUNCTION ----------------
def perform_qc_checks(df, child_df=None):
    """
    Perform comprehensive quality control checks on the dataset
    Returns a DataFrame with flagged issues by LGA, Ward, and Community
    """
    qc_issues = []
    
    if df.empty:
        return pd.DataFrame(qc_issues)
    
    # Find column names flexibly
    lga_col = find_column(df, ['lgas', 'lga', 'Q2. Local Government Area', 'LGA'])
    ward_col = find_column(df, ['wards', 'ward', 'Q3.Ward', 'Q3. Ward', 'Ward'])
    community_col = find_column(df, ['Community Name', 'Q4. Community Name', 'community'])
    uuid_col = find_column(df, ['_uuid', 'uuid'])
    unique_code_col = find_column(df, ['unique_code', 'unique_code_1', 'household_code'])
    validation_status_col = find_column(df, ['_validation_status', 'validation_status', 'Validation Status'])
    
    # Create lookup dictionary for child records to get parent HH info
    parent_lookup = {}
    if uuid_col:
        for idx, row in df.iterrows():
            parent_lookup[row[uuid_col]] = {
                'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                'Unique HH ID': row.get(unique_code_col, 'N/A') if unique_code_col else 'N/A',
                'Validation Status': row.get(validation_status_col, 'N/A') if validation_status_col else 'N/A'
            }
    
    # QC Check 1: Q22 > Q13 (Years living > Age of HH Head)
    q22_col = find_column(df, ['Q22. How long have you been living continuously in ${community_confirm}', 
                                'Q22', 'years_living', 'residence_duration'])
    q13_col = find_column(df, [
        'Q13. Age of Head of the Household',
        'Q13',
        'hh_head_age',
        'age_head'
    ])
    
    if q22_col and q13_col:
        age_issue = df[pd.to_numeric(df[q22_col], errors='coerce') > pd.to_numeric(df[q13_col], errors='coerce')]
        for idx, row in age_issue.iterrows():
            qc_issues.append({
                'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                'Unique HH ID': row.get(unique_code_col, 'N/A') if unique_code_col else 'N/A',
                'Validation Status': row.get(validation_status_col, 'N/A') if validation_status_col else 'N/A',
                'Issue Type': 'Age Inconsistencies',
                'Description': f'Years of Living ({row.get(q22_col, "N/A")}) > HH Head Age ({row.get(q13_col, "N/A")})',
                'Row Index': idx
            })
    
    # QC Check 2: Education vs Occupation mismatch
    education_col = find_column(df, ['Q20. Highest education level completed', 'Q20', 'education', 'education_level'])
    occupation_col = find_column(df, ['Occupation', 'occupation', 'Q21. Occupation'])
    
    if education_col and occupation_col:
        edu_occ_issue = df[
            (df[education_col].astype(str).str.contains('No Formal Education', case=False, na=False)) &
            (df[occupation_col].astype(str).str.contains('Professional|technical|managerial', case=False, na=False))
        ]
        for idx, row in edu_occ_issue.iterrows():
            qc_issues.append({
                'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                'Unique HH ID': row.get(unique_code_col, 'N/A') if unique_code_col else 'N/A',
                'Validation Status': row.get(validation_status_col, 'N/A') if validation_status_col else 'N/A',
                'Issue Type': 'Education-Occupation Mismatch',
                'Description': 'No formal education but professional occupation',
                'Row Index': idx
            })
    
    # QC Check 3: Negative total children in household
    children_cols = [col for col in df.columns if 'child' in col.lower() and 'total' in col.lower()]
    for child_col in children_cols:
        negative_children = df[pd.to_numeric(df[child_col], errors='coerce') < 0]
        for idx, row in negative_children.iterrows():
            qc_issues.append({
                'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                'Unique HH ID': row.get(unique_code_col, 'N/A') if unique_code_col else 'N/A',
                'Validation Status': row.get(validation_status_col, 'N/A') if validation_status_col else 'N/A',
                'Issue Type': 'Negative Children Count',
                'Description': f'Negative value in {child_col}: {row.get(child_col, "N/A")}',
                'Row Index': idx
            })
    
    # QC Check 4: Households without eligible children
    eligible_child_cols = [col for col in df.columns if 'eligible' in col.lower() and 'child' in col.lower()]
    for elig_col in eligible_child_cols:
        no_eligible = df[pd.to_numeric(df[elig_col], errors='coerce') == 0]
        for idx, row in no_eligible.iterrows():
            qc_issues.append({
                'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                'Unique HH ID': row.get(unique_code_col, 'N/A') if unique_code_col else 'N/A',
                'Validation Status': row.get(validation_status_col, 'N/A') if validation_status_col else 'N/A',
                'Issue Type': 'No Eligible Children',
                'Description': 'Household has 0 eligible children',
                'Row Index': idx
            })
    
    # QC Check 5: Check child_infoo sheet if provided (children 1-59 months)
    if child_df is not None and not child_df.empty:
        # Find child sheet columns
        age_col = find_column(child_df, [
            'Q88. Child name and age ${child_idd} as at when MDA was done (19th to 25th July 2025)',
            'age_months',
            'child_age'
        ])
        q94_col = find_column(child_df, [
            'Q94. Did child ${child_idd} swallow the AZM offered?',
            'Q94',
            'child_swallow_azm'
        ])
        q95_col = find_column(child_df, [
            'Q95. Did child ${child_idd} swallow the AZM in the presence of the person who offered it?',
            'Q95',
            'swallow_in_presence'
        ])
        q102_col = find_column(df, [
            'Q102. About how many minutes did the CDD spend in your household?',
            'Q102',
            'cdd_time_minutes'
        ])
        
        # Check Q94 (child swallowed AZM) AND child age >59 months
        if age_col and q94_col:
            swallowed_over_59 = child_df[
                (pd.to_numeric(child_df[age_col], errors='coerce') > 59) &
                (child_df[q94_col].astype(str).str.contains('Yes', case=False, na=False))
            ]
            for idx, row in swallowed_over_59.iterrows():
                submission_uuid = row.get('_submission__uuid', 'N/A')
                parent_info = parent_lookup.get(submission_uuid, {'LGA': 'N/A', 'Ward': 'N/A', 'Community': 'N/A'})
                qc_issues.append({
                    'LGA': parent_info['LGA'],
                    'Ward': parent_info['Ward'],
                    'Community': parent_info['Community'],
                    'Unique HH ID': parent_info.get('Unique HH ID', 'N/A'),
                    'Validation Status': parent_info.get('Validation Status', 'N/A'),
                    'Issue Type': 'Q94 Yes & Child Age >59 months',
                    'Description': f'Child {row.get("child_idd", "N/A")} aged {row.get(age_col, "N/A")} months (>59) swallowed AZM (unique_code2: {row.get("unique_code2", "N/A")})',
                    'Row Index': idx
                })
        
        # Check Q95 (swallowed in presence) AND Q102 = 0 minutes
        if q95_col and q102_col:
            for idx_child, child_row in child_df.iterrows():
                submission_uuid = child_row.get('_submission__uuid', 'N/A')
                # Find matching parent record
                if uuid_col and submission_uuid != 'N/A':
                    parent_row = df[df[uuid_col] == submission_uuid]
                    if not parent_row.empty:
                        q102_val = pd.to_numeric(parent_row.iloc[0].get(q102_col, -1), errors='coerce')
                        q95_val = str(child_row.get(q95_col, '')).strip()
                        
                        if 'yes' in q95_val.lower() and q102_val == 0:
                            parent_info = parent_lookup.get(submission_uuid, {'LGA': 'N/A', 'Ward': 'N/A', 'Community': 'N/A'})
                            qc_issues.append({
                                'LGA': parent_info['LGA'],
                                'Ward': parent_info['Ward'],
                                'Community': parent_info['Community'],
                                'Unique HH ID': parent_info.get('Unique HH ID', 'N/A'),
                                'Validation Status': parent_info.get('Validation Status', 'N/A'),
                                'Issue Type': 'Q95 Yes & Q102 = 0 minutes',
                                'Description': f'Child {child_row.get("child_idd", "N/A")} swallowed in presence but CDD time = 0 min (unique_code2: {child_row.get("unique_code2", "N/A")})',
                                'Row Index': idx_child
                            })
        
        # Check Q95 (swallowed in presence) AND Q102 >= 100 minutes
        if q95_col and q102_col:
            for idx_child, child_row in child_df.iterrows():
                submission_uuid = child_row.get('_submission__uuid', 'N/A')
                # Find matching parent record
                if uuid_col and submission_uuid != 'N/A':
                    parent_row = df[df[uuid_col] == submission_uuid]
                    if not parent_row.empty:
                        q102_val = pd.to_numeric(parent_row.iloc[0].get(q102_col, -1), errors='coerce')
                        q95_val = str(child_row.get(q95_col, '')).strip()
                        
                        if 'yes' in q95_val.lower() and q102_val >= 100:
                            parent_info = parent_lookup.get(submission_uuid, {'LGA': 'N/A', 'Ward': 'N/A', 'Community': 'N/A'})
                            qc_issues.append({
                                'LGA': parent_info['LGA'],
                                'Ward': parent_info['Ward'],
                                'Community': parent_info['Community'],
                                'Unique HH ID': parent_info.get('Unique HH ID', 'N/A'),
                                'Validation Status': parent_info.get('Validation Status', 'N/A'),
                                'Issue Type': 'Q95 Yes & Q102 >= 100 minutes',
                                'Description': f'Child {child_row.get("child_idd", "N/A")} swallowed in presence but CDD time = {q102_val} min (>=100) (unique_code2: {child_row.get("unique_code2", "N/A")})',
                                'Row Index': idx_child
                            })
        
        # Check for duplicate unique_code2 (child duplicate)
        unique_code2_col = find_column(child_df, ['unique_code2', 'unique_code_2', 'child_unique_code'])
        if unique_code2_col:
            duplicates = child_df[child_df.duplicated(subset=[unique_code2_col], keep=False)]
            for idx, row in duplicates.iterrows():
                submission_uuid = row.get('_submission__uuid', 'N/A')
                parent_info = parent_lookup.get(submission_uuid, {'LGA': 'N/A', 'Ward': 'N/A', 'Community': 'N/A'})
                qc_issues.append({
                    'LGA': parent_info['LGA'],
                    'Ward': parent_info['Ward'],
                    'Community': parent_info['Community'],
                    'Unique HH ID': parent_info.get('Unique HH ID', 'N/A'),
                    'Validation Status': parent_info.get('Validation Status', 'N/A'),
                    'Issue Type': 'Child Duplicate (unique_code2)',
                    'Description': f'Duplicate unique_code2: {row.get(unique_code2_col, "N/A")}',
                    'Row Index': idx
                })
    
    # QC Check 6: Duplicate unique_code (HH Duplicate)
    if unique_code_col:
        duplicates = df[df.duplicated(subset=[unique_code_col], keep=False)]
        for idx, row in duplicates.iterrows():
            qc_issues.append({
                'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                'Unique HH ID': row.get(unique_code_col, 'N/A') if unique_code_col else 'N/A',
                'Validation Status': row.get(validation_status_col, 'N/A') if validation_status_col else 'N/A',
                'Issue Type': 'HH Duplicate (unique_code)',
                'Description': f'Duplicate unique_code: {row.get(unique_code_col, "N/A")}',
                'Row Index': idx
            })
    
    # QC Check 7: Urban settlement without basic amenities (batch check by enumerator)
    settlement_col = find_column(df, ['Q5. Type of Settlement', 'Q5', 'settlement_type', 'settlement'])
    enumerator_col = find_column(df, ['username', 'Type in your Name', 'Enumerator', 'enumerator_name'])
    amenity_cols = ['Q23. Electricity', 'Q24. Radio', 'Q25. Television', 'Q26. A non-mobile telephone',
                    'Q27. Computer', 'Q28. Refrigerator', 'Q29. Chair', 'Q30. Bed', 'Q31. Sofa',
                    'Q32. Cupboard', 'Q33. Animal-drawn cart (donkey, horse, camel)', 'Q34. Bicycle',
                    'Q35. Motorcycle or motor scooter', 'Q36. Car or truck', 'Q37. Boat with motor',
                    'Q38. Canoe', 'Q39. Keke Napep', 'Q40. Fan', 'Q41. Watch', 'Q42. Mobile telephone',
                    'Q43. Table', 'Q44. Electric Iron', 'Q45. Bank account', 'Q46. Air condition', 'Q47. Generator']
    
    if settlement_col and enumerator_col:
        # Get existing amenity columns
        existing_amenities = [col for col in amenity_cols if col in df.columns]
        
        if existing_amenities:
            # Filter urban households only
            urban_df = df[df[settlement_col].astype(str).str.contains('Urban', case=False, na=False)].copy()
            
            if not urban_df.empty:
                # Group by enumerator
                for enumerator, group in urban_df.groupby(enumerator_col):
                    if len(group) >= 1:  # At least 1 record
                        # Check if ALL records by this enumerator have ALL amenities as "No"
                        all_records_no_amenities = True
                        
                        for idx, row in group.iterrows():
                            # Check if this row has all amenities as "No"
                            row_all_no = True
                            for amenity in existing_amenities:
                                val = str(row.get(amenity, '')).strip().lower()
                                if val not in ['no', '']:
                                    row_all_no = False
                                    break
                            
                            # If even one row has some amenities, the enumerator is OK
                            if not row_all_no:
                                all_records_no_amenities = False
                                break
                        
                        # Flag if ALL records by this enumerator have no amenities
                        if all_records_no_amenities:
                            # Flag all records from this enumerator
                            for idx, row in group.iterrows():
                                qc_issues.append({
                                    'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                                    'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                                    'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                                    'Unique HH ID': row.get(unique_code_col, 'N/A') if unique_code_col else 'N/A',
                                    'Validation Status': row.get(validation_status_col, 'N/A') if validation_status_col else 'N/A',
                                    'Issue Type': 'Urban HH No Amenities (Enumerator Pattern)',
                                    'Description': f'Enumerator "{enumerator}" - ALL {len(group)} urban records have NO amenities',
                                    'Row Index': idx
                                })
    
    # Convert to DataFrame
    qc_df = pd.DataFrame(qc_issues)
    
    # Format display text
    if not qc_df.empty and 'LGA' in qc_df.columns:
        qc_df['LGA'] = qc_df['LGA'].apply(format_display_text)
    if not qc_df.empty and 'Ward' in qc_df.columns:
        qc_df['Ward'] = qc_df['Ward'].apply(format_display_text)
    
    return qc_df


# ---------------- LOGIN FUNCTIONS ----------------
def check_login(username):
    username_lower = username.lower().strip()
    
    if username_lower == ADMIN_USERNAME.lower():
        return 'admin', None
    
    if username_lower in LGA_CREDENTIALS:
        lga_name = LGA_CREDENTIALS[username_lower]
        return 'lga', lga_name
    
    return None, None


def login_page():
    """Display login interface"""
    st.markdown("""
    <div style='text-align: center; margin-top: 3rem; margin-bottom: 2rem;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🔐</div>
        <h1 style='color: #0077B5; font-weight: 800; font-size: 2.5rem; margin-bottom: 0.5rem;'>
            SARMAAN II Coverage Dashboard
        </h1>
        <p style='color: #666; font-size: 1.1rem; font-weight: 500;'>
            Katsina State - Secure Data Analytics Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Collapsible Login hint - outside the form
        with st.expander("🔑 Click here to view available usernames", expanded=False):
            st.markdown("""
            **Admin Access:**
            - Username: `Admin`
            
            **LGA Users (use lowercase):**
            - `ingawa`, `kankara`, `kankia`, `mani`, `musawa`, `rimi`
            
            """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<p style='text-align: center; color: #666; margin-bottom: 1.5rem;'>Enter your username to continue</p>", unsafe_allow_html=True)
            
            username = st.text_input("👤 Username", placeholder="Enter your username (e.g., Admin or kware)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 Login to Dashboard", use_container_width=True)
            
            if submit:
                if not username:
                    st.error("⚠️ Please enter your username")
                else:
                    access_level, lga_filter = check_login(username)
                    if access_level:
                        st.session_state['logged_in'] = True
                        st.session_state['access_level'] = access_level
                        st.session_state['lga_filter'] = lga_filter
                        st.session_state['username'] = username
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username. Please try again.")


# ---------------- MAIN DASHBOARD ----------------
def run_dashboard():
    """Main dashboard interface"""
    
    # Enhanced Header
    st.markdown("""
    <div class="main-header">
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'></div>
        SARMAAN II Coverage Evaluation
        <div style='font-size: 1.2rem; font-weight: 500; opacity: 0.9; margin-top: 0.5rem; letter-spacing: 2px;'>
            DATA ANALYTICS DASHBOARD
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data first - now returns dictionary of sheets
    sheets_dict = load_data_from_kobo()
    
    if sheets_dict and not sheets_dict['main'].empty:
        sheets_dict = preprocess_data(sheets_dict)
    
    # Extract main sheet for compatibility with existing code
    df = sheets_dict['main'] if sheets_dict else pd.DataFrame()
    
    # Sidebar with Filters
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1rem; 
                    background: rgba(255,255,255,0.1); border-radius: 15px;'>
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>👤</div>
            <div style='color: white; font-size: 1.1rem; font-weight: 600;'>
                User Information
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 1.5rem;'>
            <div style='margin-bottom: 1rem;'>
                <span style='color: #666; font-size: 0.85rem; text-transform: uppercase; 
                           letter-spacing: 1px;'>Username</span>
                <div style='color: #1E3A5F; font-weight: 600; font-size: 1.1rem;'>
                    {st.session_state.get('username', 'Unknown')}
                </div>
            </div>
            <div style='margin-bottom: 1rem;'>
                <span style='color: #666; font-size: 0.85rem; text-transform: uppercase; 
                           letter-spacing: 1px;'>Access Level</span>
                <div style='color: #0077B5; font-weight: 600; font-size: 1.1rem;'>
                    {st.session_state.get('access_level', 'Unknown').upper()}
                </div>
            </div>
            {f'''<div>
                <span style='color: #666; font-size: 0.85rem; text-transform: uppercase; 
                           letter-spacing: 1px;'>Assigned LGA</span>
                <div style='color: #057642; font-weight: 600; font-size: 1.1rem;'>
                    {st.session_state['lga_filter'].upper()}
                </div>
            </div>''' if st.session_state.get('lga_filter') else ''}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Data Filters Section
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; margin: 1.5rem 0;
                    background: rgba(255,255,255,0.1); border-radius: 15px;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🔍</div>
            <div style='color: white; font-size: 1.1rem; font-weight: 600;'>
                Data Filters
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize filtered_df
        filtered_df = df.copy() if df is not None and not df.empty else pd.DataFrame()
        
        # Find column names (including plural forms)
        lga_col = find_column(filtered_df, ['lgas', 'lga', 'Q2. Local Government Area', 'LGA', 'Local Government Area', 'Lgas'])
        ward_col = find_column(filtered_df, ['wards', 'ward', 'Q3.Ward', 'Q3. Ward', 'Ward', 'Wards'])
        community_col = find_column(filtered_df, ['Community Name', 'Q4. Community Name', 'community', 'Community'])
        status_col = find_column(filtered_df, ['_validation_status', 'validation_status', 'Validation Status'])
        date_col = find_column(filtered_df, ['Q8. Date', '_submission_time', 'start', 'Date', 'date', 'submission_time'])
        
        # Apply LGA filter for non-admin users (case-insensitive comparison)
        if st.session_state.get('access_level') == 'lga' and st.session_state.get('lga_filter') and lga_col:
            # Case-insensitive filtering
            lga_filter_value = st.session_state['lga_filter']
            
            # Debug: Show what we're looking for
            st.sidebar.info(f"🔍 Searching for LGA: **{lga_filter_value}**")
            
            # Show available LGAs in the dataset
            available_lgas = df[lga_col].dropna().unique().tolist()
            st.sidebar.info("📊 Available LGAs in dataset:\n" + "\n".join([f"- {lga}" for lga in sorted(available_lgas)]))
            
            # Perform case-insensitive filtering
            filtered_df = filtered_df[filtered_df[lga_col].astype(str).str.lower() == lga_filter_value.lower()]
            
            # Show results
            if filtered_df.empty:
                st.sidebar.error(f"❌ No data found for LGA: **{lga_filter_value}**")
                st.sidebar.warning("⚠️ Please ensure:\n1. Data has been uploaded\n2. LGA name matches exactly\n3. You're using the correct username")
            else:
                st.sidebar.success(f"✅ Found {len(filtered_df)} records for **{lga_filter_value}**")
        
        # LGA Filter (only for admin)
        if st.session_state.get('access_level') == 'admin' and not filtered_df.empty and lga_col:
            lga_options = ['All'] + sorted(filtered_df[lga_col].dropna().unique().tolist())
            lga_filter = st.selectbox("📍 Filter by LGA", options=lga_options, key='sidebar_lga')
            if lga_filter != 'All':
                filtered_df = filtered_df[filtered_df[lga_col] == lga_filter]
        
        # Ward Filter
        if not filtered_df.empty and ward_col:
            ward_options = ['All'] + sorted(filtered_df[ward_col].dropna().unique().tolist())
            ward_filter = st.selectbox("🏘️ Filter by Ward", options=ward_options, key='sidebar_ward')
            if ward_filter != 'All':
                filtered_df = filtered_df[filtered_df[ward_col] == ward_filter]
        
        # Community Filter
        if not filtered_df.empty and community_col:
            community_options = ['All'] + sorted(filtered_df[community_col].dropna().unique().tolist())
            community_filter = st.selectbox("🏠 Filter by Community", options=community_options, key='sidebar_community')
            if community_filter != 'All':
                filtered_df = filtered_df[filtered_df[community_col] == community_filter]
        
        # Validation Status Filter
        if not filtered_df.empty and status_col:
            status_options = ['All'] + sorted(filtered_df[status_col].dropna().unique().tolist())
            status_filter = st.selectbox("✅ Filter by Status", options=status_options, key='sidebar_status')
            if status_filter != 'All':
                filtered_df = filtered_df[filtered_df[status_col] == status_filter]
        
        # Date Range Filter
        if not filtered_df.empty and date_col:
            date_series = pd.to_datetime(filtered_df[date_col], errors='coerce')
            if date_series.notna().any():
                min_date = date_series.min().date()
                max_date = date_series.max().date()
                date_range = st.date_input(
                    "📅 Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key='sidebar_date'
                )
                if len(date_range) == 2:
                    mask = (date_series.dt.date >= date_range[0]) & (date_series.dt.date <= date_range[1])
                    filtered_df = filtered_df[mask]
    
    # Main content - Check if data is available
    if df is None or df.empty:
        st.warning("⚠️ No data available. The dashboard will display once data is loaded from KoboToolbox.")
        return
    
    # Debug: Show column names (remove this after debugging)
    with st.expander("🔍 Debug: View Available Columns", expanded=False):
        st.write(f"**Total columns:** {len(df.columns)}")
        st.write("**Column names:**")
        st.code("\n".join(df.columns.tolist()))
    
    # Calculate metrics
    metrics = calculate_metrics(filtered_df)
    
    # Display metrics
    st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(render_metric_card("Total Submissions", metrics['total_submissions'], "card-blue"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("LGAs Covered", metrics['total_lgas'], "card-green"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("Wards Covered", metrics['total_wards'], "card-teal"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_card("Communities", metrics['total_communities'], "card-orange"), unsafe_allow_html=True)
    with col5:
        st.markdown(render_metric_card("Enumerators", metrics['total_enumerators'], "card-indigo"), unsafe_allow_html=True)
    
    # Validation status row (always show, even with zero values)
    st.markdown('<div class="section-header">✅ Validation & Quality Control Status</div>', unsafe_allow_html=True)
    vcol1, vcol2, vcol3 = st.columns(3)
    with vcol1:
        st.markdown("""
        <div class="metric-card card-green" style="min-height: 100px; padding: 1.2rem 1rem;">
            <div style='font-size: 2rem; margin-bottom: 0.3rem;'>✓</div>
            <div class="metric-value" style="font-size: 2.2rem;">{:,}</div>
            <div class="metric-label" style="font-size: 0.8rem;">Approved Submissions</div>
        </div>
        """.format(metrics['approved']), unsafe_allow_html=True)
    with vcol2:
        st.markdown("""
        <div class="metric-card card-orange" style="min-height: 100px; padding: 1.2rem 1rem;">
            <div style='font-size: 2rem; margin-bottom: 0.3rem;'>⏳</div>
            <div class="metric-value" style="font-size: 2.2rem;">{:,}</div>
            <div class="metric-label" style="font-size: 0.8rem;">Awaiting Review</div>
        </div>
        """.format(metrics['pending']), unsafe_allow_html=True)
    with vcol3:
        st.markdown("""
        <div class="metric-card card-red" style="min-height: 100px; padding: 1.2rem 1rem;">
            <div style='font-size: 2rem; margin-bottom: 0.3rem;'>✗</div>
            <div class="metric-value" style="font-size: 2.2rem;">{:,}</div>
            <div class="metric-label" style="font-size: 0.8rem;">Not Approved</div>
        </div>
        """.format(metrics['rejected']), unsafe_allow_html=True)
    
    # Data Quality Alerts
    issues = identify_data_quality_issues(filtered_df)
    if issues:
        st.markdown('<div class="section-header">⚠️ Data Quality Insights & Alerts</div>', unsafe_allow_html=True)
        for issue in issues:
            alert_class = f"alert-{issue['type']}"
            icon = "⚠️" if issue['type'] == 'warning' else "❌"
            st.markdown(f'<div class="alert-box {alert_class}"><strong>{icon} {issue["message"]}</strong></div>', unsafe_allow_html=True)
    
    # Data Explorer - Advanced Table with Planned vs Reached HH (MOVED FIRST)
    st.markdown('<div class="section-header">📋 Coverage Summary: Planned vs Reached Households</div>', unsafe_allow_html=True)
    
    # Get community column
    q4_col = find_column(filtered_df, ['Q4. Community Name', 'community', 'community_name'])
    lga_col = find_column(filtered_df, ['Q2. Local Government Area', 'lga', 'LGA'])
    ward_col = find_column(filtered_df, ['Q3.Ward', 'Q3. Ward', 'ward', 'Ward'])
    
    if q4_col and not filtered_df.empty:
        # Group by LGA, Ward, Community and count households
        explorer_data = []
        
        for lga in filtered_df[lga_col].unique() if lga_col else ['N/A']:
            lga_df = filtered_df[filtered_df[lga_col] == lga] if lga_col else filtered_df
            
            for ward in lga_df[ward_col].unique() if ward_col else ['N/A']:
                ward_df = lga_df[lga_df[ward_col] == ward] if ward_col else lga_df
                
                for community_code in ward_df[q4_col].unique():
                    if pd.notna(community_code):
                        # Get community name from mapping
                        community_name = COMMUNITY_CODE_TO_NAME.get(str(community_code), str(community_code))
                        
                        # Get planned HH
                        planned_hh = COMMUNITY_PLANNED_HH.get(str(community_code), 0)
                        
                        # Count reached HH
                        reached_hh = len(ward_df[ward_df[q4_col] == community_code])
                        
                        # Calculate percentage
                        coverage_pct = (reached_hh / planned_hh * 100) if planned_hh > 0 else 0
                        
                        # Status
                        if reached_hh >= planned_hh:
                            status = "✅ Target Met"
                            status_color = "green"
                        elif reached_hh > 0:
                            status = "⚠️ In Progress"
                            status_color = "red"
                        else:
                            status = "❌ Not Started"
                            status_color = "red"
                        
                        explorer_data.append({
                            'LGA': lga,
                            'Ward': ward,
                            'Community': community_name,
                            'Planned HH': planned_hh,
                            'Reached HH': reached_hh,
                            'Coverage %': round(coverage_pct, 1),
                            'Status': status,
                            'Status_Color': status_color
                        })
        
        if explorer_data:
            explorer_df = pd.DataFrame(explorer_data)
            
            # Summary metrics
            exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)
            
            total_planned = explorer_df['Planned HH'].sum()
            total_reached = explorer_df['Reached HH'].sum()
            overall_coverage = (total_reached / total_planned * 100) if total_planned > 0 else 0
            communities_met_target = len(explorer_df[explorer_df['Status_Color'] == 'green'])
            
            with exp_col1:
                st.metric("Total Planned HH", f"{total_planned:,}")
            with exp_col2:
                st.metric("Total Reached HH", f"{total_reached:,}")
            with exp_col3:
                st.metric("Overall Coverage", f"{overall_coverage:.1f}%")
            with exp_col4:
                st.metric("Communities @ Target", f"{communities_met_target}/{len(explorer_df)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display table with color coding
            st.markdown("### 📝 Detailed Coverage Table")
            
            # Remove the Status_Color column for display
            display_explorer_df = explorer_df.drop(columns=['Status_Color'])
            
            # Apply styling using the original dataframe's Status_Color column
            st.dataframe(
                display_explorer_df.style.apply(
                    lambda row: ['background-color: #d1fae5'] * len(row) 
                    if explorer_df.loc[row.name, 'Status_Color'] == 'green' 
                    else ['background-color: #fee2e2'] * len(row), 
                    axis=1
                ),
                use_container_width=True,
                height=500,
                hide_index=True
            )
        else:
            st.info("📊 Data explorer will populate when community data is available")
    else:
        st.info("📊 Data explorer requires community column in the dataset")
    
    # Approval Section - QC Checks (NOW BELOW DATA EXPLORER)
    st.markdown('<div class="section-header">Quality Control Checks</div>', unsafe_allow_html=True)
    
    # Perform QC checks - pass main sheet and child_infoo sheet
    child_infoo_df = sheets_dict.get('child_infoo', pd.DataFrame()) if sheets_dict else pd.DataFrame()
    qc_results = perform_qc_checks(filtered_df, child_df=child_infoo_df)
    
    if not qc_results.empty:
        # Summary metrics
        qc_col1, qc_col2, qc_col3, qc_col4 = st.columns(4)
        
        with qc_col1:
            st.metric("Total Issues Found", len(qc_results), delta=None)
        with qc_col2:
            age_issues = len(qc_results[qc_results['Issue Type'] == 'Age Inconsistencies'])
            st.metric("Age Inconsistencies", age_issues)
        with qc_col3:
            duplicates = len(qc_results[qc_results['Issue Type'].str.contains('Duplicate', na=False)])
            st.metric("Duplicates", duplicates)
        with qc_col4:
            other_issues = len(qc_results[~qc_results['Issue Type'].isin(['Age Inconsistencies']) & 
                                          ~qc_results['Issue Type'].str.contains('Duplicate', na=False)])
            st.metric("Other Issues", other_issues)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Issue breakdown by type
        issue_counts = qc_results['Issue Type'].value_counts().reset_index()
        issue_counts.columns = ['Issue Type', 'Count']
        
        fig_qc = px.bar(
            issue_counts, 
            x='Issue Type', 
            y='Count',
            title='Distribution of QC Issues',
            color='Count',
            color_continuous_scale='Reds'
        )
        fig_qc.update_layout(xaxis_tickangle=-45, showlegend=False, height=400)
        st.plotly_chart(fig_qc, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Detailed QC table
        st.markdown("### 📝 Detailed QC Issues Table")
        st.write(f"**{len(qc_results):,}** issues flagged across LGA, Ward, and Community")
        
        # Add filtering options for QC results
        qc_filter_col1, qc_filter_col2 = st.columns(2)
        
        with qc_filter_col1:
            selected_issue_types = st.multiselect(
                "Filter by Issue Type",
                options=sorted(qc_results['Issue Type'].unique()),
                default=sorted(qc_results['Issue Type'].unique()),
                key="qc_issue_filter"
            )
        
        with qc_filter_col2:
            if 'LGA' in qc_results.columns:
                selected_lgas_qc = st.multiselect(
                    "Filter by LGA",
                    options=sorted(qc_results['LGA'].unique()),
                    default=sorted(qc_results['LGA'].unique()),
                    key="qc_lga_filter"
                )
            else:
                selected_lgas_qc = []
        
        # Filter QC results
        filtered_qc = qc_results.copy()
        if selected_issue_types:
            filtered_qc = filtered_qc[filtered_qc['Issue Type'].isin(selected_issue_types)]
        if selected_lgas_qc:
            filtered_qc = filtered_qc[filtered_qc['LGA'].isin(selected_lgas_qc)]
        
        # Remove Row Index column before displaying
        if 'Row Index' in filtered_qc.columns:
            filtered_qc = filtered_qc.drop(columns=['Row Index'])
        
        # Display filtered QC table
        st.dataframe(
            filtered_qc,
            use_container_width=True,
            height=500,
            column_config={
                "LGA": st.column_config.TextColumn("LGA", width="small"),
                "Ward": st.column_config.TextColumn("Ward", width="small"),
                "Community": st.column_config.TextColumn("Community", width="medium"),
                "Unique HH ID": st.column_config.TextColumn("Unique HH ID", width="medium"),
                "Validation Status": st.column_config.TextColumn("Validation Status", width="small"),
                "Issue Type": st.column_config.TextColumn("Issue Type", width="medium"),
                "Description": st.column_config.TextColumn("Description", width="large")
            }
        )
        
        # QC recommendations
        st.markdown("### 💡 QC Recommendations")
        st.markdown("""
        **Action Items:**
        - 🔴 **High Priority:** Review all Age Inconsistencies and Duplicates immediately
        - 🟡 **Medium Priority:** Verify Education-Occupation mismatches and Urban HH without amenities
        - 🟢 **Low Priority:** Check households without eligible children (may be legitimate)

        """)
    else:
        st.success("✅ **No QC issues found!** All data quality checks passed successfully.")
        
        # Debug info to help understand why no issues found
        with st.expander("🔍 Debug Info: Why no issues found?"):
            st.write(f"**Total records being checked:** {len(filtered_df)}")
            st.write(f"**Columns available:** {len(filtered_df.columns) if not filtered_df.empty else 0}")
            
            if not filtered_df.empty:
                # Check what columns exist
                settlement_col = find_column(filtered_df, ['Q5. Type of Settlement', 'Q5', 'settlement_type', 'settlement'])
                lga_col = find_column(filtered_df, ['lgas', 'lga', 'Q2. Local Government Area', 'LGA'])
                age_col = find_column(filtered_df, [
                    'Q17. How old is ${name_questionnaire}?', 
                    'Q17', 
                    'age', 
                    'respondent_age',
                    'Age of child ${child_id} as at when MDA was done (24th to 29th July 2025)',
                    'child_age',
                    'Age',
                    'age_years'
                ])
                enumerator_col = find_column(filtered_df, ['username', 'Type in your Name', 'Enumerator', 'enumerator_name'])
                
                st.write(f"- Settlement column found: {settlement_col if settlement_col else '❌ Not found'}")
                st.write(f"- LGA column found: {lga_col if lga_col else '❌ Not found'}")
                st.write(f"- Age column found: {age_col if age_col else '❌ Not found'}")
                st.write(f"- Enumerator column found: {enumerator_col if enumerator_col else '❌ Not found'}")
                
                if settlement_col:
                    urban_count = filtered_df[filtered_df[settlement_col].astype(str).str.contains('Urban', case=False, na=False)]
                    st.write(f"- Urban households: {len(urban_count)}")
                    
                # Show sample column names to help debug
                st.write("**Sample column names in your data:**")
                col_list = list(filtered_df.columns[:20])  # Show first 20 columns
                for col in col_list:
                    st.write(f"  - {col}")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; margin-top: 2rem;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                border-radius: 15px;
                border-top: 3px solid #0077B5;'>
        <div style='display: flex; justify-content: center; align-items: center; gap: 1.5rem; flex-wrap: wrap; margin-bottom: 1rem;'>
            <div style='font-size: 0.95rem; color: #495057; font-weight: 500;'>
                Created by <span style='color: #0077B5; font-weight: 700;'>Abdulrahaman</span>
            </div>
            <div style='border-left: 2px solid #dee2e6; height: 30px;'></div>
            <div style='font-size: 0.9rem; color: #6c757d;'>
                SARMAAN II Coverage Evaluation Dashboard - Katsina State
            </div>
        </div>
        <div style='margin-top: 1rem; font-size: 0.85rem; color: #868e96;'>
            © 2026 • Powered by Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- MAIN ENTRY POINT ----------------
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        login_page()
    else:
        run_dashboard()


if __name__ == "__main__":
    main()
