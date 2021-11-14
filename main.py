import fastapi
import fastapi.staticfiles
import fastapi.responses
import fastapi.exceptions
import urllib.parse
import pathlib
import routers.api.v1

app = fastapi.FastAPI()
app.include_router(routers.api.v1.router)


@app.get("/{path:path}", include_in_schema=False)
async def subdir(request: fastapi.Request, path: str):
    try:
        if path != "/" and len(urllib.parse.urlparse(path).path.split('/')[-1].split(".")) == 1:
            if pathlib.Path(f"content/{path}").exists():
                return fastapi.responses.FileResponse(f"content/{path}/index.html")
            else:
                raise fastapi.HTTPException(status_code=404, detail="Not Found")
        else:
            if pathlib.Path(f"content/{path}").exists():
                return fastapi.responses.FileResponse(f"content/{path}")
            else:
                raise fastapi.HTTPException(status_code=404, detail="Not Found")
    except RuntimeError:
        raise fastapi.HTTPException(status_code=404, detail="Not Found")


@app.get("/", response_class=fastapi.responses.FileResponse, include_in_schema=False)
async def root():
    return fastapi.responses.FileResponse("content/index.html")


@app.get("/{path}/", response_class=fastapi.responses.RedirectResponse, include_in_schema=False)
async def redirect(path):
    return fastapi.responses.RedirectResponse(f"/{path}")

