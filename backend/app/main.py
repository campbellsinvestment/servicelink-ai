from fastapi import FastAPI

app = FastAPI(
    title="ServiceLink AI",
    description=(
        "An independent research-software prototype for normalizing "
        "community-service data and linking it to social-platform posts."
    ),
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return basic application information."""
    return {
        "name": "ServiceLink AI",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the health status of the API."""
    return {"status": "healthy"}