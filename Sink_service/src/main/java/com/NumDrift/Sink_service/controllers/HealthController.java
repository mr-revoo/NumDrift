package com.NumDrift.Sink_service.controllers;

import com.NumDrift.Sink_service.services.UpdateNumber;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@RestController
public class HealthController {

    private final UpdateNumber updateNumber;

    @Autowired
    public HealthController(UpdateNumber updateNumber) {
        this.updateNumber = updateNumber;
    }

    @GetMapping("/health")
    public Map<String, Object> health() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "UP");
        response.put("message", "Sink Service is running");
        response.put("timestamp", System.currentTimeMillis());
        return response;
    }
    
    @GetMapping("/")
    public Map<String, Object> root() {
        Map<String, Object> response = new HashMap<>();
        response.put("service", "Sink Service");
        response.put("status", "Running");
        response.put("version", "1.0.0");
        return response;
    }

    @GetMapping("/additionResult")
    public Map<String, Object> getAdditionResult() throws IOException {
        Map<String, Object> response = new HashMap<>();
        try {
            int latestNumber = updateNumber.getLatestNumber();
            response.put("latestNumber", latestNumber);
            response.put("success", true);
        } catch (Exception e) {
            response.put("success", false);
            response.put("error", e.getMessage());
        }
        return response;
    }
} 