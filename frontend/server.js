const express = require('express');
const path = require('path');
const app = express();

const distPath = path.join(__dirname, 'dist');
app.use(express.static(distPath));

// SPA fallback: serve index.html for all non-asset routes
app.get('*', (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

const port = process.env.PORT || 10000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
