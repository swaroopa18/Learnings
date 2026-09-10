const fs = require("fs")

const requestHandler = (req, res) => {
    const url = req.url
    const method = req.method

    if (url === '/') {
        res.write('<html>')
        res.write('<div>hi</div>')
        res.write('<body><form action="/message" method="post" ><input type="text" name="message"><button type"submit">submit</button></input></form></body>')
        res.write('</html>')
        return res.end()
    } else if (url == '/message' && method == "POST") {
        const body = []
        req.on("data", (chunk) => {
            body.push(chunk)
        })
        return req.on("end", () => {
            const parseBody = Buffer.concat(body).toString();
            const message = parseBody.split("=")[1]
            fs.writeFile("message.text", message, () => {
                res.statusCode = 302
                res.setHeader('Location', '/')
                return res.end()
            })
        })
    }
    res.setHeader('Content-Type', 'text/html')
    res.write('<html>')
    res.write('<div>hi</div>')
    res.write('<div>heloo</div>')
    res.write('</html>')
    res.end()
}

module.exports = requestHandler