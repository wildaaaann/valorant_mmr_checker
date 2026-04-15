import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Valorant MMR Tracker @wildaaan", page_icon="🎮", layout="wide")

# Custom CSS for an Elegant, Fun, and Glassmorphism Theme
st.markdown("""
    <style>
    /* Google Fonts Import for modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    /* Main Background with a richer gradient overlay */
    .stApp {
        background-image: linear-gradient(rgba(10, 15, 25, 0.75), rgba(10, 15, 25, 0.95)), url("https://images.contentstack.io/v3/assets/bltb6530b271fddd0b1/blt05e7094254b0c793/5e626b147778b7707e7191d8/valorant_bg.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
        color: #ece8e1;
    }
    
    /* Elegant Metric Containers with Glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(31, 46, 61, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #ff4655;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    
    /* Base style for Match Cards (Fun & Interactive) */
    .match-card {
        background: rgba(31, 46, 61, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Hover animation */
    .match-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }

    /* Specific border colors for outcomes */
    .match-win { border-left: 6px solid #00ea90; } /* Brighter green */
    .match-lose { border-left: 6px solid #ff4655; } /* Valorant Red */
    .match-draw { border-left: 6px solid #b2b2b2; } /* Silver */
    
    /* Headers tweaking */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Valorant MMR Calculator @wildaaan")
st.markdown("Track your **Rank**, **ELO**, and **Match History** with real-time analytics.")

# INSERT YOUR API KEY HERE
API_KEY = "HDEV-5ab0a08e-6c41-46f9-abfe-520ee4c6cf8c"

# 2. Region Options
region_options = {
    "Asia Pacific (AP)": "ap",
    "North America (NA)": "na",
    "Europe (EU)": "eu",
    "Korea (KR)": "kr",
    "Latin America (LATAM)": "latam",
    "Brazil (BR)": "br"
}

col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Riot ID", placeholder="E.g., lunaticc")
with col2:
    tag = st.text_input("Tagline", placeholder="E.g., 000")
with col3:
    region_display = st.selectbox("Select Region", list(region_options.keys()))
    region = region_options[region_display]

if st.button("Calculate MMR", type="primary"):
    if name and tag:
        with st.spinner('Syncing data with Riot servers... ⏳'):
            headers = {"Authorization": API_KEY}
            
            # Endpoints
            url_mmr = f"https://api.henrikdev.xyz/valorant/v1/mmr/{region}/{name}/{tag}"
            url_history = f"https://api.henrikdev.xyz/valorant/v1/mmr-history/{region}/{name}/{tag}"
            
            try:
                res_mmr = requests.get(url_mmr, headers=headers)
                res_history = requests.get(url_history, headers=headers)
                
                if res_mmr.status_code == 200 and res_history.status_code == 200:
                    data_mmr = res_mmr.json()['data']
                    data_history = res_history.json()['data']
                    
                    st.success(f"🎯 Data found for: **{name}#{tag}**")
                    st.markdown("---")
                    
                    # 3. Top Layout: Rank Image & Main Metrics
                    col_img, col_metrics = st.columns([1, 4])
                    
                    with col_img:
                        rank_image_url = data_mmr.get('images', {}).get('large', 'https://media.valorant-api.com/competitivetiers/564d8e28-c226-3180-6285-e19a31071cb2/0/largeicon.png')
                        st.image(rank_image_url, width=140)
                        
                    with col_metrics:
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Current Rank", data_mmr.get('currenttierpatched', 'Unranked'))
                        m2.metric("Rank Rating (RR)", f"{data_mmr.get('ranking_in_tier', 0)} / 100")
                        m3.metric("Total ELO", data_mmr.get('elo', 0))
                        
                    st.markdown("---")
                    
                    # 4. Bottom Layout: 8 Recent Matches
                    st.subheader("🔥 Last 8 Matches")
                    
                    recent_matches = data_history[:8]
                    
                    if not recent_matches:
                        st.info("No recent competitive match history found.")
                    else:
                        for match in recent_matches:
                            mmr_change = match.get('mmr_change_to_last_game', 0)
                            
                            # Safely extract map name
                            map_data = match.get('map', {})
                            if isinstance(map_data, dict):
                                map_name = map_data.get('name', 'Unknown Map')
                            else:
                                map_name = str(map_data)
                                
                            date_raw = match.get('date', 'Unknown Date')
                            
                            # Logic for colors and symbols
                            if mmr_change > 0:
                                border_class = "match-win"
                                symbol = "📈 VICTORY"
                                change_text = f"+{mmr_change} RR"
                                color_code = "#00ea90"
                            elif mmr_change < 0:
                                border_class = "match-lose"
                                symbol = "📉 DEFEAT"
                                change_text = f"{mmr_change} RR"
                                color_code = "#ff4655"
                            else:
                                border_class = "match-draw"
                                symbol = "➖ DRAW"
                                change_text = "0 RR (Draw / Remake)"
                                color_code = "#b2b2b2"
                            
                            # Render custom HTML card
                            st.markdown(f"""
                            <div class="match-card {border_class}">
                                <h4 style="margin:0; color:#ece8e1; font-weight: 600;">
                                    <span style="color: {color_code}; font-size: 14px; margin-right: 8px;">{symbol}</span> 
                                    {map_name.upper()}
                                </h4>
                                <p style="margin:6px 0 0 0; color:#a0aab5; font-size: 14px;">
                                    Progress: <strong style="color: {color_code}; font-size: 16px;">{change_text}</strong> 
                                    &nbsp;&bull;&nbsp; Date: {date_raw}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                elif res_mmr.status_code == 404:
                    st.error("Player not found. Please check your Riot ID, Tagline, and Region.")
                else:
                    st.error(f"Failed to fetch data from Riot servers. (Status Code: {res_mmr.status_code})")
                    
            except Exception as e:
                st.error(f"System error occurred: {e}")
    else:
        st.warning("Please fill in your Riot ID and Tagline first.")