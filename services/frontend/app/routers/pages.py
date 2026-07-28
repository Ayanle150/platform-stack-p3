import os
import httpx
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["pages"])

API_URL = os.getenv("API_URL", "http://api:8000")


@router.get("/", response_class=HTMLResponse)
async def index():
    items = []
    error = None
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{API_URL}/api/items")
            resp.raise_for_status()
            items = resp.json().get("items", [])
    except Exception as exc:
        error = str(exc)

    rows = "".join(
        f"<tr><td>{i['id']}</td><td>{i['name']}</td><td>${i['price']:.2f}</td></tr>"
        for i in items
    )
    error_block = f'<p class="error">API error: {error}</p>' if error else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Platform Stack</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }}
    h1 {{ color: #0078d4; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: .6rem 1rem; text-align: left; }}
    th {{ background: #0078d4; color: #fff; }}
    tr:nth-child(even) {{ background: #f5f5f5; }}
    .error {{ color: red; }}
  </style>
</head>
<body>
  <h1>Platform Stack P3</h1>
  <p>Henter data fra <code>{API_URL}</code></p>
  {error_block}
  <table>
    <thead><tr><th>ID</th><th>Navn</th><th>Pris</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <footer>Miljø: {os.getenv("ENVIRONMENT", "local")}</footer>
</body>
</html>"""
    return HTMLResponse(content=html)
