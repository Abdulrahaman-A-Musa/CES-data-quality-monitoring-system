# =============================================================================
# SARMAAN II COVERAGE EVALUATION DASHBOARD - KANO STATE
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
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
ADMIN_PASSWORD = "Admin"

LGA_CREDENTIALS = {
    "kiru": ("Kiru@2024", "kiru"),
    "minjibir": ("Minjibir@2024", "minjibir"),
    "rimin_gado": ("RiminGado@2024", "rimin_gado"),
    "shanono": ("Shanono@2024", "shanono"),
    "tarauni": ("Tarauni@2024", "tarauni"),
    "wudil": ("Wudil@2024", "wudil"),
}


KOBO_DATA_URL = "https://kf.kobotoolbox.org/api/v2/assets/aBvDSQGCGKpDegseBTTjcj/export-settings/esauv3HQnXbiSEXbSSoDK95/data.xlsx"

# ---------------- COMMUNITY MAPPING DATA ----------------
COMMUNITY_MAPPING_DATA = """Q2. Local Government Area	Q3.Ward	community_name	Q4. Community Name	Planned HH
kiru	baawa	50111	Baawa Cikin Gari	57
kiru	baawa	50112	Karimawa Gidan Sarki	41
kiru	badafi	50121	Rahma Gidan Wakili	51
kiru	badafi	50122	Unguwan Mamman	14
minjibir	azore	50211	Afanawa Layin Alhaji Nasiru	29
minjibir	azore	50212	Gidan Rinji Layin Yakubu Adamu	12
minjibir	gandurwawa	50221	Asanawar Saadu	23
minjibir	gandurwawa	50222	Gandurwawa Unguwar A Haruna Anda	28
rimin_gado	butu-butu	50311	Kofar Gabas	218
rimin_gado	butu-butu	50312	Rokuwa Gangare	14
rimin_gado	butu-butu	50313	Alkalwa	168
rimin_gado	dawakin_gulu	50321	Sabuwar Unguwar Yomma	21
rimin_gado	dawakin_gulu	50322	Tudun Asakala	17
shanono	alajawa	50411	Koya Nassarawa Gangarawa	30
shanono	alajawa	50412	Unguwar Sarkin Noma	27
shanono	dutsen_bakoshi	50421	Gwazaye	19
shanono	dutsen_bakoshi	50422	Unguwar Arewa	10
tarauni	babban_giji	50511	19Th Link	35
tarauni	babban_giji	50512	Hausawar Gandu Layin Alhaji Sharu	23
tarauni	darmanawa	50521	Darmanawa Layin Tsohuwar Makabarta	214
tarauni	darmanawa	50522	Layin Maman Aslamiya	56
wudil	achika	50611	Hargagi Kuka	33
wudil	achika	50612	Yallawa	29
wudil	dagumawa	50621	Dagumawa	41
wudil	dagumawa	50622	Fagen Zaki Layin Ado Mai Karofi	191"""

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
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            padding: 1.5rem 1rem;
        }
        .metric-value {
            font-size: 2rem;
        }
        .section-header {
            font-size: 1.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------- DATA LOADING ----------------
@st.cache_data(show_spinner="📊 Loading data from KoboToolbox...", ttl=600)
def load_data_from_kobo():
    """Load data directly from KoboToolbox API"""
    try:
        # Check if URL is configured
        if "YOUR_ASSET_ID" in KOBO_DATA_URL or "myurl_here" in KOBO_DATA_URL:
            st.warning("⚠️ KoboToolbox URL is not configured. Please update the KOBO_DATA_URL variable in the code.")
            return pd.DataFrame()
        
        response = requests.get(KOBO_DATA_URL, timeout=60)
        response.raise_for_status()
        excel_file = BytesIO(response.content)
        df = pd.read_excel(excel_file)
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error loading data from KoboToolbox: {e}")
        st.info("Please check that your KOBO_DATA_URL is correct and accessible.")
        return pd.DataFrame()


def preprocess_data(df):
    """Preprocess and map column names"""
    if df.empty:
        return df
    
    df = df.copy()
    
    # Map community codes to names if community_name exists
    if 'community_name' in df.columns:
        df['Community_Code_Original'] = df['community_name'].copy()
        df['Q4. Community Name'] = df['community_name'].astype(str).map(COMMUNITY_CODE_TO_NAME).fillna(df.get('Q4. Community Name', ''))
    
    # Convert date columns
    date_cols = ['Q8. Date', '_submission_time', 'start', 'Date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df


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
    community_cols = ['Q4. Community Name', 'community', 'Community', 'Community Name']
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
    community_col = find_column(df, ['Q4. Community Name', 'community', 'Community Name'])
    
    # QC Check 1: Age of residence vs Age of respondent
    q22_col = find_column(df, ['Q22. How long have you been living continuously in ${community_confirm}', 
                                'Q22', 'years_living', 'residence_duration'])
    q17_col = find_column(df, [
        'Q17. How old is ${name_questionnaire}?', 
        'Q17', 
        'age', 
        'respondent_age',
        'Age of child ${child_id} as at when MDA was done (24th to 29th July 2025)',
        'child_age',
        'Age',
        'age_years'
    ])
    
    if q22_col and q17_col:
        age_issue = df[pd.to_numeric(df[q22_col], errors='coerce') > pd.to_numeric(df[q17_col], errors='coerce')]
        for idx, row in age_issue.iterrows():
            qc_issues.append({
                'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                'Issue Type': 'Age Inconsistency',
                'Description': f'Years living ({row.get(q22_col, "N/A")}) > Age ({row.get(q17_col, "N/A")})',
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
                'Issue Type': 'Education-Occupation Mismatch',
                'Description': f'No formal education but professional occupation',
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
                'Issue Type': 'No Eligible Children',
                'Description': f'Household has 0 eligible children',
                'Row Index': idx
            })
    
    # QC Check 5: Check child_infoo sheet if provided
    if child_df is not None and not child_df.empty:
        # Q90: Age check (>59 months flag)
        q90_col = find_column(child_df, ['Q90. Did someone offer child ${child_idd} azithromycin between 24th and 29th of July 2025?',
                                         'Q90', 'azithromycin_offered', 'child_age_months'])
        if q90_col:
            age_over_59 = child_df[pd.to_numeric(child_df[q90_col], errors='coerce') > 59]
            for idx, row in age_over_59.iterrows():
                qc_issues.append({
                    'LGA': 'Check child_infoo',
                    'Ward': 'Check child_infoo',
                    'Community': 'Check child_infoo',
                    'Issue Type': 'Child Age >59 months',
                    'Description': f'Child age >59 months: {row.get(q90_col, "N/A")}',
                    'Row Index': idx
                })
        
        # Check for duplicate unique_code2
        unique_code2_col = find_column(child_df, ['unique_code2', 'unique_code_2', 'child_unique_code'])
        if unique_code2_col:
            duplicates = child_df[child_df.duplicated(subset=[unique_code2_col], keep=False)]
            for idx, row in duplicates.iterrows():
                qc_issues.append({
                    'LGA': 'Check child_infoo',
                    'Ward': 'Check child_infoo',
                    'Community': 'Check child_infoo',
                    'Issue Type': 'Child Duplicate',
                    'Description': f'Duplicate unique_code2: {row.get(unique_code2_col, "N/A")}',
                    'Row Index': idx
                })
    
    # QC Check 6: Urban settlement without basic amenities (batch check by enumerator)
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
                                    'Issue Type': 'Urban HH No Amenities (Enumerator Pattern)',
                                    'Description': f'Enumerator "{enumerator}" - ALL {len(group)} urban records have NO amenities',
                                    'Row Index': idx
                                })
    
    # QC Check 7: Duplicate unique_code (HH Duplicate)
    unique_code_col = find_column(df, ['unique_code', 'unique_code_1', 'household_code'])
    if unique_code_col:
        duplicates = df[df.duplicated(subset=[unique_code_col], keep=False)]
        for idx, row in duplicates.iterrows():
            qc_issues.append({
                'LGA': row.get(lga_col, 'N/A') if lga_col else 'N/A',
                'Ward': row.get(ward_col, 'N/A') if ward_col else 'N/A',
                'Community': row.get(community_col, 'N/A') if community_col else 'N/A',
                'Issue Type': 'HH Duplicate',
                'Description': f'Duplicate unique_code: {row.get(unique_code_col, "N/A")}',
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
def check_login(username, password):
    username_lower = username.lower().strip()
    
    if username_lower == ADMIN_USERNAME.lower() and password == ADMIN_PASSWORD:
        return 'admin', None
    
    if username_lower in LGA_CREDENTIALS:
        correct_password, lga_name = LGA_CREDENTIALS[username_lower]
        if password == correct_password:
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
            Kano State - Secure Data Analytics Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("<p style='text-align: center; color: #666; margin-bottom: 1.5rem;'>Enter your credentials to continue(Type *Admin* in userName and Password to get access to the App) </p>", unsafe_allow_html=True)
            
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 Login to Dashboard", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("⚠️ Please enter both username and password")
                else:
                    access_level, lga_filter = check_login(username, password)
                    if access_level:
                        st.session_state['logged_in'] = True
                        st.session_state['access_level'] = access_level
                        st.session_state['lga_filter'] = lga_filter
                        st.session_state['username'] = username
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password. Please try again.")


# ---------------- MAIN DASHBOARD ----------------
def run_dashboard():
    """Main dashboard interface"""
    
    # Enhanced Header
    st.markdown("""
    <div class="main-header">
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>📊</div>
        SARMAAN II Coverage Evaluation - KANO STATE
        <div style='font-size: 1.2rem; font-weight: 500; opacity: 0.9; margin-top: 0.5rem; letter-spacing: 2px;'>
            DATA ANALYTICS DASHBOARD
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data first
    df = load_data_from_kobo()
    
    if df is not None and not df.empty:
        df = preprocess_data(df)
    
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
        community_col = find_column(filtered_df, ['Q4. Community Name', 'community', 'Community', 'Community Name'])
        status_col = find_column(filtered_df, ['_validation_status', 'validation_status', 'Validation Status'])
        date_col = find_column(filtered_df, ['Q8. Date', '_submission_time', 'start', 'Date', 'date', 'submission_time'])
        
        # Apply LGA filter for non-admin users
        if st.session_state.get('access_level') == 'lga' and st.session_state.get('lga_filter') and lga_col:
            filtered_df = filtered_df[filtered_df[lga_col] == st.session_state['lga_filter']]
        
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
    
    # Validation status row
    if metrics['approved'] > 0 or metrics['pending'] > 0 or metrics['rejected'] > 0:
        st.markdown('<div class="section-header">✅ Validation & Quality Control Status</div>', unsafe_allow_html=True)
        vcol1, vcol2, vcol3 = st.columns(3)
        with vcol1:
            st.markdown(f"""
            <div class="metric-card card-green">
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>✓</div>
                <div class="metric-value">{metrics['approved']:,}</div>
                <div class="metric-label">Approved Submissions</div>
            </div>
            """, unsafe_allow_html=True)
        with vcol2:
            st.markdown(f"""
            <div class="metric-card card-orange">
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>⏳</div>
                <div class="metric-value">{metrics['pending']:,}</div>
                <div class="metric-label">Awaiting Review</div>
            </div>
            """, unsafe_allow_html=True)
        with vcol3:
            st.markdown(f"""
            <div class="metric-card card-red">
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>✗</div>
                <div class="metric-value">{metrics['rejected']:,}</div>
                <div class="metric-label">Rejected Submissions</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Data Quality Alerts
    issues = identify_data_quality_issues(filtered_df)
    if issues:
        st.markdown('<div class="section-header">⚠️ Data Quality Insights & Alerts</div>', unsafe_allow_html=True)
        for issue in issues:
            alert_class = f"alert-{issue['type']}"
            icon = "⚠️" if issue['type'] == 'warning' else "❌"
            st.markdown(f'<div class="alert-box {alert_class}"><strong>{icon} {issue["message"]}</strong></div>', unsafe_allow_html=True)
    
    # Community Coverage Analysis
    st.markdown('<div class="section-header">📋 Community Coverage Analysis (Planned vs Actual)</div>', unsafe_allow_html=True)
    
    coverage_table = create_community_coverage_table(filtered_df)
    
    if coverage_table is not None:
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        total_communities = len(coverage_table)
        completed = (coverage_table['Actual_HH'] >= coverage_table['Planned HH']).sum()
        partial = ((coverage_table['Actual_HH'] > 0) & (coverage_table['Actual_HH'] < coverage_table['Planned HH'])).sum()
        not_started = (coverage_table['Actual_HH'] == 0).sum()
        
        with col1:
            st.metric("Total Communities", f"{total_communities:,}")
        with col2:
            st.metric("✅ Completed", f"{completed:,}", delta=f"{(completed/total_communities*100):.1f}%")
        with col3:
            st.metric("⚠️ Partial", f"{partial:,}", delta=f"{(partial/total_communities*100):.1f}%")
        with col4:
            st.metric("❌ Not Started", f"{not_started:,}", delta=f"{(not_started/total_communities*100):.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display coverage table
        display_coverage = coverage_table[[
            'Q2. Local Government Area', 'Q3.Ward', 'Q4. Community Name', 'community_name',
            'Planned HH', 'Actual_HH', 'Coverage_%', 'Status'
        ]].rename(columns={
            'Q2. Local Government Area': 'LGA',
            'Q3.Ward': 'Ward',
            'Q4. Community Name': 'Community Name',
            'community_name': 'Community Code',
            'Planned HH': 'Planned HH',
            'Actual_HH': 'Actual HH',
            'Coverage_%': 'Coverage %'
        })
        
        # Color code based on status
        def highlight_status(row):
            if row['Status'] == '✅ Complete':
                return ['background-color: #d1fae5'] * len(row)
            elif row['Status'] == '⚠️ Partial':
                return ['background-color: #fef3c7'] * len(row)
            else:
                return ['background-color: #fee2e2'] * len(row)
        
        st.dataframe(
            display_coverage.style.apply(highlight_status, axis=1),
            use_container_width=True,
            hide_index=True,
            height=400
        )
    else:
        st.info("📊 Community coverage analysis will appear when data is available")
    
    # Visualizations
    st.markdown('<div class="section-header">📊 Interactive Data Visualizations</div>', unsafe_allow_html=True)
    
    # Row 1
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig = create_lga_distribution_chart(filtered_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("LGA distribution chart will appear when data is available")
    
    with chart_col2:
        fig = create_timeline_chart(filtered_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Timeline chart will appear when data is available")
    
    # QC Checks Section
    st.markdown('<div class="section-header">🔍 Quality Control Checks</div>', unsafe_allow_html=True)
    
    # Perform QC checks
    qc_results = perform_qc_checks(filtered_df)
    
    if not qc_results.empty:
        # Summary metrics
        st.markdown("### 📋 QC Summary")
        qc_col1, qc_col2, qc_col3, qc_col4 = st.columns(4)
        
        with qc_col1:
            st.metric("Total Issues Found", len(qc_results), delta=None)
        with qc_col2:
            age_issues = len(qc_results[qc_results['Issue Type'] == 'Age Inconsistency'])
            st.metric("Age Inconsistencies", age_issues)
        with qc_col3:
            duplicates = len(qc_results[qc_results['Issue Type'].str.contains('Duplicate', na=False)])
            st.metric("Duplicates", duplicates)
        with qc_col4:
            other_issues = len(qc_results[~qc_results['Issue Type'].isin(['Age Inconsistency']) & 
                                          ~qc_results['Issue Type'].str.contains('Duplicate', na=False)])
            st.metric("Other Issues", other_issues)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Issue breakdown by type
        st.markdown("### 📊 Issues by Type")
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
        
        # Display filtered QC table
        st.dataframe(
            filtered_qc,
            use_container_width=True,
            height=500,
            column_config={
                "LGA": st.column_config.TextColumn("LGA", width="small"),
                "Ward": st.column_config.TextColumn("Ward", width="small"),
                "Community": st.column_config.TextColumn("Community", width="medium"),
                "Issue Type": st.column_config.TextColumn("Issue Type", width="medium"),
                "Description": st.column_config.TextColumn("Description", width="large"),
                "Row Index": st.column_config.NumberColumn("Row Index", width="small")
            }
        )
        
        # Download QC report
        qc_csv = filtered_qc.to_csv(index=False)
        st.download_button(
            label="📥 Download QC Report",
            data=qc_csv,
            file_name=f"qc_report_{date.today()}.csv",
            mime="text/csv",
            use_container_width=False
        )
        
        # QC recommendations
        st.markdown("### 💡 QC Recommendations")
        st.markdown("""
        **Action Items:**
        - 🔴 **High Priority:** Review all Age Inconsistencies and Duplicates immediately
        - 🟡 **Medium Priority:** Verify Education-Occupation mismatches and Urban HH without amenities
        - 🟢 **Low Priority:** Check households without eligible children (may be legitimate)
        
        **Tips:**
        - Use Row Index to locate specific records in your raw data
        - Export QC report for sharing with field teams
        - Address duplicates before final data submission
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
                if len(filtered_df.columns) > 20:
                    st.write(f"  ... and {len(filtered_df.columns) - 20} more columns")
            else:
                st.warning("No data in filtered dataset. Check your filters!")
    
    # Data Explorer
    st.markdown('<div class="section-header">🔍 Advanced Data Explorer</div>', unsafe_allow_html=True)
    
    st.write(f"Showing **{len(filtered_df):,}** of **{len(df):,}** records")
    
    if not filtered_df.empty:
        # Try to find common display columns using flexible matching (including plural forms)
        possible_display_cols = [
            ['lgas', 'lga', 'Q2. Local Government Area', 'LGA', 'Lgas'],
            ['wards', 'ward', 'Q3.Ward', 'Q3. Ward', 'Ward', 'Wards'],
            ['Q4. Community Name', 'community', 'Community'],
            ['Q8. Date', 'start', 'Date', 'date'],
            ['username', 'Type in your Name', 'Enumerator'],
            ['_validation_status', 'validation_status']
        ]
        
        display_cols = []
        for col_options in possible_display_cols:
            col = find_column(filtered_df, col_options)
            if col:
                display_cols.append(col)
        
        if display_cols:
            st.dataframe(filtered_df[display_cols], use_container_width=True, height=400)
        else:
            st.dataframe(filtered_df.head(100), use_container_width=True, height=400)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(f"""
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
                SARMAAN II Coverage Evaluation Dashboard - Kano State
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
