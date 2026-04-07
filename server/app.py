# server/app.py

import uvicorn


def main():
    """
    Entry point for OpenEnv multi-mode deployment.
    Starts FastAPI server.
    """
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )


# Required for script execution
if __name__ == "__main__":
    main()