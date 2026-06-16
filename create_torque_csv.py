import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)

# ==================================================
# COMPONENTS
# ==================================================

components = {

    "Drive Head": {
        "count": 12,
        "target": 180
    },

    "LH Shaft": {
        "count": 6,
        "target": 120
    },

    "RH Shaft": {
        "count": 6,
        "target": 120
    },

    "LH Wheel Hub": {
        "count": 12,
        "target": 220
    },

    "RH Wheel Hub": {
        "count": 12,
        "target": 220
    },

    "LH Brake Caliper": {
        "count": 6,
        "target": 95
    },

    "RH Brake Caliper": {
        "count": 6,
        "target": 95
    },

    "LH Brake Chamber": {
        "count": 2,
        "target": 70
    },

    "RH Brake Chamber": {
        "count": 2,
        "target": 70
    },

    "Drain Plug": {
        "count": 1,
        "target": 35
    },

    "Magnetic Plug": {
        "count": 1,
        "target": 35
    }

}

# ==================================================
# CREATE DATA
# ==================================================

records = []

for axle in range(1, 11):

    axle_no = f"RA07-{axle:04d}"

    for component, data in components.items():

        target = data["target"]

        min_torque = round(target * 0.95, 2)
        max_torque = round(target * 1.05, 2)

        for bolt in range(1, data["count"] + 1):

            actual = round(
                np.random.normal(
                    target,
                    target * 0.03
                ),
                2
            )

            if actual < min_torque:
                status = "UNDER TORQUE"

            elif actual > max_torque:
                status = "OVER TORQUE"

            else:
                status = "OK"

            records.append([

                datetime.now(),

                axle_no,

                component,

                f"BOLT-{bolt:02d}",

                target,

                min_torque,

                max_torque,

                actual,

                status

            ])

# ==================================================
# DATAFRAME
# ==================================================

df = pd.DataFrame(

    records,

    columns=[

        "Timestamp",

        "Axle",

        "Component",

        "Bolt No",

        "Target Torque",

        "Min Torque",

        "Max Torque",

        "Actual Torque",

        "Status"

    ]

)

# ==================================================
# SAVE CSV
# ==================================================

df.to_csv(
    "torque_data.csv",
    index=False
)

print("Torque database created successfully")
print("Total Records =", len(df))

print(df.head())