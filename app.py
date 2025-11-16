"""
Streamlit frontend for Carbon Footprint Estimator.

This app provides an interactive UI for users to input their lifestyle and activity data,
then calls a FastAPI backend to predict their carbon emission footprint.
"""

import streamlit as st
import requests
from datetime import datetime


# Configuration
BACKEND_URL = "http://127.0.0.1:9696/predict"
REQUEST_TIMEOUT = 10  # seconds


# ============================================================================
# Streamlit Page Configuration
# ============================================================================
st.set_page_config(
    page_title="Carbon Footprint Estimator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)



# ============================================================================
# Helper Functions
# ============================================================================
def validate_inputs(inputs: dict) -> tuple[bool, str]:
    """Validate user inputs before sending to backend."""
    # Numeric validations
    if inputs["monthly_grocery_bill"] < 0:
        return False, "Monthly grocery bill cannot be negative."
    if inputs["vehicle_distance"] < 0:
        return False, "Vehicle distance cannot be negative."
    if inputs["waste_weekly"] < 0:
        return False, "Weekly waste cannot be negative."
    if inputs["tv_daily_hour"] < 0 or inputs["tv_daily_hour"] > 24:
        return False, "TV daily hours must be between 0 and 24."
    if inputs["clothes_monthly"] < 0:
        return False, "Monthly clothes purchases cannot be negative."
    if inputs["internet_daily"] < 0 or inputs["internet_daily"] > 24:
        return False, "Internet daily hours must be between 0 and 24."

    # Categorical validations (should not fail in normal UI but good for robustness)
    if not inputs["body_type"] or inputs["body_type"] == "":
        return False, "Please select a body type."
    if not inputs["sex"] or inputs["sex"] == "":
        return False, "Please select a sex."

    return True, ""


def call_prediction_api(inputs: dict) -> dict:
    """Call the FastAPI backend and return the prediction or error."""
    is_valid, error_msg = validate_inputs(inputs)
    if not is_valid:
        return {"error": error_msg, "status": "validation_error"}

    payload = {
        "body_type": inputs["body_type"],
        "sex": inputs["sex"],
        "diet": inputs["diet"],
        "shower": inputs["shower"],
        "heating": inputs["heating"],
        "transport": inputs["transport"],
        "vehicle_type": inputs["vehicle_type"],
        "social_activity": inputs["social_activity"],
        "monthly_grocery_bill": inputs["monthly_grocery_bill"],
        "flight": inputs["flight"],
        "vehicle_distance": inputs["vehicle_distance"],
        "waste_bag_size": inputs["waste_bag_size"],
        "waste_weekly": inputs["waste_weekly"],
        "tv_daily_hour": inputs["tv_daily_hour"],
        "clothes_monthly": inputs["clothes_monthly"],
        "internet_daily": inputs["internet_daily"],
        "energy_efficiency": inputs["energy_efficiency"],
        "recycling": inputs["recycling"],
        "cooking": inputs["cooking"],
    }

    request_error = None
    response_data = None

    # Attempt API call with error handling
    if request_error is None:
        request_error = None
        response_data = None
        connection_error = None

        connection_error = None
        timeout_error = None
        http_error = None

        # Try to connect to backend
        connection_error = None
        try:
            response = requests.post(
                BACKEND_URL, json=payload, timeout=REQUEST_TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            connection_error = "Cannot connect to backend service. Please ensure the FastAPI server is running on http://localhost:9696"
            return {"error": connection_error, "status": "connection_error"}
        except requests.exceptions.Timeout:
            timeout_error = f"Request timed out after {REQUEST_TIMEOUT} seconds. Backend server may be overloaded."
            return {"error": timeout_error, "status": "timeout_error"}
        except requests.exceptions.RequestException as e:
            http_error = f"Request error: {str(e)}"
            return {"error": http_error, "status": "request_error"}

        # Parse response
        if response.status_code == 200:
            response_data = response.json()
            return {"status": "success", "data": response_data}
        elif response.status_code == 422:
            validation_error = "Invalid input format. Please check your entries."
            error_detail = response.json().get("detail", validation_error)
            return {
                "error": f"{validation_error}\nDetails: {error_detail}",
                "status": "validation_error",
            }
        else:
            server_error = f"Backend returned status code {response.status_code}. Response: {response.text}"
            return {"error": server_error, "status": "server_error"}

    return {"error": "Unknown error occurred.", "status": "unknown_error"}


def format_prediction_result(prediction_value: float) -> str:
    """Format the prediction value for display."""
    return f"{prediction_value:,.2f} kg CO₂e"


# ============================================================================
# Main UI Layout - Two Column Form with Centered Predict Button
# ============================================================================

# Create a container for the form
form_container = st.container()

with form_container:
    st.title("🌍 Carbon Footprint Estimator")
    st.markdown(
        """
        **Predict your carbon footprint based on your lifestyle choices.
        Fill in your information below and click the predict button to get your carbon emission estimate.**
        """
    )
    st.markdown("---")



    # Create two columns for input fields
    col1, col2 = st.columns(2, gap="large")

    # ========== COLUMN 1 ==========
    with col1:
        st.subheader("📋 Personal & Diet Information")

        # Personal Information
        body_type = st.selectbox(
            "Body Type",
            options=["underweight", "normal", "overweight", "obese"],
            help="Select your body type classification.",
        )
        
        sex = st.selectbox(
            "Sex",
            options=["male", "female", "other"],
            help="Select your sex.",
        )

        # Diet & Food
        diet = st.selectbox(
            "Diet Type",
            options=["vegan", "vegetarian", "pescatarian", "omnivore"],
            help="What type of diet do you follow?",
        )
        
        monthly_grocery_bill = st.number_input(
            "Monthly Grocery Bill ($)",
            min_value=0.0,
            step=10.0,
            value=200.0,
            help="Your average monthly spending on groceries.",
        )

        # Daily Habits
        st.subheader("🏠 Daily Habits")
        
        shower = st.selectbox(
            "Shower Frequency",
            options=["less frequently", "more frequently", "daily", "twice a day"],
            help="How often do you shower?",
        )
        
        tv_daily_hour = st.slider(
            "TV/Screen Time (hours/day)",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            value=3.0,
            help="Average hours per day spent on TV/screens.",
        )
        
        internet_daily = st.slider(
            "Internet Usage (hours/day)",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            value=4.0,
            help="Average hours per day spent on the internet.",
        )

    # ========== COLUMN 2 ==========
    with col2:
        st.subheader("🚗 Transportation & Energy")

        # Transportation
        transport = st.selectbox(
            "Primary Transport",
            options=["public", "walking/bicycling", "private"],
            help="Your primary mode of transportation.",
        )
        
        vehicle_type = st.selectbox(
            "Vehicle Type",
            options=["None", "petrol", "diesel", "hybrid", "lpg", "electric"],
            help="Type of vehicle you own (if applicable).",
        )
        
        vehicle_distance = st.number_input(
            "Vehicle Distance (km/week)",
            min_value=0.0,
            step=10.0,
            value=100.0,
            help="Average distance driven per week.",
        )

        # Energy & Utilities
        st.subheader("⚡ Energy & Consumption")
        
        heating = st.selectbox(
            "Heating Source",
            options=["coal", "natural gas", "wood", "electricity", "none"],
            help="Your primary heating source.",
        )
        
        energy_efficiency = st.selectbox(
            "Energy Efficiency",
            options=["No", "Sometimes", "Yes"],
            help="Do you have energy-efficient appliances/home?",
        )

        # Consumption & Waste
        st.subheader("♻️ Waste & Shopping")
        
        clothes_monthly = st.number_input(
            "Clothes Purchased (items/month)",
            min_value=0,
            step=1,
            value=5,
            help="Average number of clothing items purchased per month.",
        )
        
        waste_bag_size = st.selectbox(
            "Waste Bag Size",
            options=["small", "medium", "large", "extra large"],
            help="Typical size of your weekly waste bags.",
        )
        
        waste_weekly = st.number_input(
            "Waste Bags Per Week",
            min_value=0,
            step=1,
            value=2,
            help="Number of waste bags per week.",
        )

    # ========== FULL WIDTH FIELDS ==========
    st.markdown("---")
    st.subheader("🍳 Lifestyle Choices")

    col3, col4, col5 = st.columns(3)

    with col3:
        recycling = st.multiselect(
            "Items You Recycle",
            options=["Metal", "Plastic", "Paper", "Glass", "None"],
            default=["Paper", "Plastic"],
            help="Select all items you regularly recycle.",
        )

    with col4:
        cooking = st.multiselect(
            "Cooking Methods",
            options=["Stove", "Oven", "Microwave", "Grill", "Airfryer", "None"],
            default=["Stove"],
            help="Select your primary cooking methods.",
        )

    with col5:
        social_activity = st.selectbox(
            "Social Activity Level",
            options=["never", "sometimes", "often"],
            help="How frequently do you engage in social activities?",
        )
        
        flight = st.selectbox(
            "Flight Frequency",
            options=[ "never","rarely", "frequently", "very frequently"],
            help="How often do you take flights?",
        )

# ========== CENTERED PREDICT BUTTON ==========
st.markdown("---")

# Create columns to center the button
col_button_left, col_button_center, col_button_right = st.columns([1, 2, 1])

with col_button_center:
    predict_button = st.button(
        "🚀 Predict Carbon Footprint",
        use_container_width=True,
        type="primary"
    )

# Collect all inputs
user_inputs = {
    "body_type": body_type,
    "sex": sex,
    "diet": diet,
    "shower": shower,
    "heating": heating,
    "transport": transport,
    "vehicle_type": vehicle_type,
    "social_activity": social_activity,
    "monthly_grocery_bill": monthly_grocery_bill,
    "flight": flight,
    "vehicle_distance": vehicle_distance,
    "waste_bag_size": waste_bag_size,
    "waste_weekly": waste_weekly,
    "tv_daily_hour": tv_daily_hour,
    "clothes_monthly": clothes_monthly,
    "internet_daily": internet_daily,
    "energy_efficiency": energy_efficiency,
    "recycling": recycling if recycling else ["None"],
    "cooking": cooking if cooking else ["None"],
}

# ========== PREDICTION RESULT SECTION ==========
if predict_button:
    with st.spinner("⏳ Calculating your carbon footprint..."):
        result = call_prediction_api(user_inputs)

    if result["status"] == "success":
        prediction_value = result["data"]["prediction"]
        
        # Display result prominently
        st.markdown("---")
        st.markdown("### ✅ Your Carbon Footprint Estimate")
        
        # Create columns for better layout
        result_col1, result_col2, result_col3 = st.columns([1, 2, 1])
        
        with result_col2:
            st.metric(
                label="Carbon Footprint Estimate",
                value=format_prediction_result(prediction_value),
                label_visibility="hidden"
            )
        
        # Assessment badge
        if prediction_value < 2000:
            assessment = "🟢 Sustainable - Your footprint is well below average!"
            color = "green"
        elif prediction_value < 5000:
            assessment = "🟡 Average - You're on par with typical emissions."
            color = "blue"
        elif prediction_value < 8000:
            assessment = "🟠 High - Consider reducing your carbon footprint."
            color = "orange"
        else:
            assessment = "🔴 Very High - Significant reduction opportunities exist."
            color = "red"
        
        st.markdown(f"<h4 style='text-align: center;'>{assessment}</h4>", unsafe_allow_html=True)

        # Store result in session state for reference
        st.session_state.last_prediction = {
            "value": prediction_value,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "inputs": user_inputs,
        }

    else:
        error_message = result.get("error", "An unknown error occurred.")
        st.error(f"❌ Prediction Failed\n\n{error_message}")
        st.info(
            "**Troubleshooting Tips:**\n"
            "1. Ensure the FastAPI backend is running on http://127.0.0.1:9696\n"
            "2. Check your internet connection\n"
            "3. Verify all input values are valid\n"
            "4. Try again in a few moments if the server is temporarily overloaded"
        )

# Display last prediction if available
if "last_prediction" in st.session_state and not predict_button:
    st.markdown("---")
    st.markdown("### 📜 Last Prediction")
    last = st.session_state.last_prediction
    col_ts, col_result = st.columns(2)
    with col_ts:
        st.write(f"**Timestamp:** {last['timestamp']}")
    with col_result:
        st.write(f"**Result:** {format_prediction_result(last['value'])}")

# ============================================================================
# Footer
# ============================================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 11px;'>
    🌍 Carbon Footprint Estimator | Powered by FastAPI & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
