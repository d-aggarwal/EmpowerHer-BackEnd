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

router.post("/businessplan", async (req, res) => {
  const FormData = req.body;

  if (!FormData) {
    return res.status(400).json({ message: "Form data is missing" });
  }

  try {
    const response = await fetch(`${API_URL}/plangenerate`, {
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
    const response = await fetch(`${API_URL}/namegenerate`, {
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
    const response = await fetch(`${API_URL}/timelinegenerate`, {
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
