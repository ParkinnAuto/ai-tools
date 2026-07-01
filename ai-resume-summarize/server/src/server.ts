import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import analyzeRoutes from "./routes/analyzeRoutes";

dotenv.config()

const app = express();
const PORT = process.env.PORT || 5000;

// Connect with frontend
app.use(cors({
    origin:["http://localhost:8081"],
    methods:["GET", "POST"],
    credentials:true
}));

// Middleware
app.use(express.json());

// Routes
app.use("/api/analyze", analyzeRoutes)

// Test route
app.get("/", (req, res) => {
  res.json({ message: "CKQ server is running" });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});