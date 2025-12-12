// small helper functions used by frontend pages
async function getJSON(url){ return fetch(url).then(r=>r.json()); }

async function postJSON(url, body){
  const res = await fetch(url, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(body)
  });
  return res.json();
}
