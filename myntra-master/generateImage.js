import fs from "fs";
import axios from "axios";
import FormData from "form-data";
import express from "express";

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static("public"));

app.post("/generate-image", async (req, res) => {
  const { prompt } = req.body;
  const apiUrl = 'https://api.stability.ai/v2beta/stable-image/generate/ultra';
  const token = 'sk-FRAtrsTszUeVn8RJ7WovThvTLVfy7nYOPHtrOadmO3yyBVvK'; // Replace with your actual API token

  try {
    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('output_format', 'webp');

    const response = await axios.post(apiUrl, formData, {
      headers: {
        ...formData.getHeaders(),
        Authorization: `Bearer ${token}`,
        Accept: 'image/*',
      },
      responseType: 'arraybuffer'
    });

    if (response.status === 200) {
      const imageBuffer = Buffer.from(response.data);
      const imageName = `generated_image_${Date.now()}.webp`;
      fs.writeFileSync(`public/${imageName}`, imageBuffer);
      res.json({ imageUrl: `/${imageName}` });
    } else {
      throw new Error(`Failed to generate image: ${response.status}`);
    }
  } catch (error) {
    console.error('Error generating image:', error.message);
    res.status(500).json({ error: 'Failed to generate image. Please try again.' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

