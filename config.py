ASSISTANT_NAME = "stella"

OWNER = "Shikhar"

WAKE_WORDS = ["wake up", "hey stella", "stella"]

MIN_PYTHON = (3, 10)
MAX_PYTHON = (3, 11)

# Language settings
CURRENT_LANG = "en"

# Responses
RESPONSES = {
    "startup": "Stella is online and ready.",
    "stop": "Stopping Stella. Goodbye.",
    "hmm": "hmm?",
    "sleep_mode": "Computer is going to sleep mode.",
    "wake_up": "I am awake and ready.",
    "shutdown": "Your computer is shutting down.",
    "restart": "Your computer is restarting.",
    "unknown": "Sorry, I did not understand that.",
    "error": "Something went wrong. Please try again."
}

# Command keywords
COMMANDS_KEYWORDS = {
    "stop": ["stop"],
    "sleep": ["exit", "sleep"],
    "shutdown": ["shutdown"],
    "restart": ["restart"],
    "switch_hindi": [],
    "switch_english": ["switch to english", "english mode", "english"],
    "search": ["search", "find", "look up"],
    "open": ["open"],
    "play": ["play"]
}