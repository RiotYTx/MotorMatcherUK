const express = require("express");
const csvParser = require("csv-parser");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3000;

app.use(express.static("public"));

// Utility function to sanitize and parse price/mileage
const parsePrice = (price) => {
  if (price) {
    return parseFloat(price.replace(/[^0-9.-]+/g, "")); // Removes currency symbols, commas
  }
  return NaN; // Return NaN if no price provided
};

const parseMileage = (mileage) => {
  return parseFloat(mileage) || 0; // Convert to a number, fallback to 0
};

app.get("/cars", async (req, res) => {
  const brand = req.query.model;
  const transmission = req.query.transmission;
  const price = req.query.price;
  const mileage = req.query.mileage;

  if (!brand) {
    return res.status(400).json({ error: "Model (brand) is required" });
  }

  const filePath = path.join(__dirname, "car_data", `${brand}.csv`);
  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: "CSV file not found" });
  }

  const results = [];
  console.log('Request received with parameters:', req.query);

  fs.createReadStream(filePath)
    .pipe(csvParser())
    .on("data", (data) => {
      // Parse car data
      const carPrice = parsePrice(data.price); // Sanitize and parse price
      const carMileage = parseMileage(data.mileage); // Sanitize and parse mileage

      // Log the car data to see what we're working with
      console.log(`Checking car: ${data.model}, Price: ${carPrice}, Mileage: ${carMileage}`);

      const maxPrice = parsePrice(price);
      const maxMileage = parseMileage(mileage);

      // Apply filters
      if (
        (transmission && !data.transmission.toLowerCase().includes(transmission.toLowerCase())) || // Case-insensitive partial matching for transmission type
        (price && carPrice > maxPrice) || // Check if car's price is greater than max price
        (mileage && carMileage > maxMileage) // Check if car's mileage is greater than max mileage
      ) {
        console.log('Car filtered out');
        return; // Skip this car if it doesn't match
      }

      console.log('Car added to results');
      results.push(data); // Add the car to the results if it passes all filters
    })
    .on("end", () => {
      console.log(`Found ${results.length} cars matching the filters`);
      res.json(results); // Return the filtered results
    })
    .on("error", (err) => {
      console.error("CSV Read Error:", err);
      res.status(500).json({ error: "Error reading CSV" });
    });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
