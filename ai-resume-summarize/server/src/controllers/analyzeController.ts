import { Request, Response } from "express";
import axios from "axios";
import FormData from "form-data";
import fs from "fs";

export const analyzeResume = async (req: Request, res: Response) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        message: "No file uploaded",
      });
    }

    const formData = new FormData();

    formData.append("file", fs.createReadStream(req.file.path), {
      filename: req.file.originalname,
      contentType: req.file.mimetype,
    });

    const aiResponse = await axios.post(
      "http://localhost:8000/analyze",
      formData,
      {
        headers: formData.getHeaders(),
      }
    );

    return res.json({
      message: "Resume analyzed successfully",
      file: {
        originalName: req.file.originalname,
        filename: req.file.filename,
        path: req.file.path,
        mimetype: req.file.mimetype,
        size: req.file.size,
      },
      textLength: aiResponse.data.textLength,
      extractedTextPreview: aiResponse.data.extractedTextPreview,
      analysis: aiResponse.data.analysis,
    });
  } catch (error: any) {
    return res.status(500).json({
      message: "Something went wrong while analyzing resume",
      error: error.message,
    });
  }
};