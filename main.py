from fastapi import FastAPI
import json

app = FastAPI()

def get_interactive_carrier_comparison(carriers):
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

@app.post("/interactive-comparison/")
def interactive_comparison(carriers: list):
    return get_interactive_carrier_comparison(carriers)

# Example usage in FastAPI:
# Run the app with `uvicorn your_script_name:app --reload`
