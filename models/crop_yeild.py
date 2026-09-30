import pandas as pd 
import numpy as np
import joblib
import os 

from sklearn.model_selection import train_test_split 
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer 
from sklearn.preprocessing import OneHotEncoder ,StandardScaler
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score


MODEL_FILE = "yeild_model.pkl"
PIPELINE_FILE = "yeild_pipeline.pkl"
OUTPUT_SCALER = "output_scaler.pkl"

def build_pipeline():
    num_pipeline = Pipeline(steps=[
            ("imputer",SimpleImputer(strategy="mean")),
            ("scaling",StandardScaler())
    ])
    
    cat_pipeline = Pipeline(steps=[
            ("imputer",SimpleImputer(strategy="most_frequent")),
            ("encoder",OneHotEncoder(handle_unknown="ignore"))
    ])
    
    final_pipeline = ColumnTransformer(transformers=[
            ("numerial",num_pipeline,num_cols),
            ("categorical",cat_pipeline,cat_cols)
    ])
    
    return final_pipeline

model = joblib.load(MODEL_FILE)
pipeline = joblib.load(PIPELINE_FILE)
ot_scaler = joblib.load(OUTPUT_SCALER)


def predict_yield(state, district, season, crop, temperature, humidity, area):

    input_data = pd.DataFrame([{
        "State_Name": state,
        "District_Name": district,
        "Season": season,
        "Crop": crop,
        "Temperature": temperature,
        "Humidity": humidity,
        "Area": area
    }])

    input_data["Area"] = np.log1p(input_data["Area"])

    input_transform = pipeline.transform(input_data)

    input_pred = model.predict(input_transform)

    output_pred = ot_scaler.inverse_transform(
        input_pred.reshape(-1, 1)
    )

    final_output = np.expm1(output_pred)

    production = final_output[0][0] * area

    return final_output[0][0], production



if not os.path.exists(MODEL_FILE):
    
    df = pd.read_csv("../data/crop_yield.csv")

    cat_cols = ["State_Name","District_Name","Season","Crop"]
    num_cols = ["Temperature","Humidity","Area"]



    df = df.dropna(subset=['Production'])

    #Applies Log Transformation: Both Area and Production features 
    #typically have heavily right-skewed distributions with extreme outliers 
    df["Yeild"] = (df["Production"]/df["Area"])

    df['Area'] = np.log1p(df['Area'])
    df['Yeild'] = np.log1p(df['Yeild'])

    df = df.drop("Soil_Moisture",axis=1)


    df = df.drop(columns=["Crop_Year","Production"])

    df = df.drop_duplicates()


    X = df.drop(columns=["Yeild"])
    y = df["Yeild"]

    x_train, x_test, y_train, y_test = train_test_split(X,y, stratify=df["Crop"],
                                        test_size=0.2,
                                        random_state=42
                                        )


    pipeline = build_pipeline()

    x_train_encoded = pipeline.fit_transform(x_train)
    x_test_encoded = pipeline.transform(x_test)

    le = StandardScaler()
    y_train_encoded = le.fit_transform(y_train.to_frame())
    y_test_encoded = le.transform(y_test.to_frame())



    xg_model = XGBRegressor(n_estimators=950, random_state=42)
    xg_model.fit(x_train_encoded, y_train_encoded)

    xg_pred = xg_model.predict(x_test_encoded)

    joblib.dump(xg_model,MODEL_FILE)
    joblib.dump(pipeline,PIPELINE_FILE)
    joblib.dump(le,OUTPUT_SCALER)


    xg_rsme = root_mean_squared_error(y_test_encoded,xg_pred)
    xg_mae = mean_absolute_error(y_test_encoded,xg_pred)
    xg_r2score = r2_score(y_test_encoded,xg_pred)

    n = x_test_encoded.shape[0]
    k = x_test_encoded.shape[1] 

    xg_r2score = r2_score(y_test_encoded, xg_pred)

    xg_adj_r2 = 1 - ((1 - xg_r2score) * (n - 1) / (n - k - 1))

    print(f"RMSE     : {xg_rsme:.4f}")
    print(f"MAE      : {xg_mae:.4f}")
    print(f"R² Score : {xg_r2score:.4f}")
    print(f"Adj R²   : {xg_adj_r2:.4f}")
    print(f"Congrats !! Your model is trained")
