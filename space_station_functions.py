# ---------------------------------------------------------
# Example 1: Defining a Function and Identifying Parts
# ---------------------------------------------------------
print("--- Example 1 Output ---")

def initiate_warp_drive(destination_galaxy):
    """
    Initiates the ship's warp drive to a specific galaxy.
    parameter: destination_galaxy
    """
    print(f"Warp drive engaged! Traveling to the {destination_galaxy} galaxy.")

initiate_warp_drive("Andromeda")


# ---------------------------------------------------------
# Example 2: Different Argument Types
# ---------------------------------------------------------
print("\n--- Example 2 Output ---")

initiate_warp_drive("Sombrero")

target_sector = "Triangulum"
initiate_warp_drive(target_sector)

initiate_warp_drive("Milky" + " " + "Way")


# ---------------------------------------------------------
# Example 3: Local Variables
# ---------------------------------------------------------
print("\n--- Example 3 Output ---")

def repair_hull():
    # 'welding_torch_fuel' is a local variable
    welding_torch_fuel = 100
    print(f"Hull repaired. Fuel remaining: {welding_torch_fuel}%")

repair_hull()

print("Attempting to access 'welding_torch_fuel' globally:")
try:
    print(welding_torch_fuel)
except NameError as e:
    print(f"Error encountered: {e}")


# ---------------------------------------------------------
# Example 4: Parameter Scope
# ---------------------------------------------------------
print("\n--- Example 4 Output ---")

def scan_lifeform(alien_species_id):
    print(f"Scanning lifeform with ID: {alien_species_id}...")
    print("Scan complete. No threat detected.")

scan_lifeform("Xenomorph-001")

# Attempting to use the parameter name outside the function
print("Attempting to access parameter 'alien_species_id' globally:")
try:
    print(alien_species_id)
except NameError as e:
    print(f"Error encountered: {e}")


# ---------------------------------------------------------
# Example 5: Variable Shadowing (Global vs Local)
# ---------------------------------------------------------
print("\n--- Example 5 Output ---")

# Global variable
oxygen_level = 98

def emergency_airlock_procedure():
    # Local variable with the SAME NAME as the global variable
    oxygen_level = 15
    print(f"Inside function (Airlock): Oxygen level is {oxygen_level}%")

print(f"Before function call: Oxygen level is {oxygen_level}%")
emergency_airlock_procedure()
print(f"After function call: Oxygen level is {oxygen_level}%")