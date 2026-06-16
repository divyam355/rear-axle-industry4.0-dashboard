import pandas as pd
import numpy as np

np.random.seed(42)

records = []

axles = [f"RA07-{i:04d}" for i in range(1, 11)]

components = [
    ("Drain Plug", 1, 45, 43, 47),
    ("Magnetic Plug", 1, 45, 43, 47),

    ("Drive Head", 12, 180, 171, 189),

    ("Wheel Hub LH", 12, 220, 209, 231),
    ("Wheel Hub RH", 12, 220, 209, 231),

    ("Shaft LH", 12, 120, 114, 126),
    ("Shaft RH", 12, 120, 114, 126),

    ("Brake Caliper LH", 6, 95, 90, 100),
    ("Brake Caliper RH", 6, 95, 90, 100),

    ("Brake Chamber LH", 2, 70, 66.5, 73.5),
    ("Brake Chamber RH", 2, 70, 66.5, 73.5),

    ("Pole Wheel Sensor", 4, 12, 11, 13)
]

for axle in axles:

    for comp, qty, target, lower, upper in components:

        for bolt in range(1, qty + 1):

            actual = round(
                np.random.normal(target, target * 0.04),
                1
            )

            if actual < lower:
                status = "UNDER TORQUE"

            elif actual > upper:
                status = "OVER TORQUE"

            else:
                status = "OK"

            records.append([
                axle,
                comp,
                f"{comp[:3].upper()}-{bolt}",
                target,
                lower,
                upper,
                actual,
                status
            ])

df = pd.DataFrame(
    records,
    columns=[
        "Axle",
        "Component",
        "Bolt ID",
        "Target",
        "Lower",
        "Upper",
        "Actual",
        "Status"
    ]
)

df.to_csv("torque_database.csv", index=False)

print("Torque Database Created")
print("Total Records =", len(df))