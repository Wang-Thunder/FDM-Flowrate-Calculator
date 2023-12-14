import json
import matplotlib.pyplot as plt
import os
import math
import numpy as np

def initialize_parameters():
    
    # Initialize/update parameters with default values and save them to a file. Keep existing results if they exist.
    
    default_parameters = {
        "flow_rate_start": 12,  # mm³/s
        "flow_rate_end": 20,    # mm³/s
        "temp_start": 210,      # celsius 
        "temp_end": 230,        # celsius
        "blob_volume": 100      # mm
    }

    # Check if the file already exists and has results
    if os.path.exists("parameters.txt"):
        with open("parameters.txt", "r") as file:
            existing_parameters = json.load(file)
        if "results" in existing_parameters:
            default_parameters["results"] = existing_parameters["results"]

    with open("parameters.txt", "w") as file:
        file.write(json.dumps(default_parameters, indent=4))

    print("\nParameters (re)initialized and saved to parameters.txt.")
    print("\nCurrent Parameters:")
    print(json.dumps(default_parameters, indent=4))

def modify_parameters():
 
    # Modify the existing parameters in the parameters.txt file.

    if os.path.exists("parameters.txt"):
        with open("parameters.txt", "r") as file:
            parameters = json.load(file)
        
        # Show current parameters and ask for changes
        print("\nCurrent Parameters:")
        print(json.dumps(parameters, indent=4))
        print("\nEnter new parameters (leave blank to keep current value):")

        flow_rate_start = input("New flow rate start (mm^3/s): ")
        flow_rate_end = input("New flow rate end (mm^3/s): ")
        temp_start = input("New temperature start (°C): ")
        temp_end = input("New temperature end (°C): ")
        blob_volume = input("New blob volume (mm): ")

        # Update parameters if new values are provided
        parameters["flow_rate_start"] = float(flow_rate_start) if flow_rate_start else parameters["flow_rate_start"]
        parameters["flow_rate_end"] = float(flow_rate_end) if flow_rate_end else parameters["flow_rate_end"]
        parameters["temp_start"] = float(temp_start) if temp_start else parameters["temp_start"]
        parameters["temp_end"] = float(temp_end) if temp_end else parameters["temp_end"]
        parameters["blob_volume"] = float(blob_volume) if blob_volume else parameters["blob_volume"]

        with open("parameters.txt", "w") as file:
            file.write(json.dumps(parameters, indent=4))

        print("\nParameters updated.")
    else:
        print("No existing parameters found. Please initialize parameters first.")

def enter_results():

    # Enter test results (weights) for each set and save to parameters.txt. Calculates flow rate and temperature for each test based on the test number.
    if os.path.exists("parameters.txt"):
        with open("parameters.txt", "r") as file:
            parameters = json.load(file)

        results = {}
        num_tests_per_temp = parameters["flow_steps"]
        temp_increment = parameters["temp_offset"]
        flow_increment = parameters["flow_offset"]
        current_temp = parameters["temp_start"]

        for i in range(calculate_number_of_tests(parameters)):
            if i % num_tests_per_temp == 0 and i != 0:
                current_temp += temp_increment

            flow_rate = parameters["flow_start"] + (i % num_tests_per_temp) * flow_increment
            weight = float(input(f"Enter weight for test {i+1} at {current_temp}°C, {flow_rate}mm³/s (in grams): "))
            results[f"test{i+1}"] = {"weight": weight, "temperature": current_temp, "flow_rate": flow_rate}

        parameters["results"] = results

        with open("parameters.txt", "w") as file:
            file.write(json.dumps(parameters, indent=4))

        print("\nResults saved.")
    else:
        print("No existing parameters found. Please enter parameters first.")


        
def calculate_number_of_tests(parameters):

    # Calculate test steps
    flow_rate_range = parameters["flow_rate_end"] - parameters["flow_rate_start"]
    temp_range = parameters["temp_end"] - parameters["temp_start"]

    # Increments of 2 for flow rate and 10 for temperature
    num_flow_rate_tests = flow_rate_range / 2 + 1
    num_temp_tests = temp_range / 10 + 1
    return int(num_flow_rate_tests * num_temp_tests)

def calculate_filament_length(weight, density_pla, diameter):

    # Calculate the length of filament used based on weight.

    radius = diameter / 2
    cross_sectional_area = math.pi * (radius ** 2)
    volume = weight / density_pla  # Volume in cm³
    length = volume / (cross_sectional_area / 100)  # Convert area to cm²
    return length  # Length in cm

def run_analysis():

    # Run the analysis using the values from parameters.txt and make graphs. Accounts for different temperatures and flow rates.

    if os.path.exists("parameters.txt"):
        with open("parameters.txt", "r") as file:
            parameters = json.load(file)

        if "results" in parameters:
            density_pla = 1.24  # g/cm³, density of PLA
            diameter = 1.75  # mm, diameter of filament

            data = []
            for test_data in parameters["results"].values():
                filament_length = calculate_filament_length(test_data["weight"], density_pla, diameter) / 10  # converting to mm
                actual_flow_rate = filament_length  # Simplified assumption
                data.append((test_data["temperature"], test_data["flow_rate"], actual_flow_rate))


        else:
            print("No results found. Please enter test results first.")
    else:
        print("No existing parameters found. Please initialize parameters first.")


# Main loop
def main():
    while True:
        print("\nOptions:")
        print("1. Initialize Parameters")
        print("2. Modify Parameters")
        print("3. Enter Test Results")
        print("4. Run Analysis")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            initialize_parameters()
        elif choice == '2':
            modify_parameters()
        elif choice == '3':
            enter_results()
        elif choice == '4':
            run_analysis()
        elif choice == '5':
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
