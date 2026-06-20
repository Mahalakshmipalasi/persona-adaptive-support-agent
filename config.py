import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurable Escalation parameters
RETRIEVAL_CONFIDENCE_THRESHOLD = 0.65  
MAX_TURNS_BEFORE_ESCALATION = 3