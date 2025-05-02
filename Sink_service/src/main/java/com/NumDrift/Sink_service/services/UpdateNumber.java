package com.NumDrift.Sink_service.services;

import org.springframework.stereotype.Service;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

@Service
public class UpdateNumber {
    private final FileReader fileReader;
    private final Lock lock = new ReentrantLock();

    public UpdateNumber() throws IOException {
        this.fileReader = new FileReader();
    }

    public void updateNumber(int number) throws IOException {
        lock.lock();
        try {
            int currentNumber = 0;
            if (fileReader.ensureFileExists()) {
                currentNumber = fileReader.readFile();
            }
            int newNumber = currentNumber + number;
            fileReader.writeFile(newNumber);
        } finally {
            lock.unlock();
        }
    }
    
    public int getLatestNumber() throws IOException {
        lock.lock();
        try {
            if (fileReader.ensureFileExists()) {
                return fileReader.readFile();
            }
            return 0; // Return default value if file doesn't exist
        } finally {
            lock.unlock();
        }
    }
}
