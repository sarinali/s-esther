# Claude Code Rules

## Backend Development Standards

### Code Comments
- **NO comments explaining WHAT code does** - code should be self-explanatory
- **ONLY comments explaining WHY something happens** - business logic, complex decisions, or non-obvious reasoning
- Avoid obvious comments like `# increment counter` or `# check if user exists`

### Import Organization
Always organize imports in this exact order:

```python
import os
import sys
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from constants.chat_models import ChatRequest
from services.openai_service import OpenAIInferenceService
```

**Import Structure:**
1. Standard library imports (`import ...`)
2. Third-party imports (`from ... import ...`)
3. Local imports (`from constants...`, `from services...`)

### Service Pattern
- **Always use singleton pattern for services**
- Create service instances at the module level (after imports)
- Example:

```python
# services/openai_service.py
class OpenAIInferenceService:
    def __init__(self):
        # initialization code
    
    def process_request(self, data):
        # service logic

# At the end of the file, create singleton instance
service = OpenAIInferenceService()
```

### Constants Organization

#### AI Prompts
- **All AI prompts MUST be located in the `constants/` folder**
- Create dedicated files for prompt categories (e.g., `prompts.py`, `system_prompts.py`)
- Use descriptive variable names for prompts

```python
# constants/prompts.py
CHAT_SYSTEM_PROMPT = """
You are a helpful assistant that...
"""

SUMMARIZATION_PROMPT = """
Please summarize the following text...
"""
```

#### API Schema Definitions
- **All API schema definitions MUST be in the `constants/` folder**
- Organize schemas by route/feature in corresponding files
- For `/chat` routes, create schemas in `constants/chat_models.py`
- For `/user` routes, create schemas in `constants/user_models.py`
- Use descriptive file names that match the route structure

```python
# constants/chat_models.py
from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str
```

### File Structure Guidelines
```
backend/
├── constants/
│   ├── chat_models.py      # Chat-related schemas
│   ├── user_models.py      # User-related schemas
│   ├── prompts.py          # AI prompts
│   └── system_prompts.py   # System prompts
├── services/
│   ├── openai_service.py   # Contains: service = OpenAIInferenceService()
│   └── database_service.py # Contains: service = DatabaseService()
├── routes/
│   ├── chat.py            # Uses constants.chat_models
│   └── user.py            # Uses constants.user_models
└── main.py
```

### Additional Standards
- Use type hints for all function parameters and return values
- Follow PEP 8 naming conventions
- Keep functions focused and single-purpose
- Use dependency injection for service dependencies
- Always validate input data using Pydantic models
- Handle errors gracefully with appropriate HTTP status codes

### Example Service Implementation
```python
# services/example_service.py
from typing import Dict, Any
from constants.prompts import CHAT_SYSTEM_PROMPT

class ExampleService:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
    
    def process_data(self, data: Dict[str, Any]) -> str:
        # No comments needed - method name and type hints are self-explanatory
        return self._transform_data(data)
    
    def _transform_data(self, data: Dict[str, Any]) -> str:
        # Private method implementation
        pass

# Singleton instance
service = ExampleService()
```

This structure ensures consistency, maintainability, and clear separation of concerns across the backend codebase.
