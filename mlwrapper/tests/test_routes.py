import pytest
from app import create_app
from unittest.mock import patch, MagicMock


@pytest.fixture
def app():
    """Create test Flask application"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestPredictEndpoint:
    """Tests for /predict endpoint"""

    def test_predict_success(self, client):
        """Test successful prediction"""

        mock_response = {
            "prediction": 1,
            "probability": 0.85
        }

        with patch('app.routes.prediction_routes.ml_client.predict') as mock_predict:
            mock_predict.return_value = mock_response

            response = client.post('/predict', json={
                "flightNumber": "AA1234",
                "companyName": "AA",
                "flightOrigin": "JFK",
                "flightDestination": "LAX",
                "flightDepartureDate": "2025-12-20T14:30:00",
                "flightDistance": 3974
            })

            assert response.status_code == 200
            data = response.get_json()
            assert data['prediction'] == 1
            assert data['probability'] == 0.85

    def test_predict_empty_body(self, client):
        """Test prediction with empty request body"""

        response = client.post('/predict', json=None)

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_predict_invalid_data(self, client):
        """Test prediction with invalid data"""

        response = client.post('/predict', json={
            "flightNumber": "A",  # Too short
            "companyName": "AA",
            "flightOrigin": "JFK",
            "flightDestination": "LAX",
            "flightDepartureDate": "2025-12-20T14:30:00",
            "flightDistance": 3974
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_predict_negative_distance(self, client):
        """Test prediction with negative distance"""

        response = client.post('/predict', json={
            "flightNumber": "AA1234",
            "companyName": "AA",
            "flightOrigin": "JFK",
            "flightDestination": "LAX",
            "flightDepartureDate": "2025-12-20T14:30:00",
            "flightDistance": -100
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_predict_ml_service_error(self, client):
        """Test prediction when ML service fails"""

        with patch('app.routes.prediction_routes.ml_client.predict') as mock_predict:
            mock_predict.side_effect = Exception("ML service unavailable")

            response = client.post('/predict', json={
                "flightNumber": "AA1234",
                "companyName": "AA",
                "flightOrigin": "JFK",
                "flightDestination": "LAX",
                "flightDepartureDate": "2025-12-20T14:30:00",
                "flightDistance": 3974
            })

            assert response.status_code == 500
            data = response.get_json()
            assert 'error' in data

    def test_predict_uppercase_conversion(self, client):
        """Test that airport codes are converted to uppercase"""

        mock_response = {
            "prediction": 0,
            "probability": 0.92
        }

        with patch('app.routes.prediction_routes.ml_client.predict') as mock_predict:
            mock_predict.return_value = mock_response

            response = client.post('/predict', json={
                "flightNumber": "AA1234",
                "companyName": "aa",  # lowercase
                "flightOrigin": "jfk",  # lowercase
                "flightDestination": "lax",  # lowercase
                "flightDepartureDate": "2025-12-20T14:30:00",
                "flightDistance": 3974
            })

            assert response.status_code == 200
            # Verify that the mock was called with uppercase codes
            called_data = mock_predict.call_args[0][0]
            assert called_data['companyName'] == 'AA'
            assert called_data['flightOrigin'] == 'JFK'
            assert called_data['flightDestination'] == 'LAX'


class TestHealthEndpoint:
    """Tests for /health endpoint"""

    def test_health_check_success(self, client):
        """Test health check when ML service is UP"""

        mock_status = {
            "status": "UP",
            "ml_service": "OK"
        }

        with patch('app.routes.prediction_routes.ml_client.health_check') as mock_health:
            mock_health.return_value = mock_status

            response = client.get('/health')

            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'UP'
            assert data['service'] == 'Flask ML Wrapper'

    def test_health_check_degraded(self, client):
        """Test health check when ML service is DOWN"""

        mock_status = {
            "status": "DOWN",
            "ml_service": "Connection refused"
        }

        with patch('app.routes.prediction_routes.ml_client.health_check') as mock_health:
            mock_health.return_value = mock_status

            response = client.get('/health')

            assert response.status_code == 503
            data = response.get_json()
            assert data['status'] == 'DEGRADED'

    def test_health_check_exception(self, client):
        """Test health check when an exception occurs"""

        with patch('app.routes.prediction_routes.ml_client.health_check') as mock_health:
            mock_health.side_effect = Exception("Unexpected error")

            response = client.get('/health')

            assert response.status_code == 503
            data = response.get_json()
            assert data['status'] == 'DOWN'
            assert 'error' in data
