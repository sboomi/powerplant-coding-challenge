from imp import reload
import uvicorn


def start():
    uvicorn.run("powerplant_api.app.main:app", host="0.0.0.0", port=8888, reload=True)


if __name__ == "__main__":
    start()
