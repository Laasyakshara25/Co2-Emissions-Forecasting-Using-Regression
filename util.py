import pickle
import json
import numpy as np
import pandas as pd

__model = None
__data_columns = None

def load_saved_artifacts():
    """Load the trained model and column configuration"""
    global __model
    global __data_columns
    
    print("Loading saved artifacts...")
    
    # Load the trained model
    with open('Co2_emissions.pickle', 'rb') as f:
        __model = pickle.load(f)
    
    # Load column configuration
    with open("columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
    
    print("Model and artifacts loaded successfully!")

def get_data_columns():
    """Return the list of feature columns"""
    return __data_columns

def predict_co2_emissions(engine_size, cylinders, fuel_consumption_city, 
                          fuel_consumption_hwy, fuel_consumption_comb, 
                          fuel_consumption_mpg, vehicle_class, fuel_type):
    """
    Predict CO2 emissions based on vehicle specifications
    
    Parameters:
    -----------
    engine_size : float
        Engine size in liters
    cylinders : int
        Number of cylinders
    fuel_consumption_city : float
        Fuel consumption in city (L/100 km)
    fuel_consumption_hwy : float
        Fuel consumption on highway (L/100 km)
    fuel_consumption_comb : float
        Combined fuel consumption (L/100 km)
    fuel_consumption_mpg : float
        Fuel consumption in mpg
    vehicle_class : str
        Vehicle class (e.g., 'COMPACT', 'SUV - SMALL', 'MID-SIZE', 'SUV - STANDARD', 'FULL-SIZE')
    fuel_type : str
        Fuel type (e.g., 'X' for Regular gasoline, 'Z' for Premium gasoline, 'D' for Diesel)
    
    Returns:
    --------
    float : Predicted CO2 emissions in g/km
    """
    
    # Calculate weighted fuel consumption (as done in training)
    fuel_consumption_weighted = (fuel_consumption_city * 0.55 + fuel_consumption_hwy * 0.45)
    
    # Create a dataframe with all features initialized to 0
    x = pd.DataFrame(np.zeros((1, len(__data_columns))), columns=__data_columns)
    
    # Set the numeric features (using exact capitalized names from model)
    x['Engine Size(L)'] = engine_size
    x['Cylinders'] = cylinders
    x['Fuel Consumption City (L/100 km)'] = fuel_consumption_city
    x['Fuel Consumption Hwy (L/100 km)'] = fuel_consumption_hwy
    x['Fuel Consumption Comb (L/100 km)'] = fuel_consumption_comb
    x['Fuel Consumption Comb (mpg)'] = fuel_consumption_mpg
    x['Fuel Consumption Weighted'] = fuel_consumption_weighted
    
    # Set vehicle class (one-hot encoded) - format: "Vehicle Class_COMPACT"
    vehicle_class_col = f"Vehicle Class_{vehicle_class.upper()}"
    if vehicle_class_col in __data_columns:
        x[vehicle_class_col] = 1
    
    # Set fuel type (one-hot encoded) - format: "Fuel Type_X"
    fuel_type_col = f"Fuel Type_{fuel_type.upper()}"
    if fuel_type_col in __data_columns:
        x[fuel_type_col] = 1
    
    # Make prediction
    prediction = __model.predict(x)[0]
    
    return round(prediction, 2)

def get_vehicle_classes():
    """Return available vehicle classes"""
    return ['COMPACT', 'SUV - SMALL', 'MID-SIZE', 'SUV - STANDARD', 'FULL-SIZE']

def get_fuel_types():
    """Return available fuel types with descriptions"""
    return {
        'X': 'Regular gasoline',
        'Z': 'Premium gasoline',
        'D': 'Diesel'
    }

if __name__ == '__main__':
    # Test the utility functions
    load_saved_artifacts()
    print(f"Data columns: {len(__data_columns)}")
    print(f"Vehicle classes: {get_vehicle_classes()}")
    print(f"Fuel types: {get_fuel_types()}")
    
    # Test prediction
    test_prediction = predict_co2_emissions(
        engine_size=2.0,
        cylinders=4,
        fuel_consumption_city=9.9,
        fuel_consumption_hwy=6.7,
        fuel_consumption_comb=8.5,
        fuel_consumption_mpg=33,
        vehicle_class='COMPACT',
        fuel_type='X'
    )
    print(f"\nTest prediction: {test_prediction} g/km")
