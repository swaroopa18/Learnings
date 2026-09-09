const http = require('http')

const server = http.createServer((req, res) => {
    if (req.url === '/') {
        res.write('<html>')
        res.write('<div>hi</div>')
        res.write('<body><form action="/message" method="post" ><input type="text" name="message"><button type"submit">submit</button></input></form></body>')
        res.write('</html>')
        return res.end()
    }
    res.setHeader('Content-Type', 'text/html')
    res.write('<html>')
    res.write('<div>hi</div>')
    res.write('<div>heloo</div>')
    res.write('</html>')
    res.end()
})

server.listen(3000)