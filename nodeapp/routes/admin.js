const express = require('express');
const router = express.Router();

router.get("/add-product", (req, res, next) => {
    res.send("<body><form action='/admin/add-product' method='post' ><input type='text' name='message'><button type'submit'>Add Product</button></input></form></body>")
})

router.post("/add-product", (req, res) => {
    console.log(req.body)
    res.redirect("/")
})

module.exports = router;