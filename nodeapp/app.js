const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const rootDir = require('./utils/path');

const adminRouter = require('./routes/admin')
const shopRouter = require('./routes/shop')


const app = express();

app.use(bodyParser.urlencoded())

app.use('/admin',adminRouter);
app.use(shopRouter);

app.use((req, res, next) => {
    res.status(404).sendFile(path.join(rootDir, 'views', '404.html'))
})


app.listen(3000)