package com.NumDrift.Sink_service.services;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class FileReader {
    private static final String DIR_PATH = "./saveFile";
    private static final String FILE_PATH = DIR_PATH + File.separator + "save.txt";
    
    public FileReader() throws IOException {
        File dir = new File(DIR_PATH);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        
        File file = new File(FILE_PATH);
        if (!file.exists()) {
            file.createNewFile();
            writeFile(0);
        }
    }
    
    public Boolean ensureFileExists() {
        File file = new File(FILE_PATH);
        return file.exists();
    }

    public int readFile() {
        try {
            File file = new File(FILE_PATH);
            Scanner scanner = new Scanner(file);
            if (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                scanner.close();
                return Integer.parseInt(line);
            }
            scanner.close();
            return 0;
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public void writeFile(int data) throws IOException {
        String input = String.valueOf(data);
        FileWriter file = new FileWriter(FILE_PATH);
        file.write(input);
        file.close();
    }
}
