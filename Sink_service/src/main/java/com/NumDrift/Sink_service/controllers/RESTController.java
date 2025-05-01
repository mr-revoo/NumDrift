package com.NumDrift.Sink_service.controllers;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import com.NumDrift.Sink_service.services.FileReader;
import java.io.IOException;

@RestController
public class RESTController {
    private final FileReader fileReader;

    public RESTController() throws IOException {
        this.fileReader = new FileReader();
    }

    @GetMapping("/api/additionResult")
    public ResponseEntity<String> getResult() {
        int result = fileReader.readFile();
        return ResponseEntity.ok("The result is: " + result);
    }
}
