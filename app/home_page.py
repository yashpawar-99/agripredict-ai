import streamlit as st


def render_home():
    # Page styling for the AgriPredict home page
    st.markdown("""
    <style>
        .home-hero {
            position: relative;
            overflow: hidden;
            padding: 3.2rem 3rem;
            border-radius: 26px;
            background: linear-gradient(120deg, rgba(10, 54, 39, .97), rgba(24, 105, 69, .92));
            box-shadow: 0 18px 45px rgba(17, 74, 48, .18);
            color: #fff;
            margin: .5rem 0 1.4rem;
        }
        .home-hero:before, .home-hero:after {
            content: "";
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
        }
        .home-hero:before {
            width: 270px; height: 270px; right: -55px; top: -95px;
            background: rgba(194, 235, 127, .12);
        }
        .home-hero:after {
            width: 190px; height: 190px; right: 125px; bottom: -130px;
            border: 1px solid rgba(255,255,255,.17);
        }
        .hero-content { position: relative; z-index: 1; max-width: 760px; }
        .hero-kicker {
            display: inline-block; padding: .42rem .8rem; margin-bottom: 1rem;
            border: 1px solid rgba(220,255,220,.28); border-radius: 999px;
            background: rgba(255,255,255,.09); color: #d9f99d;
            font-size: .75rem; font-weight: 800; letter-spacing: 1.8px;
        }
        .hero-title { font-size: clamp(2.1rem, 4vw, 3.45rem); font-weight: 850; line-height: 1.12; letter-spacing: -1.4px; }
        .hero-title span { color: #c9f27b; }
        .hero-text { max-width: 650px; margin-top: 1rem; color: #e4f3e9; font-size: 1.05rem; line-height: 1.8; }
        .hero-pill {
            display: inline-block; margin-top: 1.35rem; padding: .65rem 1rem;
            border-radius: 12px; background: rgba(201,242,123,.13);
            border: 1px solid rgba(201,242,123,.3); color: #efffd5; font-weight: 650;
        }
        .section-head { color: var(--text-color); font-size: 1.8rem; font-weight: 800; letter-spacing: -.5px; margin-bottom: 1.2rem; }
        .section-head span { color: #24945e; }
        .section-sub { color: #7a8b80; margin-top: -.7rem; margin-bottom: 1.5rem; font-size: .98rem; }
        .feature-card, .step-card {
            height: 100%; min-height: 190px; padding: 1.35rem 1.2rem;
            border: 1px solid rgba(38, 115, 74, .13); border-radius: 18px;
            background: linear-gradient(155deg, var(--secondary-background-color), rgba(38, 115, 74, .035));
            box-shadow: 0 7px 22px rgba(26, 71, 47, .045);
            transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
        }
        .feature-card:hover, .step-card:hover {
            transform: translateY(-4px); box-shadow: 0 14px 28px rgba(26, 71, 47, .10);
            border-color: rgba(36, 148, 94, .42);
        }
        .feature-icon { width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;
            border-radius: 14px; background: rgba(54, 164, 101, .12); font-size: 1.55rem; margin-bottom: 1rem; }
        .feature-title, .step-title { font-size: 1.03rem; font-weight: 750; color: var(--text-color); margin-bottom: .55rem; }
        .feature-text, .step-text { color: var(--text-color); opacity: .72; font-size: .88rem; line-height: 1.65; }
        .step-card { min-height: 175px; position: relative; padding-top: 1.5rem; }
        .step-number { display: flex; align-items: center; justify-content: center; width: 38px; height: 38px;
            margin-bottom: 1rem; border-radius: 12px; background: #208653; color: white; font-weight: 800; font-size: 1.05rem;
            box-shadow: 0 5px 12px rgba(32,134,83,.22); }
        .why-card { min-height: 200px; padding: 1.2rem 1rem; }
        .why-card .feature-icon { margin-left: auto; margin-right: auto; }
        .why-card .feature-title, .why-card .feature-text { text-align: center; }
        .footer { margin-top: 3rem; padding: 1.5rem 1rem; text-align: center; border-top: 1px solid rgba(38,115,74,.16); }
        .footer-title { font-size: 1.25rem; font-weight: 850; color: #24945e; }
        .footer-text { margin-top: .4rem; font-size: .85rem; color: var(--text-color); opacity: .65; }
        div.stButton > button[kind="primary"] {
            border: 0; border-radius: 14px; padding: .85rem 1.5rem; font-weight: 750;
            background: linear-gradient(100deg, #218653, #43ad68); box-shadow: 0 8px 20px rgba(33,134,83,.22);
            transition: transform .2s ease, box-shadow .2s ease;
        }
        div.stButton > button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 12px 25px rgba(33,134,83,.3); }
        @media (max-width: 700px) {
            .home-hero { padding: 2.2rem 1.4rem; border-radius: 20px; }
            .hero-text { font-size: .96rem; }
            .section-head { font-size: 1.5rem; }
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="home-hero">
        <div class="hero-content">
            <div class="hero-kicker">AI / ML AGRICULTURAL SYSTEM</div>
            <div class="hero-title">
                Welcome to <span>AgriPredict</span>
            </div>
            <div class="hero-text">
                Make better farming decisions using soil, weather and
                machine learning. Get suitable crop recommendations
                and estimated crop yield in one place.
            </div>
            <div class="hero-pill">🌱 Smart Farming • Better Decisions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    start_col1, start_col2, start_col3 = st.columns([1, 1, 1])
    with start_col2:
        if st.button(
            "🌱 Start Prediction",
            type="primary",
            use_container_width=True,
            key="home_start_prediction"
        ):
            st.session_state.current_page = "New Prediction"
            st.rerun()

    st.markdown("""
    <div class="section-head" style="text-align:center;margin-top:2.6rem;">
        Smart Agriculture with <span>AgriPredict</span>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("🌱", "Crop Recommendation",
         "Recommend suitable crops using soil nutrients and weather conditions."),
        ("☁️", "Weather-Aware",
         "Use temperature, humidity and rainfall information for predictions."),
        ("📊", "Yield Estimation",
         "Estimate expected crop yield and total farm production."),
        ("🌿", "Sustainable Farming",
         "Support informed and data-driven farming decisions.")
    ]

    cols = st.columns(4, gap="medium")
    for col, (emoji, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{emoji}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head" style="text-align:center;margin-top:2.8rem;">
        How It <span>Works</span>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("1", "Enter Data",
         "Select your location, soil details and farm area."),
        ("2", "Analyze",
         "Retrieve weather information and process farm inputs."),
        ("3", "Predict",
         "Use the crop recommendation and yield prediction models."),
        ("4", "View Results",
         "See the recommended crop and estimated production.")
    ]

    cols = st.columns(4, gap="medium")
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="step-card">
                <div class="step-number">{num}</div>
                <div class="step-title">{title}</div>
                <div class="step-text">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head" style="text-align:center;margin-top:2.8rem;">
        Why <span>AgriPredict?</span>
    </div>
    <div class="section-sub" style="text-align:center;">
        Turning Data into Better Harvests
    </div>
    """, unsafe_allow_html=True)

    reasons = [
        ("📊", "Data Driven",
         "Reliable and accurate insights from real data."),
        ("😊", "User Friendly",
         "Simple and intuitive interface for everyone."),
        ("⚙️", "ML Powered",
         "Built with advanced machine learning models."),
        ("🌿", "Sustainable Agriculture",
         "Helping farmers create a better future."),
        ("🌾", "Higher Productivity",
         "Make informed decisions for better yields.")
    ]

    cols = st.columns(5, gap="small")
    for col, (emoji, title, desc) in zip(cols, reasons):
        with col:
            st.markdown(f"""
            <div class="feature-card why-card">
                <div class="feature-icon">{emoji}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        <div class="footer-title">🌱 AgriPredict</div>
        <div class="footer-text">
            AI for a Smarter, Greener Tomorrow • Academic Project
        </div>
    </div>
    """, unsafe_allow_html=True)
