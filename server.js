const express = require("express");
const csvParser = require("csv-parser");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3000;

app.use(express.static("public"));

const parseNumber = (value) => {
  if (!value) return NaN;
  return parseFloat(value.toString().replace(/[^0-9.]/g, "")) || NaN;
};

app.get("/cars", async (req, res) => {
  const brand = req.query.model;
  const transmissionFilter = req.query.transmission?.toLowerCase();
  const fuelFilter = req.query.fuel?.toLowerCase();
  const maxPrice = parseNumber(req.query.price);
  const maxMileage = parseNumber(req.query.mileage);
  const maxTax = parseNumber(req.query.tax);
  const minMpg = parseNumber(req.query.mpg);
  const maxEngineSize = parseNumber(req.query.engineSize);

  if (!brand) {
    return res.status(400).json({ error: "Model (brand) is required" });
  }

  const filePath = path.join(__dirname, "car_data", `${brand}.csv`);
  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: "CSV file not found" });
  }

  const results = [];

  fs.createReadStream(filePath)
    .pipe(csvParser())
    .on("data", (car) => {
      const carPrice = parseNumber(car.price);
      const carMileage = parseNumber(car.mileage);
      const carTransmission = car.transmission?.toLowerCase() || "";
      const carFuel = car.fuelType?.toLowerCase() || "";
      const carTax = parseNumber(car.tax);
      const carMpg = parseNumber(car.mpg);
      const carEngineSize = parseNumber(car.engineSize);

      const matchesTransmission = !transmissionFilter || carTransmission.includes(transmissionFilter);
      const matchesFuel = !fuelFilter || carFuel.includes(fuelFilter);
      const matchesPrice = isNaN(maxPrice) || carPrice <= maxPrice;
      const matchesMileage = isNaN(maxMileage) || carMileage <= maxMileage;
      const matchesTax = isNaN(maxTax) || carTax <= maxTax;
      const matchesMpg = isNaN(minMpg) || carMpg >= minMpg;
      const matchesEngineSize = isNaN(maxEngineSize) || carEngineSize <= maxEngineSize;

      if (matchesTransmission && matchesFuel && matchesPrice && matchesMileage && matchesTax && matchesMpg && matchesEngineSize) {
        results.push(car);
      }
    })
    .on("end", () => {
      res.json(results);
    })
    .on("error", (err) => {
      console.error("CSV Read Error:", err);
      res.status(500).json({ error: "Error reading CSV" });
    });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
}

module.exports = app;