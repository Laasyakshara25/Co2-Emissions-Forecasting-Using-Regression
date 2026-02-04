import streamlit as st
import pandas as pd
import util

# Page configuration
st.set_page_config(
    page_title="CO2 Emissions Predictor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .prediction-value {
        font-size: 4rem;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .prediction-label {
        color: white;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    util.load_saved_artifacts()
    return True

# Initialize
model_loaded = load_model()

# Header
st.markdown('<h1 class="main-header">🌍 CO2 Emissions Predictor</h1>', unsafe_allow_html=True)
st.markdown("### Predict vehicle CO2 emissions based on specifications")

# Sidebar
with st.sidebar:
    st.header("📊 About")
    st.info("""
    This application predicts CO2 emissions (g/km) based on vehicle specifications using a 
    **Random Forest model** with **99.67% accuracy**.
    
    **Features:**
    - Real-time predictions
    - Environmental impact analysis
    - Comparison with averages
    """)
    
    st.header("🔧 Model Info")
    st.metric("Model Accuracy", "99.67%")
    st.metric("Algorithm", "Random Forest")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🚗 Vehicle Specifications")
    
    # Input fields
    vehicle_class = st.selectbox(
        "Vehicle Class",
        options=util.get_vehicle_classes(),
        help="Select the vehicle class"
    )
    
    fuel_types = util.get_fuel_types()
    fuel_type = st.selectbox(
        "Fuel Type",
        options=list(fuel_types.keys()),
        format_func=lambda x: f"{x} - {fuel_types[x]}",
        help="Select the fuel type"
    )
    
    engine_size = st.slider(
        "Engine Size (L)",
        min_value=0.5,
        max_value=8.0,
        value=2.0,
        step=0.1,
        help="Engine displacement in liters"
    )
    
    cylinders = st.selectbox(
        "Number of Cylinders",
        options=[3, 4, 5, 6, 8, 10, 12, 16],
        index=1,
        help="Number of engine cylinders"
    )
    
    st.subheader("⛽ Fuel Consumption")
    
    fuel_consumption_city = st.number_input(
        "City (L/100 km)",
        min_value=1.0,
        max_value=30.0,
        value=9.9,
        step=0.1,
        help="Fuel consumption in city driving"
    )
    
    fuel_consumption_hwy = st.number_input(
        "Highway (L/100 km)",
        min_value=1.0,
        max_value=25.0,
        value=6.7,
        step=0.1,
        help="Fuel consumption on highway"
    )
    
    fuel_consumption_comb = st.number_input(
        "Combined (L/100 km)",
        min_value=1.0,
        max_value=30.0,
        value=8.5,
        step=0.1,
        help="Combined fuel consumption"
    )
    
    fuel_consumption_mpg = st.number_input(
        "Combined (mpg)",
        min_value=5.0,
        max_value=100.0,
        value=33.0,
        step=0.5,
        help="Fuel consumption in miles per gallon"
    )
    
    predict_button = st.button("🔮 Predict CO2 Emissions", type="primary", use_container_width=True)

with col2:
    st.header("📈 Prediction Results")
    
    if predict_button:
        with st.spinner("Calculating emissions..."):
            # Make prediction
            prediction = util.predict_co2_emissions(
                engine_size=engine_size,
                cylinders=cylinders,
                fuel_consumption_city=fuel_consumption_city,
                fuel_consumption_hwy=fuel_consumption_hwy,
                fuel_consumption_comb=fuel_consumption_comb,
                fuel_consumption_mpg=fuel_consumption_mpg,
                vehicle_class=vehicle_class,
                fuel_type=fuel_type
            )
            
            # Display prediction
            st.markdown(f"""
                <div class="prediction-box">
                    <div class="prediction-label">Predicted CO2 Emissions</div>
                    <div class="prediction-value">{prediction} g/km</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Comparison with average
            avg_emissions = 250  # Average CO2 emissions
            difference = prediction - avg_emissions
            percentage_diff = (difference / avg_emissions) * 100
            
            st.subheader("📊 Comparison")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Your Vehicle", f"{prediction} g/km")
            with col_b:
                st.metric("Average Vehicle", f"{avg_emissions} g/km")
            with col_c:
                st.metric("Difference", f"{difference:.1f} g/km", f"{percentage_diff:.1f}%")
            
            # Visual bar comparison
            st.markdown("### Visual Comparison")
            comparison_data = pd.DataFrame({
                'Category': ['Your Vehicle', 'Average Vehicle'],
                'CO2 Emissions (g/km)': [prediction, avg_emissions]
            })
            st.bar_chart(comparison_data.set_index('Category'))
            
            # Environmental impact
            st.subheader("🌱 Environmental Impact")
            
            # Calculate yearly emissions (assuming 15,000 km/year)
            yearly_km = 15000
            yearly_emissions = (prediction * yearly_km) / 1000  # Convert to kg
            yearly_emissions_tons = yearly_emissions / 1000  # Convert to tons
            
            col_x, col_y = st.columns(2)
            with col_x:
                st.markdown(f"""
                    <div class="metric-card">
                        <h4>📅 Yearly CO2</h4>
                        <h2>{yearly_emissions:.1f} kg</h2>
                        <p>({yearly_emissions_tons:.2f} tons)</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_y:
                trees_needed = yearly_emissions / 21  # One tree absorbs ~21kg CO2/year
                st.markdown(f"""
                    <div class="metric-card">
                        <h4>🌳 Trees to Offset</h4>
                        <h2>{trees_needed:.0f} trees</h2>
                        <p>per year</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Additional metrics
            st.markdown("### 📍 Additional Insights")
            col_i, col_j = st.columns(2)
            with col_i:
                monthly_emissions = yearly_emissions / 12
                st.info(f"**Monthly CO2**: {monthly_emissions:.1f} kg")
            with col_j:
                daily_emissions = yearly_emissions / 365
                st.info(f"**Daily CO2**: {daily_emissions:.2f} kg")
            
            # Recommendations
            if prediction > avg_emissions:
                st.markdown(f"""
                    <div class="warning-box">
                        <h4>⚠️ Higher than average emissions</h4>
                        <p><strong>Your vehicle emits {percentage_diff:.1f}% more CO2 than average.</strong></p>
                        <p><strong>Consider:</strong></p>
                        <ul>
                            <li>🚗 Carpooling or public transport</li>
                            <li>🔧 Regular vehicle maintenance</li>
                            <li>🍃 Eco-friendly driving habits</li>
                            <li>🔄 Upgrading to a more efficient vehicle</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="success-box">
                        <h4>✅ Below average emissions!</h4>
                        <p><strong>Your vehicle emits {abs(percentage_diff):.1f}% less CO2 than average.</strong></p>
                        <p>Great job! Your vehicle is more environmentally friendly than average. 🌍</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👈 Enter vehicle specifications and click 'Predict' to see results")
        
        # Show example
        st.subheader("📝 Example Input")
        example_data = {
            "Specification": ["Vehicle Class", "Fuel Type", "Engine Size", "Cylinders", 
                            "City Consumption", "Highway Consumption"],
            "Value": ["COMPACT", "X (Regular)", "2.0 L", "4", "9.9 L/100km", "6.7 L/100km"]
        }
        st.table(pd.DataFrame(example_data))

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit | Model Accuracy: 99.67% | Random Forest Regressor</p>
    </div>
""", unsafe_allow_html=True)
