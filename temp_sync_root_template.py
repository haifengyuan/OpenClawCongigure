from pathlib import Path
import re

root = Path(r'C:/Users/1/.openclaw/workspace')
engine = root / 'kb/.ai-kb/cognition/Engine'
files = ['AGENTS.md','SOUL.md','TOOLS.md','HEARTBEAT.md','IDENTITY.md']

pat_locked = re.compile(r'<!-- LOCKED:START -->\n(.*?)\n<!-- LOCKED:END -->', re.S)
pat_template = re.compile(r'<!-- TEMPLATE:START -->\n(.*?)\n<!-- TEMPLATE:END -->', re.S)

def extract(text, pat):
    m = pat.search(text)
    return m.group(1).strip('\n') if m else ''

for name in files:
    root_path = root / name
    eng_path = engine / name
    root_text = root_path.read_text(encoding='utf-8', errors='replace')
    eng_text = eng_path.read_text(encoding='utf-8', errors='replace')

    if '<!-- TEMPLATE:START -->' in root_text:
        print(f'skip {name}: already has TEMPLATE')
        continue

    locked = extract(root_text, pat_locked) or extract(eng_text, pat_locked)
    template = extract(eng_text, pat_template)

    body = root_text
    body = re.sub(r'^<!-- LOCKED:START -->\n.*?\n<!-- LOCKED:END -->\n*', '', body, flags=re.S)
    body = body.lstrip('\n')

    parts = []
    if locked:
        parts.append('<!-- LOCKED:START -->\n' + locked + '\n<!-- LOCKED:END -->')
    if template:
        parts.append('<!-- TEMPLATE:START -->\n' + template + '\n<!-- TEMPLATE:END -->')
    if body.strip():
        parts.append(body.rstrip() + '\n')

    new_text = '\n\n'.join(parts).rstrip() + '\n'
    root_path.write_text(new_text, encoding='utf-8')
    print(f'updated {name}')
