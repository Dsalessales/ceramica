// Servidor local para testar o site como no GitHub Pages.
// Uso: node server.js   ->   http://localhost:8080/ceramica/
const http = require('http'), fs = require('fs'), path = require('path');
const root = __dirname, port = process.env.PORT || 8080, BASE = '/ceramica';
const types = {
  '.html': 'text/html; charset=utf-8', '.mjs': 'text/javascript', '.js': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif',
  '.gif': 'image/gif', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.ico': 'image/x-icon',
};
const dec = s => { try { return decodeURIComponent(s); } catch (e) { return s; } };
function send(res, f, code) {
  res.writeHead(code || 200, { 'Content-Type': types[path.extname(f).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}
http.createServer((req, res) => {
  let p = req.url.split('?')[0].split('#')[0];
  if (p === '/' || p === BASE) { res.writeHead(302, { Location: BASE + '/' }); return res.end(); }
  if (p.startsWith(BASE + '/')) p = p.slice(BASE.length);
  if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
  const cands = p === '/' ? ['/index.html'] : [p, p + '.html', p + '/index.html'];
  for (const c of cands) for (const v of [c, dec(c)]) {
    const f = path.join(root, v);
    if (!f.startsWith(root)) continue;
    try { if (fs.statSync(f).isFile()) return send(res, f); } catch (e) {}
  }
  res.writeHead(404); res.end('Not found');
}).listen(port, () => console.log(`Site rodando em http://localhost:${port}${BASE}/`));
