from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import json

# Initialize OpenAI API with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Load this from environment variables or set it directly.

app = FastAPI()

# Pydantic model for the carrier rate comparison request
class CarrierRateRequest(BaseModel):
    carriers: list
    years: int = 4

# Function to call the OpenAI Chat API to generate carrier rate comparison data
def get_carrier_rate_comparison(carriers, years=4):
    prompt = f"""Generate comparison data for the following carriers: {', '.join(carriers)}.
    For each carrier, provide:
    - Onboarding Time (in days)
    - Tracking Capabilities (Advanced, Intermediate, or Basic)
    - Sustainability Score (0-100)
    
    Return the data as a JSON string with this structure:
    {{  
      "data": [
        {{
            "name": "UPS",
            "onboardingTime": 2,
            "trackingCapabilities": "Advanced",
            "sustainabilityScore": 85
        }},
        ...
      ]
    }}

    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format = { "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates realistic shipping carrier data."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)

@app.post("/carrier-rate-comparison/")
async def carrier_rate_comparison(request: CarrierRateRequest):
    # Call the function to get the carrier rate comparison data
    rate_comparison_data = get_carrier_rate_comparison(request.carriers, request.years)
    
    # Return the response data
    return rate_comparison_data

@app.get("/")
def read_root():
    return {"message": "Welcome to the Carrier Rate Comparison API!"}
