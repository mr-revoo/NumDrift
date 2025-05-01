package com.NumDrift.Sink_service.services;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

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
}
