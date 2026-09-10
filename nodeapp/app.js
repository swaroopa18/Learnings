const express = require('express');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.urlencoded())

app.use("/add-product", (req, res, next) => {
    res.send("<body><form action='/product' method='post' ><input type='text' name='message'><button type'submit'>Add Product</button></input></form></body>")
})

app.post("/product", (req, res) => {
    console.log(req.body)
    res.redirect("/")

})

app.use("/", (req, res, next) => {
    res.send("<h1>I am from expresss</h1>")
})

app.listen(3000)