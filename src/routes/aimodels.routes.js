import { Router } from "express";
import fetch from "node-fetch"; // Make sure fetch is imported correctly
const API_URL_S = process.env.FLASK_API_URL_STRATEGY;
const API_URL_B = process.env.FLASK_API_URL_BUSSI;
const API_URL_N = process.env.FLASK_API_URL_NAME;
const API_URL_T = process.env.FLASK_API_URL_TIME;



const router = Router();

// Define the POST route for /api/generate-strategy
router.post("/generate-strategy", async (req, res) => {
  // console.log("Hello from expresssssssssssssssssssssssssssssssssssss");
  try {
    // console.log("Hello from expresssssssssssssssssssssssssssssssssssss");
    const response = await fetch(`${API_URL_S}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Error:", err);
    console.log("error from express", err)
    res.status(500).json({ success: false, error: "Server error" });
  }
  // console.log("Hello from expresssssssssssssssssssssssssssssssssssss");
});

router.post("/businessplan", async (req, res) => {
  const FormData = req.body;

  if (!FormData) {
    return res.status(400).json({ message: "Form data is missing" });
  }

  try {
    const response = await fetch(`${API_URL_B}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Error:", err);
    res.status(500).json({ success: false, error: "Server error" });
  }
});

router.post("/generate-name", async (req, res) => {
  const FormData = req.body;

  if (!FormData) {
    return res.status(400).json({ message: "Form data is missing" });
  }

  try {
    const response = await fetch(`${API_URL_N}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Error:", err);
    res.status(500).json({ success: false, error: "Server error" });
  }
});

router.post("/generate-timeline", async (req, res) => {
  const business_idea = req.body;

  if (!business_idea) {
    return res.status(400).json({ message: "Business Idea is missing" });
  }

  try {
    const response = await fetch(`${API_URL_T}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });
    
    const data = await response.json();
    console.log(data);
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Error:", err);
    res.status(500).json({ success: false, error: "Server error" });
  }
});

export default router;
