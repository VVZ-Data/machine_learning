import json, re, os

notebooks = [f for f in os.listdir('.') if f.endswith('.ipynb')]
print(f"Notebooks trouves : {len(notebooks)}")
print()

patterns = [
    r'read_csv\(["\']([^"\']+)["\']',
    r'open\(["\']([^"\']+)["\']',
    r'Document\(["\']([^"\']+)["\']',
    r'read_index\(["\']([^"\']+)["\']',
    r'["\']([^"\']*[.](csv|xlsx|docx|faiss|txt|json|pkl|joblib))["\']',
]

for nb_file in sorted(notebooks):
    with open(nb_file, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    refs = set()
    for cell in nb['cells']:
        src = ''.join(cell['source'])
        for pat in patterns:
            for m in re.findall(pat, src):
                ref = m if isinstance(m, str) else m[0]
                if ref.startswith('http'):
                    continue
                is_abs = (':\\' in ref) or (':/' in ref) or ref.startswith('//')
                if is_abs:
                    refs.add('ABSOLUTE:' + ref)
                else:
                    refs.add(ref)
    if refs:
        print(f"[{nb_file}]")
        for r in sorted(refs):
            clean = r.replace("ABSOLUTE:", "")
            if r.startswith("ABSOLUTE:"):
                tag = " [ABSOLUTE!]"
            elif os.path.exists(clean):
                tag = " [EXISTS]"
            else:
                tag = " [MISSING]"
            print(f"  -> {r}{tag}")
        print()
