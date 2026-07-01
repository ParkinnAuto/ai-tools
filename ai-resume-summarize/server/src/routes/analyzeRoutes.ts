import express from "express";
import { analyzeResume } from "../controllers/analyzeController";
import { upload } from "../middleware/uploadMiddleware";

const router = express.Router();

router.post("/", upload.single("resume"), analyzeResume);

export default router;