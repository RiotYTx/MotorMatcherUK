const request = require("supertest");
const fs = require("fs");
const path = require("path");
const app = require("./server");

// Test CSV brand name
const TEST_BRAND = "TestBrand";
const TEST_CSV_PATH = path.join(__dirname, "..", "car_data", `${TEST_BRAND}.csv`);

beforeAll(() => {
  const csvData = `price,mileage,transmission,fuelType,tax,mpg,engineSize
8000,40000,manual,petrol,150,45.6,1.4
10000,30000,automatic,diesel,120,60.5,1.6`;

  // Ensure folder exists
  const dir = path.dirname(TEST_CSV_PATH);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir);

  fs.writeFileSync(TEST_CSV_PATH, csvData);
});

afterAll(() => {
  fs.unlinkSync(TEST_CSV_PATH);
});

describe("GET /cars", () => {
  it("returns 400 if model is missing", async () => {
    const res = await request(app).get("/cars");
    expect(res.statusCode).toBe(400);
    expect(res.body).toHaveProperty("error");
  });

  it("returns 404 if CSV doesn't exist", async () => {
    const res = await request(app).get("/cars?model=NoSuchModel");
    expect(res.statusCode).toBe(404);
    expect(res.body).toHaveProperty("error");
  });

  it("returns all cars with only model given", async () => {
    const res = await request(app).get(`/cars?model=${TEST_BRAND}`);
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body.length).toBe(2);
  });

  it("filters cars by fuel type", async () => {
    const res = await request(app).get(`/cars?model=${TEST_BRAND}&fuel=petrol`);
    expect(res.statusCode).toBe(200);
    expect(res.body.length).toBe(1);
    expect(res.body[0].fuelType.toLowerCase()).toBe("petrol");
  });

  it("filters cars by max price", async () => {
    const res = await request(app).get(`/cars?model=${TEST_BRAND}&price=9000`);
    expect(res.statusCode).toBe(200);
    expect(res.body.length).toBe(1);
    expect(Number(res.body[0].price)).toBeLessThanOrEqual(9000);
  });
});
