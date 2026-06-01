import importlib.util
import os
import sys
from pathlib import Path


os.environ["TAVILY_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

MOCK_PROVIDER_PATH = Path(__file__).parent / "mocks" / "mock_provider.py"
spec = importlib.util.spec_from_file_location(
    "tests.mocks.mock_provider",
    MOCK_PROVIDER_PATH,
)
assert spec is not None
assert spec.loader is not None
mock_provider = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mock_provider)
sys.modules["research_agent.providers.mock_provider"] = mock_provider
