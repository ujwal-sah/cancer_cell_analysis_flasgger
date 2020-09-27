# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 11:01:53 2020

@author: ujwal
"""

from flask import Flask, request
import pandas as pd
import pickle
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

pickle_in = open("svm_cancer_prediction.pkl", "rb")
classifier = pickle.load(pickle_in)

@app.route("/")
def welcome():
    return "Welcome All"

@app.route("/predict")
def predict_cancer():
    """We will analyse the features of a cell to predict whether it is malignant or benign
    This is using docstrings for specifications.
    ---
    parameters:
      - name: Clump
        in: query
        type: number
        required: true
      - name: UnifSize
        in: query
        type: number
        required: true
      - name: UnifShape
        in: query
        type: number
        required: true
      - name: MargAdh
        in: query
        type: number
        required: true
      - name: SingEpiSize
        in: query
        type: number
        required: true
      - name: BareNuc
        in: query
        type: number
        required: true
      - name: BlandChrom
        in: query
        type: number
        required: true
      - name: NormNucl
        in: query
        type: number
        required: true
      - name: Mit
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output value
    """
    
    Clump = request.args.get("Clump")
    UnifSize = request.args.get("UnifSize")
    UnifShape = request.args.get("UnifShape")
    MargAdh = request.args.get("MargAdh")
    SingEpiSize = request.args.get("SingEpiSize")
    BareNuc = request.args.get("BareNuc")
    BlandChrom = request.args.get("BlandChrom")
    NormNucl = request.args.get("NormNucl")
    Mit = request.args.get("Mit")
    prediction=classifier.predict([[Clump, UnifSize, UnifShape, MargAdh, SingEpiSize, BareNuc, BlandChrom, NormNucl, Mit]])
    return "The predicted value is" + str(prediction)

@app.route("/predict_file", methods = ["POST"])
def predict_cancer_file():
    """We will analyse the features of cells to predict whether they are malignant or benign
    This is using docstrings for specifications.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
    responses:
        200:
            description: The output value
    """
    
    df_test = pd.read_csv(request.files.get("file"))
    prediction = classifier.predict(df_test)
    return "The predicted values are" + str(list(prediction)) 

if __name__=="__main__":
    app.run()