const express = require("express");
const csvParser = require("csv-parser");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3000;

app.use(express.static("public"));

app.get("/cars", async (req, res) => {
  const brand = req.query.model;
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
    .on("data", (data) => results.push(data))
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
