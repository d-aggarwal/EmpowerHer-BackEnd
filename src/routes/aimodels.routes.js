import { Router } from "express";
import fetch from "node-fetch"; // Make sure fetch is imported correctly
const API_URL = process.env.FLASK_API_URL;

const router = Router();

// Define the POST route for /api/generate-strategy
router.post("/generate-strategy", async (req, res) => {
  try {
    const response = await fetch(`${API_URL}/generate`, {
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

export default router;
