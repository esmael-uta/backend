from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from TradeShield.settings import GOOGLE_CLOUD_PROJECT

@api_view(['POST'])
@permission_classes([AllowAny])
def get_supply_chain_routes(request):
    try:
        data = request.data
        origin_country = data.get('origin_country')
        destination_country = data.get('destination_country')

        if not origin_country or not destination_country:
            return Response({"error": "Origin and destination countries are required"}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"Provide real-time supply chain routes from {origin_country} to {destination_country}. Include ports, transit points, and modes of transport (e.g., sea, air). Return as a JSON list of routes."

        # Authenticate with service account
        credentials = service_account.Credentials.from_service_account_file(
            'C:/Users/smrc/Documents/GitHub/backend/apac-hackathon-780ca74cf792.json',  # Path to your service account JSON file
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        credentials.refresh(Request())
        access_token = credentials.token

        # Use the correct endpoint for Gemini's generateContent method
        api_endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{GOOGLE_CLOUD_PROJECT}/locations/us-central1/publishers/google/models/gemini-1.5-flash:generateContent"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
            }
        }
        response = requests.post(api_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        gemini_response = response.json()
        
        # Extract the generated content
        routes_text = gemini_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        # Parse the text into a JSON-like structure if needed
        if routes_text:
            routes = [{"route": route.strip()} for route in routes_text.split("\n") if route.strip()]
        else:
            routes = []

        from .models import SupplyChainRoute
        SupplyChainRoute.objects.create(
            origin_country=origin_country,
            destination_country=destination_country,
            route_details=routes
        )

        return Response({"routes": routes}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        