from pathlib import Path

IGNORED_PARTS = {'.git','.factory','node_modules','.wrangler','__pycache__','.pytest_cache','.mypy_cache','.factory_quarantine'}


def safe_path(root: Path, relative: str) -> Path:
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError(f'Unsafe path: {relative}')
    resolved = (root / p).resolve()
    root_resolved = root.resolve()
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise ValueError(f'Path escapes workspace: {relative}')
    return resolved


def should_skip(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)
