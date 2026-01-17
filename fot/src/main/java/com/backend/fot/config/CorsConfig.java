package com.backend.fot.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

import java.util.Arrays;

/**
 * CORS (Cross-Origin Resource Sharing) configuration.
 * Allows frontend applications from different origins to access the API.
 * 
 * @author FlightOnTime Team
 * @version 1.0
 * @since 2025-12-18
 */
@Configuration
public class CorsConfig {

    /**
     * Configures CORS filter to allow cross-origin requests.
     * 
     * @return CorsFilter configured with allowed origins, methods, and headers
     */
    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        
        // Allow credentials (cookies, authorization headers)
        config.setAllowCredentials(true);
        
        // Allow specific origins (update for production)
        config.setAllowedOriginPatterns(Arrays.asList(
            "http://localhost:*",
            "http://127.0.0.1:*",
            "http://localhost:3000",
            "http://localhost:5500",
            "http://localhost:8080"
        ));
        
        // Allow all HTTP methods
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"));
        
        // Allow all headers
        config.setAllowedHeaders(Arrays.asList("*"));
        
        // Expose headers to the client
        config.setExposedHeaders(Arrays.asList("Authorization", "Content-Type"));
        
        // Max age for preflight requests (1 hour)
        config.setMaxAge(3600L);
        
        source.registerCorsConfiguration("/api/**", config);
        
        return new CorsFilter(source);
    }
}
