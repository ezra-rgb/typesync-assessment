import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { createProxyMiddleware } from 'http-proxy-middleware';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

const distPath = path.join(__dirname, 'dist');

// Parse JSON bodies FIRST
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// Serve static files
app.use(express.static(distPath));

// Proxy API requests with proper configuration
const backendUrl = process.env.BACKEND_URL || 'https://typesync-backend-ipca.onrender.com';

app.use('/api', createProxyMiddleware({
  target: backendUrl,
  changeOrigin: true,
  pathRewrite: { '^/api': '/api' },
  timeout: 30000, // 30 second timeout
  proxyTimeout: 30000,
  ws: true,
  logLevel: 'debug'
}));

// SPA fallback: serve index.html for all non-file, non-API requests
app.get(/^(?!.*\.)/, (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

const port = process.env.PORT || 10000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
