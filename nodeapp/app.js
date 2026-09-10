const http = require('http');
const express = require('express');

const app = express();

app.use((req, res, next) => {
    console.log("I am in middleware");
    next(); // Allow the request to continue to next middleware
})

app.use((req, res, next) => {
    console.log("I am in another middleware")
})

const server = http.createServer(app)

server.listen(3000)