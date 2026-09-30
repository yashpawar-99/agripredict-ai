import pandas as pd
import numpy as np 
import joblib
import os 

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from sklearn.pipeline import Pipeline 
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder,StandardScaler
from sklearn.impute import SimpleImputer 

# Create a model and pipeline file 

MODEL_FILE = "model.pkl"
PIPELINE_FILE = "pipeline.pkl"
LABEL_ENCODE_OP = "label_encoder.pkl"

# a pipliene to process  a data 

def build_pipeline():
    
    num_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    cat_cols =  ['ph_category']

    num_pipeline = Pipeline(steps=[
        ("imputing",SimpleImputer(strategy="mean")),
        ("scaling", StandardScaler())
    ])

    cat_pipeline = Pipeline(steps=[
        ("imputing",SimpleImputer(strategy="most_frequent")),
        ("encoding",OneHotEncoder(handle_unknown='ignore'))
    ])

    final_pipeline = ColumnTransformer(transformers=[
        ("num cols",num_pipeline,num_cols),
        ("cat_cols",cat_pipeline,cat_cols)
    ])

    return final_pipeline


def crop_recomendation(n,p,k,ph,temp,humidity,rainfall):    
    #lets take the imput for model 

    #load  a train model and pipeline File 

    model = joblib.load(MODEL_FILE)
    pipeline = joblib.load(PIPELINE_FILE)
    output =  joblib.load(LABEL_ENCODE_OP)


    # ph_category feature engineer karna jaise notebook me kiya tha
    ph_bins = [0, 5.5, 6.5, 7.5, 8.5, 14]
    ph_labels = [
        "strongly_acidic",
        "moderately_acidic",
        "neutral",
        "alkaline",
        "strongly_alkaline",
    ]
    ph_cat = pd.cut([ph], bins=ph_bins, labels=ph_labels)[0]

    # DataFrame banana matching exact training columns
    input_data = pd.DataFrame(
        [
            {
                "N": n,
                "P": p,
                "K": k,
                "temperature": temp,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall,
                "ph_category": str(ph_cat),
            }
        ]
    )

    input_transform = pipeline.transform(input_data)
    input_pred = model.predict(input_transform)
    output_pred = output.inverse_transform(input_pred)

    return output_pred



if not os.path.exists(MODEL_FILE):

    #import file
    df = pd.read_csv("../data/Crop_recommendation.csv")

    #added a new feature 
    df['ph_category'] = pd.cut(
            df['ph'], 
            bins=[0, 5.5, 6.5, 7.5, 8.5, 14], 
            labels=['strongly_acidic', 'moderately_acidic', 'neutral', 'alkaline', 'strongly_alkaline']
    )

    #split the model 

    X = df.drop(columns=["label"])
    y = df["label"]

    x_train,x_test,y_train,y_test = train_test_split(X,y,
                                                    random_state=42,
                                                    test_size=0.20 )


    pipeline = build_pipeline()
    X_train_encoded = pipeline.fit_transform(x_train)
    X_test_encoded = pipeline.transform(x_test)

    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)
    y_test_encoded = le.transform(y_test)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_encoded, y_train_encoded)
    y_pred = model.predict(X_test_encoded)

    # Now save the model 

    joblib.dump(model,MODEL_FILE)
    joblib.dump(pipeline,PIPELINE_FILE)
    joblib.dump(le,LABEL_ENCODE_OP)


    acc = accuracy_score(y_test_encoded, y_pred)
    prec = precision_score(y_test_encoded, y_pred, average="weighted")
    rec = recall_score(y_test_encoded, y_pred, average="weighted")
    f1 = f1_score(y_test_encoded, y_pred, average="weighted")

    print(f"Accuracy : {acc}")
    print(f"Precision : {prec}")
    print(f"Recall : {rec}")
    print(f"f1 Score : {f1}")

