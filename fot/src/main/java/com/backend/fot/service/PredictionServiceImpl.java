package com.backend.fot.service;

import com.backend.fot.client.MLServiceClient;
import com.backend.fot.dto.FlightPredictionRequestDTO;
import com.backend.fot.dto.FlightPredictionResponseDTO;
import com.backend.fot.dto.MLServiceResponseDTO;
import com.backend.fot.enums.FlightPrediction;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;

/**
 * Implementation of PredictionService for flight delay predictions.
 * Integrates with Flask ML Wrapper service for ML-based predictions.
 * 
 * @author FlightOnTime Team
 * @version 2.0
 * @since 2025-12-17
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class PredictionServiceImpl implements PredictionService {

    private final MLServiceClient mlServiceClient;

    /**
     * Predicts flight delay using ML service.
     * 
     * @param request Flight information
     * @return Prediction with delay status and probability
     */
    @Override
    public FlightPredictionResponseDTO predictDelay(FlightPredictionRequestDTO request) {
        log.info("Processing prediction for flight {}", request.getFlightNumber());

        try {
            // Call Flask ML Wrapper
            MLServiceResponseDTO mlResponse = mlServiceClient.predict(request);
            
            // Convert ML service response to API response
            FlightPrediction prediction = mlResponse.getPredictionEnum();
            BigDecimal probability = mlResponse.getConfidence();
            
            log.info("Prediction result from ML service: {} with probability {}", 
                    prediction, probability);

            return FlightPredictionResponseDTO.builder()
                    .prediction(prediction)
                    .probability(probability.doubleValue())
                    .confidence(determineConfidenceLevel(probability.doubleValue()))
                    .build();
                    
        } catch (MLServiceClient.MLServiceException e) {
            log.error("ML service error for flight {}: {}", 
                    request.getFlightNumber(), e.getMessage());
            throw new RuntimeException("Failed to get prediction from ML service", e);
        }
    }

    /**
     * Determines confidence level based on probability.
     * 
     * @param probability Prediction probability
     * @return Confidence level enum
     */
    private FlightPredictionResponseDTO.ConfidenceLevel determineConfidenceLevel(Double probability) {
        if (probability >= 0.90) {
            return FlightPredictionResponseDTO.ConfidenceLevel.VERY_HIGH;
        } else if (probability >= 0.75) {
            return FlightPredictionResponseDTO.ConfidenceLevel.HIGH;
        } else if (probability >= 0.60) {
            return FlightPredictionResponseDTO.ConfidenceLevel.MEDIUM;
        } else if (probability >= 0.45) {
            return FlightPredictionResponseDTO.ConfidenceLevel.LOW;
        } else {
            return FlightPredictionResponseDTO.ConfidenceLevel.VERY_LOW;
        }
    }
}
