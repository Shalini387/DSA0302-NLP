machines = {
    "M1": "Active",
    "M2": "Active",
    "M3": "Maintenance",
    "M4": "Active"
}

produces = {
    "M1": "Gear",
    "M2": "Wheel",
    "M3": "Gear",
    "M4": "Bolt"
}

for machine, status in machines.items():
    if status == "Active":
        print(f"Producing({machine})")
    else:
        print(f"¬Producing({machine})")

print("\nAvailable Products:")

for machine, product in produces.items():
    if machines[machine] == "Active":
        print(f"Available({product})")

if machines["M3"] == "Maintenance" and produces["M3"] == "Gear":
    print("\nGear production is affected by M3 maintenance.")