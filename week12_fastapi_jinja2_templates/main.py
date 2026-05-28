from pathlib import Path
from random import choice

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
except Exception:
    class HTMLResponse(str):
        pass

    class Request:
        pass

    class StaticFiles:
        def __init__(self, directory):
            self.directory = directory

    class FastAPI:
        def __init__(self):
            self.routes = {}

        def get(self, path, response_class=None):
            def decorator(func):
                self.routes[path] = func
                return func
            return decorator

        def mount(self, path, app, name=None):
            self.routes[path] = app

    class Jinja2Templates:
        def __init__(self, directory):
            self.directory = Path(directory)

        def TemplateResponse(self, request, name, context):
            return {"template": name, "context": context}


BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

PLAYLIST = [
    {"id": 1, "title": "Moonlight Sonata", "composer": "Beethoven", "period": "Classical", "duration": 17},
    {"id": 2, "title": "Spring", "composer": "Vivaldi", "period": "Baroque", "duration": 11},
    {"id": 3, "title": "Bolero", "composer": "Ravel", "period": "Modern", "duration": 15},
    {"id": 4, "title": "String Serenade", "composer": "Tchaikovsky", "period": "Romantic", "duration": 29},
]


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html lang="ko">
      <head><title>Classical Playlist</title></head>
      <body>
        <h1>Classical Playlist</h1>
        <p>FastAPI가 HTML 문자열을 직접 반환하는 첫 단계입니다.</p>
      </body>
    </html>
    """


@app.get("/now-playing", response_class=HTMLResponse)
def now_playing():
    piece = choice(PLAYLIST)
    return f"<h1>Now Playing</h1><p>{piece['title']} - {piece['composer']}</p>"


@app.get("/playlist", response_class=HTMLResponse)
def playlist(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="playlist.html",
        context={"playlist_name": "Classical Study List", "pieces": PLAYLIST, "featured_id": 1},
    )


@app.get("/piece/{piece_id}", response_class=HTMLResponse)
def piece_detail(request: Request, piece_id: int):
    piece = next((item for item in PLAYLIST if item["id"] == piece_id), None)
    return templates.TemplateResponse(
        request=request,
        name="piece.html",
        context={"piece": piece, "piece_id": piece_id},
    )
