const http = require('http')

const server = http.createServer((req, res) => {
    console.log(req.method, req.url, req.headers);

    res.setHeader('Content-Type', 'text/html')
    res.write('<html>')
    res.write('<div>hi</div>')
    res.write('<div>heloo</div>')
    res.write('</html>')
    res.end()
})

server.listen(3000)