from flask import Blueprint, request, jsonify
from app.services.ml_client import get_ml_client
from pydantic import BaseModel, Field, ValidationError, field_validator
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('predictions', __name__)

# Client for external ML service
ml_client = get_ml_client()


class FlightPredictionRequest(BaseModel):
    """Pydantic model for request validation"""

    flightNumber: str = Field(..., min_length=2, max_length=10)
    companyName: str = Field(..., min_length=2, max_length=3)
    flightOrigin: str = Field(..., min_length=3, max_length=3)
    flightDestination: str = Field(..., min_length=3, max_length=3)
    flightDepartureDate: str = Field(...)
    flightDistance: int = Field(..., gt=0)

    @field_validator('flightOrigin', 'flightDestination', 'companyName')
    @classmethod
    def uppercase_codes(cls, v: str) -> str:
        """Convert codes to uppercase"""
        return v.upper() if v else v


@bp.route('/predict', methods=['POST'])
def predict():
    """
    Main endpoint for flight delay prediction

    This endpoint is called by the Java API (MLServiceClient).
    Acts as wrapper/adapter between the Java API and the external ML service.

    Request Body (format received from Java API):
    {
        "flightNumber": "AA1234",
        "companyName": "AA",
        "flightOrigin": "JFK",
        "flightDestination": "LAX",
        "flightDepartureDate": "2025-12-20T14:30:00",
        "flightDistance": 3974
    }

    Response (format expected by Java API):
    {
        "prediction": 1,        # 0 = ON_TIME, 1 = DELAYED
        "confidence": 0.85      # Prediction confidence (0.0 - 1.0)
    }
    """

    try:
        # 1. Receive flight data from Java API
        flight_data = request.get_json()

        if not flight_data:
            return jsonify({
                "error": "Empty request body"
            }), 400

        logger.info(
            f"Request received from Java API: {flight_data.get('flightNumber')}")

        # 2. Validate input data (optional but recommended)
        validated_data = FlightPredictionRequest(**flight_data)

        # 3. Forward to external ML service
        logger.info("Forwarding to external ML service...")
        ml_result = ml_client.predict(validated_data.model_dump())

        # 4. Map ML service response to Java API format
        # ML service returns: {"prediction": 0/1, "probability": 0.85}
        # Java API expects: {"prediction": 0/1, "confidence": 0.85}
        response = {
            "prediction": ml_result.get("prediction"),
            "confidence": ml_result.get("probability")  # Map probability -> confidence
        }

        # 5. Return result in format expected by Java API
        logger.info(f"Returning result to Java API: {response}")
        return jsonify(response), 200

    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({
            "error": "Invalid data",
            "details": e.errors()
        }), 400

    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({
            "error": "Integration wrapper error",
            "message": str(e)
        }), 500


@bp.route('/health', methods=['GET'])
def health():
    """
    Integration wrapper health check

    Checks if:
    1. Flask API is working
    2. External ML service is accessible
    """

    try:
        # Check ML service status
        ml_status = ml_client.health_check()

        wrapper_status = "UP" if ml_status.get(
            "status") == "UP" else "DEGRADED"

        return jsonify({
            "status": wrapper_status,
            "service": "Flask ML Wrapper",
            "ml_service": ml_status
        }), 200 if wrapper_status == "UP" else 503

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "DOWN",
            "error": str(e)
        }), 503
