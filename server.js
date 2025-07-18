const express = require("express");
const { exec } = require("child_process");
const path = require("path");

const app = express();
const port = process.env.PORT || 3000;

app.use(express.static("public"));

// AI-powered prediction endpoint
app.get("/predict", (req, res) => {
  const { price, fuel, transmission, mileage, mpg, engineSize } = req.query;

  // Default fallback values if not provided
  const command = `python3 predict_model_with_brand_fixed.py price=${price} fuel=${fuel} transmission=${transmission} mileage=${mileage} mpg=${mpg} engineSize=${engineSize}`;

exec(command, (error, stdout, stderr) => {
  console.log("Running command:", command);
  console.log("stdout:", JSON.stringify(stdout));
  console.log("stderr:", JSON.stringify(stderr));

  if (error || stderr) {
    console.error("Prediction error:", stderr || error.message);
    return res.status(500).json({ error: "Prediction failed." });
  }

  const prediction = stdout.trim();
  if (!prediction) {
    console.warn("No prediction returned.");
    return res.status(500).json({ error: "No prediction received from model." });
  }

  res.json({ predictedModel: prediction });
});
});

// Start server
app.listen(port, () => {
  console.log(`✅ Server running at http://localhost:${port}`);
});

module.exports = app;
