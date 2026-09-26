from fastapi import FastAPI
from fastapi.responses import JSONResponse
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

tier_1_cities = ["Mumbai", "Delhi", "Banglore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = ["Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodra", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijaywada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"]


'''now we will make a pydantic model to validate the incoming data:'''

#step 1: we will create a class 'UserInput' jo ki BaseModel se inherit karegi.:
class UserInput(BaseModel): #now isme total 7 fields hongi.... fir hame isme thode discription and validation add karne hai jo ki ham typing modele ke annotated se karenge 
    age: Annotated[int, Field(..., gt=0, lt=120, description= 'Age of the user')] #this will be an integer... and field function ko call karke ham required (...) kar denge for the input... and fir validation add kar denge of gt=0, lt=120... then we can also add description just like i did.
    weight:Annotated[float, Field(..., gt=0, description= 'Weight of the user')]
    height:Annotated[float, Field(..., gt=0, lt=2.5, description= 'Height of the user')]
    income_lpa:Annotated[float, Field(..., gt=0, description= 'Annual Salary of the user in lpa')]
    smoker:Annotated[bool, Field(..., description= 'Is user a smoker')]
    city:Annotated[str, Field(..., description= 'Residing City of the user')]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description= 'Occupation of the user')] #Literal is used when we want to add options to choose from

    #now mujhe above features se new features banane hai i.e for eg. height and weight se mujhe bmi banana hai to mai use karunga computed fields ka just like:
    @computed_field
    @property
    #now we will create a new function by the name of bmi:
    def bmi(self) -> float: #isme hame ek self object mil raha hai and jo palat ke mil raha hai i.e a float, and ye function mujhe return kar raha hai:
        return self.weight/(self.height**2)
    #Ye ban gayi hamari first computed field.

    #now we will create another computed field by the name lifestyle risk:
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    #Ye ban gayi hamari lifestyle risk computed field

    #Now we will create another computed field by the name age group:
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age <25:
            return "Young"
        elif self.age < 45:
            return "Adult"
        elif self.age < 60:
            return "Middle Aged"
        else:
            return "Senior"
    #ye ban gayi hamari age group ki computed field.

    #Now we will create another computed field named city tier:
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in 'tier_1_cities':
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

    #Computed fields can be said as features that we add, and this as a whole is called feature engineering.

'''Pydantic model to ban gaya
Now we will create our predict endpoint'''

#Sabse pehle ham ek route create karnge i.e the predict route:
@app.post('/predict')
def predict_premium(data: UserInput): #yaha pe ek function create kiya by the name of predict_premium... isko input me user ka data milega by the name 'data'... aur ye 'data' kis type ka hoga? ye hamare UserInput type ka object hoga jo hamara pydantic model hai. 
#To hame request body se data aayega, vo seedha chala jayega hamare pydantic model ke paas i.e UserInput. Hamara pydantic model then usko validate karega, computed fields nikalega AUR FIR vo palat ke hame 'data' ke form me mil jayega.

    '''now that hamara model load ho chuka hai, ab hame ek proper input format create karna hai... aur hame ek row ka data pass karna hai hamarae model me... aur ye input pandas dataframe ke format me bheja jayega kyuki jo ML model hai jo rando forest model hai vo panda dataframe object ke oopar train hua hai  '''

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }]) #now we will create a panda dataframe jisme ki ham bas ek row rakhenge and usme ham ek dictionary pass karenge... in sakbo ek variable me store kar lenge by the name input_df.
    #ye ban gaya hamara input jo ham apne ml model ke paas bhejenge.

    #ab hame predicton karna hai toh:

    prediction = model.predict(input_df)[0]#oopar hamne jo model import kiya hai uske predict function ko call karenge...fir usme ham pass kar denge 'input_df'... fir isse palat ke hame list me ek output milega... aur hame uss list ka 0th item chahiye hoga... aur yahi hoga hamara 'prediction'... aur isi prediction ko hame json ke format me return karna hai... for this we will use fastapi.responses se jsonresponse

    return JSONResponse(status_code= 200, content={'predicted_category': prediction})

'''THAT'S IT, THIS IS OUR ML MODEL '''
