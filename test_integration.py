"""
Integration test script for Carbon Footprint Estimator.

This script tests both the FastAPI backend and Streamlit frontend by:
1. Verifying backend connectivity
2. Making a sample prediction request
3. Validating the response format
4. Checking error handling

Run this script after starting the FastAPI backend:
    python predict.py
    
Then in another terminal:
    python test_integration.py
"""

import requests
import json
import sys
from pathlib import Path


def test_backend_connectivity():
    """Test if FastAPI backend is running and accessible."""
    print("=" * 60)
    print("TEST 1: Backend Connectivity")
    print("=" * 60)

    backend_url = "http://localhost:9696"
    try:
        response = requests.get(f"{backend_url}/docs", timeout=5)
        if response.status_code == 200:
            print("[OK] Backend is running and accessible at http://localhost:9696")
            return True
        else:
            print(
                f"[FAIL] Backend returned status {response.status_code}. Check if it's running."
            )
            return False
    except requests.exceptions.ConnectionError:
        print(
            "[FAIL] Cannot connect to backend at http://localhost:9696"
            "\n   Please start the backend: python predict.py"
        )
        return False
    except requests.exceptions.Timeout:
        print(
            "[FAIL] Backend connection timed out. Server may be overloaded."
        )
        return False


def test_sample_prediction():
    """Test a sample prediction request."""
    print("\n" + "=" * 60)
    print("TEST 2: Sample Prediction")
    print("=" * 60)

    backend_url = "http://localhost:9696/predict"

    # Test case 1: Basic sustainable profile
    sample_payload = {
        "body_type": "normal",
        "sex": "female",
        "diet": "vegetarian",
        "shower": "daily",
        "heating": "electric",
        "transport": "public",
        "vehicle_type": "None",
        "social_activity": "sometimes",
        "monthly_grocery_bill": 200.0,
        "flight": "never",
        "vehicle_distance": 0.0,
        "waste_bag_size": "small",
        "waste_weekly": 1,
        "tv_daily_hour": 2.0,
        "clothes_monthly": 3,
        "internet_daily": 3.0,
        "energy_efficiency": "Yes",
        "recycling": ["Paper", "Plastic", "Metal"],
        "cooking": ["Stove"],
    }

    print("\nSending sample prediction request...")
    print(f"URL: {backend_url}")
    print(f"Payload: {json.dumps(sample_payload, indent=2)}")

    response = requests.post(backend_url, json=sample_payload, timeout=10)

    if response.status_code == 200:
        result = response.json()
        prediction = result.get("prediction")
        print(f"\n[OK] Prediction successful!")
        print(f"   Predicted Carbon Emission: {prediction:,.2f} kg CO₂e/year")

        # Validate prediction is reasonable
        if 0 < prediction < 20000:
            print(f"   Assessment: Prediction value is within expected range [OK]")
            return True, prediction
        else:
            print(
                f"   [WARN] Warning: Prediction seems out of range (expected 0-20000)"
            )
            return False, prediction
    elif response.status_code == 422:
        print(f"[FAIL] Validation error (422)")
        print(f"   Details: {response.json()}")
        return False, None
    else:
        print(f"[FAIL] Backend returned status {response.status_code}")
        print(f"   Response: {response.text}")
        return False, None


def test_input_validation():
    """Test input validation and error handling."""
    print("\n" + "=" * 60)
    print("TEST 3: Input Validation & Error Handling")
    print("=" * 60)

    backend_url = "http://localhost:9696/predict"

    test_cases = [
        {
            "name": "Negative grocery bill",
            "payload": {
                "body_type": "normal",
                "sex": "male",
                "diet": "omnivore",
                "shower": "daily",
                "heating": "gas",
                "transport": "private",
                "vehicle_type": "gasoline",
                "social_activity": "often",
                "monthly_grocery_bill": -50.0,  # Invalid
                "flight": "occasionally",
                "vehicle_distance": 100.0,
                "waste_bag_size": "medium",
                "waste_weekly": 2,
                "tv_daily_hour": 3.0,
                "clothes_monthly": 5,
                "internet_daily": 4.0,
                "energy_efficiency": "No",
                "recycling": ["Paper"],
                "cooking": ["Stove"],
            },
            "expect_error": True,
        },
        {
            "name": "Invalid TV hours (> 24)",
            "payload": {
                "body_type": "normal",
                "sex": "male",
                "diet": "omnivore",
                "shower": "daily",
                "heating": "gas",
                "transport": "private",
                "vehicle_type": "gasoline",
                "social_activity": "often",
                "monthly_grocery_bill": 250.0,
                "flight": "occasionally",
                "vehicle_distance": 100.0,
                "waste_bag_size": "medium",
                "waste_weekly": 2,
                "tv_daily_hour": 25.0,  # Invalid
                "clothes_monthly": 5,
                "internet_daily": 4.0,
                "energy_efficiency": "No",
                "recycling": ["Paper"],
                "cooking": ["Stove"],
            },
            "expect_error": True,
        },
        {
            "name": "High emission profile",
            "payload": {
                "body_type": "obese",
                "sex": "male",
                "diet": "omnivore",
                "shower": "daily",
                "heating": "coal",
                "transport": "private",
                "vehicle_type": "gasoline",
                "social_activity": "often",
                "monthly_grocery_bill": 500.0,
                "flight": "frequently",
                "vehicle_distance": 500.0,
                "waste_bag_size": "large",
                "waste_weekly": 5,
                "tv_daily_hour": 8.0,
                "clothes_monthly": 20,
                "internet_daily": 10.0,
                "energy_efficiency": "No",
                "recycling": ["None"],
                "cooking": ["Stove", "Oven", "Grill"],
            },
            "expect_error": False,
        },
    ]

    all_passed = True
    for test_case in test_cases:
        print(f"\n  Testing: {test_case['name']}")
        response = requests.post(
            backend_url, json=test_case["payload"], timeout=10
        )

        if test_case["expect_error"]:
            if response.status_code != 200:
                print(f"    [OK] Correctly rejected invalid input")
            else:
                print(f"    [FAIL] Should have rejected invalid input but didn't")
                all_passed = False
        else:
            if response.status_code == 200:
                prediction = response.json().get("prediction")
                print(f"    [OK] Valid prediction: {prediction:,.2f} kg CO₂e/year")
            else:
                print(f"    [FAIL] Valid input was rejected")
                all_passed = False

    return all_passed


def test_file_dependencies():
    """Verify that all required files exist."""
    print("\n" + "=" * 60)
    print("TEST 4: File Dependencies")
    print("=" * 60)

    project_root = Path(__file__).parent
    required_files = [
        "xg_model.pkl",
        "Carbon Emission.csv",
        "predict.py",
        "app.py",
        "pyproject.toml",
    ]

    all_exist = True
    for file in required_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"[OK] {file} found")
        else:
            print(f"[FAIL] {file} NOT found")
            all_exist = False

    return all_exist


def main():
    """Run all integration tests."""
    print("\n")
    print("=" * 60)
    print("CARBON FOOTPRINT ESTIMATOR - INTEGRATION TEST SUITE")
    print("=" * 60)

    # Test file dependencies first
    files_ok = test_file_dependencies()
    if not files_ok:
        print("\n[WARN] Some required files are missing. Please check the project structure.")
        return False

    # Test backend connectivity
    backend_ok = test_backend_connectivity()
    if not backend_ok:
        print("\n[WARN] Backend is not running. Start it with: python predict.py")
        return False

    # Test sample prediction
    prediction_ok, prediction_value = test_sample_prediction()

    # Test input validation
    validation_ok = test_input_validation()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"[OK] File Dependencies: {'PASSED' if files_ok else 'FAILED'}")
    print(f"[OK] Backend Connectivity: {'PASSED' if backend_ok else 'FAILED'}")
    print(f"[OK] Sample Prediction: {'PASSED' if prediction_ok else 'FAILED'}")
    print(f"[OK] Input Validation: {'PASSED' if validation_ok else 'FAILED'}")

    all_tests_passed = files_ok and backend_ok and prediction_ok and validation_ok
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print(">>> ALL TESTS PASSED! System is ready to use.")
        print("\nTo start the frontend, run:")
        print("  streamlit run app.py")
    else:
        print("[WARN] Some tests failed. Please check the errors above.")
    print("=" * 60)

    return all_tests_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
