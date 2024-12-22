import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import path from "path";
import dotenv from "dotenv";
import { createProxyMiddleware } from "http-proxy-middleware";
import morgan from 'morgan';

dotenv.config();
const app = express();

const corsConfig = {
  origin: process.env.REACT_APP_WEB_URL || 'https://hsense-insights.helixsense.com',
  credentials: true,
};

app.use(cors(corsConfig));

app.use((req, res, next) => {
  // set the CORS policy
  res.header("Access-Control-Allow-Origin", "*");
  // set the CORS headers
  res.header(
    "Access-Control-Allow-Headers",
    "origin, X-Requested-With,Content-Type,Accept, Authorization"
  );
  // set the CORS method headers
  if (req.method === "OPTIONS") {
    res.header("Access-Control-Allow-Methods", "GET PATCH DELETE POST");
    return res.status(200).json({});
  }
  next();
});

app.use(morgan("dev"));

// parse requests of content-type - application/json
app.use(bodyParser.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

const APIURL = process.env.API_URL || "https://api-mcloud.helixsense.com";
const BASEURL = process.env.BASE_URL || "https://api-mcloud.helixsense.com";
const IOTURL = process.env.IOT_URL || "https://api-dev.helixsense.com";
const PYTHON_API_URL = process.env.PYTHON_API_URL || "http://127.0.0.1:5000"; 
const SMART_PYTHON_API = process.env.SMART_PYTHON_API || "http://127.0.0.1:5002"; 
const AI_PYTHON_API = process.env.AI_PYTHON_API || "http://127.0.0.1:5001"; 
const SUSTAINABILITY_API = process.env.SUSTAINABILITY_API || "http://127.0.0.1:5003"; 
const EXPLAIN_AI = process.env.EXPLAIN_AI || "http://127.0.0.1:5004";
const AIR = process.env.AIR || "http://127.0.0.1:5010";
const ENERGY = process.env.ENERGY || "http://127.0.0.1:5011";

// responsible for account id authentication
app.use(
  '/api/authProviders/getByAccountId',
  createProxyMiddleware({
    target: BASEURL,
    changeOrigin: true,
  }),
);

app.use(
  '/api/authentication/oauth2/token',
  createProxyMiddleware({
    target: APIURL,
    changeOrigin: true,
  }),
);


app.use(
  '/api/v4/userinformation',
  createProxyMiddleware({
    target: APIURL,
    changeOrigin: true,
  }),
);

// Use distinct paths for the Python APIs to avoid conflicts
app.use(
  "/python_api", // Proxy route for Python API
  createProxyMiddleware({
    target: PYTHON_API_URL,
    changeOrigin: true,
    pathRewrite: {
      "^/python_api": "", // Strip the prefix from the forwarded path
    },
  })
);

app.use(
  "/sustainability_api", // Proxy route for Python API
  createProxyMiddleware({
    target: SUSTAINABILITY_API,
    changeOrigin: true,
    pathRewrite: {
      "^/sustainability_api": "", // Strip the prefix from the forwarded path
    },
  })
);
app.use(
  "/air", // Proxy route for Python API
  createProxyMiddleware({
    target: AIR,
    changeOrigin: true,
    logLevel: 'debug',
    pathRewrite: {
      "^/air": "", // Strip the prefix from the forwarded path
    },
  })
);

app.use(
  "/explain_ai", // Proxy route for Python API
  createProxyMiddleware({
    target: EXPLAIN_AI,
    changeOrigin: true,
    logLevel: 'debug',
    pathRewrite: {
      "^/explain_ai": "", // Strip the prefix from the forwarded path
    },
  })
);

app.use(
  "/api", // Proxy route for Smart Python API
  createProxyMiddleware({
    target: SMART_PYTHON_API,
    changeOrigin: true,
    pathRewrite: {
      "^/api": "", // Strip the prefix from the forwarded path
    },
  })
);

app.use('/aiassist', createProxyMiddleware({
  target: AI_PYTHON_API,
  changeOrigin: true,
  logLevel: 'debug',
  onProxyReq: (proxyReq, req, res) => {
    if (req.body) {
      let bodyData = JSON.stringify(req.body);
      proxyReq.setHeader('Content-Type', 'application/json');
      proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
      proxyReq.write(bodyData);
    }
  }
}));

app.use('/energy', createProxyMiddleware({
  target: ENERGY,
  changeOrigin: true,
  logLevel: 'debug',
  onProxyReq: (proxyReq, req, res) => {
    if (req.body) {
      let bodyData = JSON.stringify(req.body);
      proxyReq.setHeader('Content-Type', 'application/json');
      proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
      proxyReq.write(bodyData);
    }
  }
}));


const __dirname = path.resolve();
app.use("/static", express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.json({ message: "Welcome to HelixSense application." });
});

const PORT = process.env.PORT || 8081;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});