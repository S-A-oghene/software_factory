from pathlib import Path

PROTECTED = {
    '.git', '.factory/state.json', '.factory/policy.json',
    '.github/workflows/security.yml', 'SECURITY.md'
}


def is_protected(relative: str) -> bool:
    rel = Path(relative).as_posix().lstrip('/')
    if rel in PROTECTED:
        return True
    parts = Path(rel).parts
    return '.git' in parts


def validate_delete(relative: str, allow_protected=False):
    if not allow_protected and is_protected(relative):
        raise PermissionError(f'Protected path: {relative}')


def validate_patch_size(patch: str, max_added=2500, max_removed=2500, max_files=40):
    files=[]; adds=removes=0
    if len(patch) > 400_000:
        raise PermissionError('Patch too large')
    for line in patch.splitlines():
        if line.startswith('+++ b/'):
            files.append(line[6:].strip())
        elif line.startswith('+') and not line.startswith('+++'):
            adds += 1
        elif line.startswith('-') and not line.startswith('---'):
            removes += 1
    for f in files:
        if is_protected(f):
            raise PermissionError(f'Protected path in patch: {f}')
    if adds > max_added or removes > max_removed or len(set(files)) > max_files:
        raise PermissionError('Patch exceeds bounded mutation policy')
    return True
