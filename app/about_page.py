
import streamlit as st


def render_about():

    # Page-specific styling: modern, consistent agricultural dashboard design
    st.markdown("""
    <style>
    .about-hero {
        position: relative;
        overflow: hidden;
        padding: 3rem 3.2rem;
        margin: 0.4rem 0 2rem 0;
        border-radius: 26px;
        background: linear-gradient(125deg, #e8f7e9 0%, #d3efd8 48%, #f4fbef 100%);
        border: 1px solid #c9e7ce;
        box-shadow: 0 12px 30px rgba(30, 90, 48, 0.10);
    }
    .about-hero:after {
        content: "🌾";
        position: absolute;
        right: 4%;
        bottom: -25px;
        font-size: 145px;
        opacity: 0.13;
        transform: rotate(-12deg);
        pointer-events: none;
    }
    .about-content { position: relative; z-index: 1; max-width: 850px; }
    .about-kicker {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(255,255,255,0.75);
        color: #287342;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 1.3px;
        margin-bottom: 14px;
    }
    .about-title {
        color: #183d2a;
        font-size: clamp(2.1rem, 5vw, 3.25rem);
        line-height: 1.12;
        font-weight: 850;
        margin-bottom: 12px;
    }
    .about-title span, .section-head span { color: #27834b; }
    .about-text {
        color: #365744;
        font-size: 1.03rem;
        line-height: 1.8;
        max-width: 760px;
        margin-top: 12px;
    }
    .section-head {
        color: var(--text-color, #203b2b);
        font-size: 1.65rem;
        line-height: 1.3;
        font-weight: 800;
        margin: 2.2rem 0 0.45rem 0;
    }
    .section-sub {
        color: #718174;
        font-size: 0.98rem;
        margin: 0 0 1.15rem 0;
    }
    .objective-card, .process-card, .model-card, .source-card,
    .contact-card, .team-person, .tech-box, .disclaimer {
        border: 1px solid rgba(90, 130, 98, 0.18);
        border-radius: 18px;
        box-shadow: 0 7px 20px rgba(29, 67, 39, 0.055);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .objective-card, .process-card {
        height: 100%;
        min-height: 185px;
        padding: 1.25rem 1.15rem;
        background: var(--secondary-background-color, #ffffff);
    }
    .objective-card:hover, .process-card:hover, .model-card:hover,
    .tech-box:hover, .team-person:hover, .contact-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 26px rgba(29, 67, 39, 0.11);
    }
    .objective-title, .process-title {
        color: var(--text-color, #244b31);
        font-size: 1.03rem;
        font-weight: 800;
        line-height: 1.4;
        margin: 12px 0 7px;
    }
    .objective-text, .process-text, .model-text, .small-text {
        color: var(--text-color, #53675a);
        font-size: 0.91rem;
        line-height: 1.65;
    }
    .process-card { min-height: 205px; }
    .process-card > div:first-child {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: #e6f5e8;
    }
    .model-card {
        height: 100%;
        padding: 1.5rem;
        background: var(--secondary-background-color, #ffffff) !important;
        border-top: 4px solid #3b9658;
    }
    .model-card:nth-of-type(2) { border-top-color: #7b69c8; }
    .model-title, .source-title, .contact-title {
        color: var(--text-color, #244b31);
        font-size: 1.12rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
    }
    .model-card ul { padding-left: 1.25rem; line-height: 1.8; }
    .source-card { padding: 1.4rem; background: var(--secondary-background-color, #fff); }
    .source-card hr { border: none; border-top: 1px solid rgba(100,130,105,.2); margin: 1rem 0; }
    .tech-box {
        text-align: center;
        min-height: 95px;
        padding: 0.9rem 0.35rem;
        margin-bottom: 0.7rem;
        background: var(--secondary-background-color, #fff);
    }
    .tech-icon { font-size: 1.55rem; margin-bottom: 0.3rem; }
    .tech-name { font-size: 0.82rem; font-weight: 700; color: var(--text-color, #35533d); }
    .team-person {
        height: 100%;
        min-height: 150px;
        padding: 1.1rem 0.45rem;
        text-align: center;
        background: var(--secondary-background-color, #fff);
        overflow-wrap: anywhere;
    }
    .avatar {
        width: 52px;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.7rem;
        border-radius: 50%;
        background: #e5f4e8;
        font-size: 1.65rem;
    }
    .person-name { font-size: 0.9rem; font-weight: 800; line-height: 1.4; color: var(--text-color, #244b31); }
    .person-role { font-size: 0.78rem; margin-top: 0.35rem; color: #32814a; font-weight: 700; }
    .contact-card { padding: 1.2rem; background: var(--secondary-background-color, #fff); min-height: 125px; }
    .disclaimer {
        padding: 1.2rem 1.4rem;
        border-left: 4px solid #d6a33b;
        background: rgba(245, 190, 62, 0.09);
        color: var(--text-color, #59634e);
        line-height: 1.75;
    }
    .footer {
        text-align: center;
        margin-top: 2.5rem;
        padding: 1.5rem 1rem;
        border-top: 1px solid rgba(100,130,105,.22);
    }
    .footer-title { font-size: 1.25rem; font-weight: 850; color: #32814a; }
    .footer-text { color: #7a887d; font-size: 0.86rem; margin-top: 0.3rem; }
    @media (max-width: 768px) {
        .about-hero { padding: 2rem 1.35rem; }
        .about-hero:after { font-size: 90px; right: 1%; }
        .about-text { font-size: 0.95rem; }
        .section-head { font-size: 1.4rem; }
        .team-person { min-height: 145px; }
    }
    </style>
    """, unsafe_allow_html=True)


    # Hero section
    st.markdown("""
    <div class="about-hero">
        <div class="about-content">
            <div class="about-kicker">🌱 AI-POWERED AGRICULTURE</div>
            <div class="about-title">About <span>AgriPredict</span></div>
            <p style="font-size:20px;font-weight:800;color:#173126;">
                AI-powered technology for smarter<br>
                and more sustainable farming.
            </p>
            <div class="about-text">
                AgriPredict is an AI/ML-based agricultural prediction
                system designed to help farmers make data-driven crop
                selection and yield estimation decisions using soil,
                weather, location and agricultural data.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Objectives
    st.markdown(
        '<div class="section-head">🎯 Our Objective</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-sub">Helping farmers make informed decisions for a better tomorrow.</div>',
        unsafe_allow_html=True
    )

    objectives = [
        ("🌱", "Better Crop Selection",
         "Recommend suitable crops based on soil and weather conditions."),
        ("☀️", "Weather-Aware Decisions",
         "Use weather information for the selected location and season."),
        ("📊", "Yield Estimation",
         "Predict expected crop yield using machine learning models."),
        ("🌿", "Smarter Agriculture",
         "Support informed and sustainable farming decisions.")
    ]

    cols = st.columns(4)

    for col, (emoji, title, desc) in zip(cols, objectives):
        with col:
            st.markdown(f"""
            <div class="objective-card">
                <div style="font-size:34px;">{emoji}</div>
                <div class="objective-title">{title}</div>
                <div class="objective-text">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Process
    st.markdown(
        '<div class="section-head">⚙️ How <span>AgriPredict</span> Works</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-sub">From farm input to AI-driven insights.</div>',
        unsafe_allow_html=True
    )

    process = [
        ("1. User Input", "📍",
         "Select state, district, season and area. Enter N, P, K and soil pH."),
        ("2. Weather Data", "☁️",
         "Retrieve temperature, humidity and rainfall for the selected location."),
        ("3. Crop Recommendation", "🌱",
         "The classification model recommends a suitable crop."),
        ("4. Crop Yield Prediction", "📊",
         "The regression model estimates crop yield and total production.")
    ]

    cols = st.columns(4)

    for col, (title, emoji, desc) in zip(cols, process):
        with col:
            st.markdown(f"""
            <div class="process-card">
                <div style="font-size:28px;">{emoji}</div>
                <div class="process-title">{title}</div>
                <p class="process-text">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Machine learning models
    st.markdown(
        '<div class="section-head">🌳 AI & <span>Machine Learning Models</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-sub">Crop recommendation and crop yield estimation.</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="model-card" style="background:#f0fbf4;">
            <div class="model-title">🌱 Crop Recommendation Model</div>
            <p class="model-text">
                Predicts a suitable crop based on soil and weather conditions.
            </p>
            <b>Input Features:</b>
            <ul class="small-text">
                <li>Nitrogen (N)</li>
                <li>Phosphorus (P)</li>
                <li>Potassium (K)</li>
                <li>Soil pH</li>
                <li>Temperature, humidity and rainfall</li>
            </ul>
            <b>Output:</b> Recommended crop
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="model-card" style="background:#f6f0ff;">
            <div class="model-title">📊 Crop Yield Prediction Model</div>
            <p class="model-text">
                Estimates crop yield using location, season, crop and
                environmental information.
            </p>
            <b>Input Features:</b>
            <ul class="small-text">
                <li>State and district</li>
                <li>Season and crop</li>
                <li>Farm area in hectares</li>
                <li>Temperature and humidity</li>
            </ul>
            <b>Output:</b> Estimated yield and production
        </div>
        """, unsafe_allow_html=True)

    # Datasets and data sources
    st.markdown(
        '<div class="section-head">🗄️ Datasets & Data Sources</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown("""
        <div class="source-card">
            <div class="source-title">📄 Crop Recommendation Dataset</div>
            <div class="small-text">
                Contains crop labels and agricultural parameters such as
                soil nutrients, temperature, humidity and rainfall.
            </div>
            <hr>
            <div class="source-title">📄 Yield Dataset</div>
            <div class="small-text">
                Historical crop yield information used to train or evaluate
                the crop yield prediction model.
            </div>
            <hr>
            <div class="source-title">☁️ Open-Meteo API</div>
            <div class="small-text">
                Provides weather information for the selected location.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="source-title" style="margin-bottom:8px;">💻 Technology Stack</div>',
            unsafe_allow_html=True
        )

        technologies = [
            ("🐍", "Python"),
            ("🔢", "NumPy"),
            ("🐼", "Pandas"),
            ("📊", "Plotly"),
            ("🤖", "Scikit-learn"),
            ("⚙️", "Joblib"),
            ("📱", "Streamlit"),
            ("☁️", "Weather API"), 
            ("📈", "Matplotlib"),
            ("📉", "Seaborn"),
            ("📄", "ReportLab")
        ]

        cols = st.columns(4)

        for col, (emoji, name) in zip(cols, technologies):
            with col:
                st.markdown(f"""
                <div class="tech-box">
                    <div class="tech-icon">{emoji}</div>
                    <div class="tech-name">{name}</div>
                </div>
                """, unsafe_allow_html=True)

    # Team
    st.markdown(
        '<div class="section-head">👥 Our Team</div>',
        unsafe_allow_html=True
    )

    team = [
        "Yash B. Pawar",
        "Om Patane",
        "Prasad Kalyani",
        "Sumit Shinde",
        "Pritesh Pawara"
    ]
    team_roll = [
            "Head Developer",
            "Tester",
            "software Engineer",
            "Frontend Developer",
            "Team member"
        ]

    cols = st.columns(5)

    for col, name, role in zip(cols, team, team_roll):
        with col:
            st.markdown(f"""
            <div class="team-person">
                <div class="avatar">👨‍💻</div>
                <div class="person-name">{name}</div>
                <div class="person-role">{role}</div>
            </div>
            """, unsafe_allow_html=True)

    # Project links and contact
    st.markdown(
        '<div class="section-head">🔗 Project Links & Contact</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-title">🔗 Project</div>
            <div class="small-text">
                Explore the project source code and documentation.
            </div>
            <div style="margin-top: 12px;">
                <a href="https://github.com/yashpawar-99/agripredict-ai.git"
                   target="_blank" rel="noopener noreferrer"
                   style="color:#27834b;font-weight:700;overflow-wrap:anywhere;">
                    https://github.com/yashpawar-99/agripredict-ai.git
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-title">✉️ Contact</div>
            <div class="small-text">
                For project-related questions and collaboration.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("**Email:** Add your actual project email address.")

    # Disclaimer
    st.markdown(
        '<div class="section-head">⚠️ Disclaimer</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="disclaimer">
        AgriPredict provides machine-learning-based estimates for
        educational and informational purposes. Predictions may vary
        depending on soil conditions, weather changes, farming practices
        and data quality. Results should not be considered a substitute
        for professional agricultural advice.
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-title">🌱 AgriPredict</div>
        <div class="footer-text">
            AI for a Smarter, Greener Tomorrow • Academic Project • © 2026
        </div>
    </div>
    """, unsafe_allow_html=True)
