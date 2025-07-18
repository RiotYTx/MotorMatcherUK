const express = require("express");
const { exec } = require("child_process");
const path = require("path");

const app = express();
const port = process.env.PORT || 3000;

app.use(express.static("public"));

// AI-powered prediction endpoint
app.get("/predict", (req, res) => {
  const { price, fuel, transmission, mileage, mpg, brand } = req.query;

  let command = `/home/runner/workspace/.pythonlibs/bin/python3 predict_model_with_brand_fixed.py price=${price} fuel=${fuel} transmission=${transmission} mileage=${mileage} mpg=${mpg}`;

  if (brand && brand.toLowerCase() !== "any") {
    command += ` brand=${brand}`;
  }

exec(command, (error, stdout, stderr) => {
  console.log("Running command:", command);
  console.log("stdout:", stdout);
  console.log("stderr:", stderr);

  if (error) {
    console.error("Prediction error:", stderr);
    return res.status(500).json({ error: "Prediction failed." });
  }

  const prediction = stdout.trim();
  res.json({ predictedModel: prediction });
});


// Start server
app.listen(port, () => {
  console.log(`✅ Server running at http://localhost:${port}`);
});
