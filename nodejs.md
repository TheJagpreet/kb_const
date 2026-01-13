# Node.js Domain Knowledge

## Overview
Node.js is a JavaScript runtime built on Chrome's V8 engine, allowing server-side JavaScript execution. It's event-driven and non-blocking, ideal for scalable network applications.

## Key Concepts
- **Event Loop**: Handles asynchronous operations efficiently.
- **Modules**: Use CommonJS (require/module.exports) or ES6 modules (import/export).
- **NPM**: Node Package Manager for installing and managing dependencies.
- **Streams**: Handle large data efficiently with readable/writable streams.
- **Express.js**: Popular framework for building web applications and APIs.

## Best Practices
- Use async/await for handling promises.
- Implement error handling with try/catch and middleware.
- Follow modular architecture for maintainable code.
- Use environment variables for configuration.
- Monitor performance with tools like PM2.

## Example
```javascript
const express = require('express');
const app = express();

app.get('/api', (req, res) => {
  res.json({ message: 'Hello from Node.js!' });
});

app.listen(3000, () => console.log('Server running on port 3000'));
```