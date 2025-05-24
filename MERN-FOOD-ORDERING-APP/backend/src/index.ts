import express, { Request, Response } from "express";
import cors from "cors";
import "dotenv/config";
import mongoose from "mongoose";
import { auth } from "express-openid-connect";

const config = {
  authRequired: false,
  auth0Logout: true,
  baseURL: 'http://localhost:3000',
  clientID: '{yourClientId}',
  issuerBaseURL: 'https://{yourDomain}',
  secret: 'LONG_RANDOM_STRING'
};

mongoose.connect(process.env.MONGODB_CONNECTION_STRING as string).then(()=>{
  console.log("connected to database")
})
const app = express();

app.use(express.json());
app.use(cors());
app.use(auth(config));

app.get("/test", async (req: Request, res: Response) => {
  res.json({ message: "hello" });
});

app.listen(3000, () => {
  console.log("listening");
});
