import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import fetch from 'node-fetch';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

const distPath = path.join(__dirname, 'dist');
app.use(express.static(distPath));

// Proxy API requests to backend
app.use('/api', async (req, res) => {
  const backendUrl = process.env.BACKEND_URL || 'https://typesync-backend-ipca.onrender.com';
  const targetUrl = `${backendUrl}${req.originalUrl}`;
  
  try {
    const response = await fetch(targetUrl, {
      method: req.method,
      headers: req.headers,
      body: req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body) : undefined,
    });
    
    const data = await response.text();
    res.status(response.status);
    Object.entries(response.headers.raw()).forEach(([key, val]) => {
      res.setHeader(key, val);
    });
    res.send(data);
  } catch (error) {
    res.status(500).json({ error: 'Backend request failed', details: error.message });
  }
});

// SPA fallback: serve index.html for all non-file, non-API requests
app.get(/^(?!.*\.)/, (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

const port = process.env.PORT || 10000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
