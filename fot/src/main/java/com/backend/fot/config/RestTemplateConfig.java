package com.backend.fot.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

/**
 * Configuration for RestTemplate used in HTTP client communications.
 * 
 * @author FlightOnTime Team
 * @version 1.0
 * @since 2025-12-21
 */
@Configuration
public class RestTemplateConfig {

    @Value("${ml.service.timeout:5000}")
    private long timeoutMs;

    /**
     * Creates a configured RestTemplate bean with timeout settings.
     * 
     * @param builder RestTemplate builder
     * @return Configured RestTemplate instance
     */
    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder
                .setConnectTimeout(Duration.ofMillis(timeoutMs))
                .setReadTimeout(Duration.ofMillis(timeoutMs))
                .build();
    }
}
