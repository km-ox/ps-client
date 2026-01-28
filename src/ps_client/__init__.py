def hello() -> str:
    return "Hello from ps-client!"


from .client import ConfigClient

__all__ = ["ConfigClient"]
__version__ = "0.2.0"
