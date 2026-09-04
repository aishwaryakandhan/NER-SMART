import pandas as pd
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv("routes.csv")

features = [
    "rainfall",
    "flood_risk",
    "landslide_risk",
    "road_condition",
    "accessibility"
]

X = data[features]
y = data["risk_level"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def predict_risk(
    rainfall,
    flood_risk,
    landslide_risk,
    road_condition,
    accessibility
):

    input_data = [[
        rainfall,
        flood_risk,
        landslide_risk,
        road_condition,
        accessibility
    ]]

    prediction = model.predict(input_data)[0]

    return prediction