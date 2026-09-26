from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle 
import pandas as pd

#importing the ml model
with open('model.pkl', 'rb') as f: #means we are opening the file in read binary mode
    model = pickle.load(f)
    # iss step me hamne model import kar liya hai

#now we will create a fast api app object

app = FastAPI()

#now we will make a pydantic model to validate the incoming data:
#step 1: we will create a class 'UserInput' jo ki BaseModel se inherit karegi.:
class UserInput(BaseModel): #now isme total 7 fields hongi.... fir hame isme thode discription and validation add karne hai jo ki ham typing modele ke annotated se karenge 
    age: Annotated[int, Field(..., gt=0, lt=120, description= 'Age of the user')] #this will be an integer... and field function ko call karke ham required (...) kar denge for the input... and fir validation add kar denge of gt=0, lt=120... then we can also add description just like i did.
    weight:
    height:
    income_lpa:
    smoker:
    city:
    occupation: