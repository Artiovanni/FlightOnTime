package com.backend.fot.client;

import com.backend.fot.dto.FlightPredictionRequestDTO;
import com.backend.fot.dto.MLServiceResponseDTO;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

/**
 * HTTP client for communication with Flask ML Wrapper service.
 * 
 * @author FlightOnTime Team
 * @version 1.0
 * @since 2025-12-21
 */
@Slf4j
@Component
public class MLServiceClient {

    private final RestTemplate restTemplate;
    private final String mlServiceUrl;
    private final Duration timeout;

    public MLServiceClient(
            RestTemplate restTemplate,
            @Value("${ml.service.url:http://localhost:5000/predict}") String mlServiceUrl,
            @Value("${ml.service.timeout:5000}") long timeoutMs) {
        this.restTemplate = restTemplate;
        this.mlServiceUrl = mlServiceUrl;
        this.timeout = Duration.ofMillis(timeoutMs);
        
        log.info("MLServiceClient initialized with URL: {}", mlServiceUrl);
        log.info("MLServiceClient timeout set to: {}ms", timeoutMs);
    }

    /**
     * Sends flight data to Flask ML Wrapper for prediction.
     * 
     * @param request Flight prediction request
     * @return ML service response with prediction and probability
     * @throws MLServiceException if communication fails
     */
    public MLServiceResponseDTO predict(FlightPredictionRequestDTO request) {
        log.info("Sending prediction request to ML service for flight: {}", request.getFlightNumber());
        
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<FlightPredictionRequestDTO> entity = new HttpEntity<>(request, headers);
            
            log.debug("Calling ML service at: {}", mlServiceUrl);
            ResponseEntity<MLServiceResponseDTO> response = restTemplate.postForEntity(
                    mlServiceUrl,
                    entity,
                    MLServiceResponseDTO.class
            );
            
            MLServiceResponseDTO result = response.getBody();
            
            if (result == null) {
                log.error("ML service returned null response");
                throw new MLServiceException("ML service returned empty response");
            }
            
            log.info("Received prediction from ML service: prediction={}, probability={}", 
                    result.getPrediction(), result.getConfidence());
            
            return result;
            
        } catch (RestClientException e) {
            log.error("Error communicating with ML service: {}", e.getMessage(), e);
            throw new MLServiceException("Failed to communicate with ML service: " + e.getMessage(), e);
        }
    }

    /**
     * Checks if ML service is available.
     * 
     * @return true if service is reachable, false otherwise
     */
    public boolean isServiceAvailable() {
        try {
            String healthUrl = mlServiceUrl.replace("/predict", "/health");
            log.debug("Checking ML service health at: {}", healthUrl);
            
            ResponseEntity<String> response = restTemplate.getForEntity(healthUrl, String.class);
            boolean available = response.getStatusCode().is2xxSuccessful();
            
            log.info("ML service health check result: {}", available ? "UP" : "DOWN");
            return available;
            
        } catch (Exception e) {
            log.warn("ML service health check failed: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Custom exception for ML service communication errors.
     */
    public static class MLServiceException extends RuntimeException {
        public MLServiceException(String message) {
            super(message);
        }

        public MLServiceException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}
