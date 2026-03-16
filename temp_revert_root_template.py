from pathlib import Path
import re

root = Path(r'C:/Users/1/.openclaw/workspace')
files = ['AGENTS.md','SOUL.md','TOOLS.md','HEARTBEAT.md','IDENTITY.md']
pat = re.compile(r'\n?<!-- TEMPLATE:START -->\n.*?\n<!-- TEMPLATE:END -->\n?', re.S)
for name in files:
    p = root / name
    text = p.read_text(encoding='utf-8', errors='replace')
    new = pat.sub('\n', text).strip() + '\n'
    p.write_text(new, encoding='utf-8')
    print(f'reverted {name}')
