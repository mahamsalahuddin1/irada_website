import os
from waitress import serve
from app import app
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[waitress] Serving http://127.0.0.1:{port}  (Ctrl+C to stop)")
    serve(app, host="127.0.0.1", port=port, threads=8)
