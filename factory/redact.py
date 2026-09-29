import re

PATTERNS = [
    re.compile(r'(?i)(api[_-]?key|access[_-]?token|secret|password|private[_-]?key)\s*[:=]\s*[\"\']?[^\s,;\"\']{8,}'),
    re.compile(r'(?i)bearer\s+[A-Za-z0-9._~+/-]{16,}'),
    re.compile(r'(?i)sk-[A-Za-z0-9_-]{16,}'),
]


def redact(text: str) -> str:
    value = text
    for rx in PATTERNS:
        value = rx.sub(lambda m: m.group(0).split(':',1)[0] + ': [REDACTED]' if ':' in m.group(0) else '[REDACTED]', value)
    return value
