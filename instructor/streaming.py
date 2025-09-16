"""
Basic streaming example that demonstrates real-time structured data extraction.

Input data sources: User prompt asking for person profile extraction
Output destinations: Console output with streaming JSON responses
Dependencies: OpenAI API key, instructor, openai, pydantic packages
Key exports: Address, Person models for structured extraction
Side effects: Makes OpenAI API calls, prints streaming output to console
"""

import json
import sys
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from instructor.core.client import instructor

load_dotenv()


class Address(BaseModel):
    """Address model for person location data."""

    street: str
    city: str
    state: str
    zip_code: str


class Person(BaseModel):
    """Person model with name, age, and address information."""

    name: str
    age: int
    addresses: List[Address]


# Create an instructor-patched client
client = instructor.from_openai(OpenAI())

# Stream the response as it's being generated
stream = client.chat.completions.create_partial(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {
            "role": "user",
            "content": "Extract a detailed person profile for John Smith, 35, "
            "who lives in Chicago and Springfield.",
        }
    ],
)

print("Streaming response...\n")

for partial in stream:
    if partial:
        # Clear the screen and move cursor to top
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

        print("🔄 Extracting structured data...\n")

        # Pretty print the current state
        partial_dict = partial.model_dump()
        print(json.dumps(partial_dict, indent=2, default=str))

        print(f"\n{'='*50}")
        print("Press Ctrl+C to stop")

        sys.stdout.flush()
