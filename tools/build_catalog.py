"""Re-embeds the catalogue list from tools/catalog.json into index.html.

Run this after editing tools/catalog.json:

    python3 tools/build_catalog.py

It regenerates the filter buttons (with per-category counts) and the
#catalog-data JSON block. Item names/descriptions live in the JSON, so the
page never needs hand editing for a new garment. Existing markup is replaced
in place, so an already-edited index.html keeps its own content.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
CATALOG = ROOT / "tools" / "catalog.json"

GROUPS = {"blazer": ("Blazers", "ব্লেজার"),
          "shirt": ("Shirts", "শার্ট"),
          "pants": ("Trousers", "ট্রাউজার"),
          "suit": ("Suits", "স্যুট")}

FIELDS = ("file", "cat", "en", "bn", "en_desc", "bn_desc")


def main() -> None:
    items = json.loads(CATALOG.read_text(encoding="utf-8"))
    unknown = {i["cat"] for i in items} - set(GROUPS)
    if unknown:
        raise SystemExit(f"Unknown category in catalog.json: {sorted(unknown)}")

    html = INDEX.read_text(encoding="utf-8")

    # --- filters -------------------------------------------------------
    buttons = [f'<button class="cat-filter active" data-cat="all" aria-pressed="true">'
               f'<span class="lbl" data-en="Everything" data-bn="সবকিছু">Everything</span>'
               f'<i class="cnt">{len(items)}</i></button>']
    for key, (en, bn) in GROUPS.items():
        n = sum(1 for i in items if i["cat"] == key)
        buttons.append(f'<button class="cat-filter" data-cat="{key}" aria-pressed="false">'
                       f'<span class="lbl" data-en="{en}" data-bn="{bn}">{en}</span>'
                       f'<i class="cnt">{n}</i></button>')
    html, n_filters = re.subn(
        r'(<div class="cat-filters"[^>]*>)(.*?)(</div>)',
        lambda m: m.group(1) + "".join(buttons) + m.group(3),
        html, flags=re.S)
    if not n_filters:
        raise SystemExit("Could not find the .cat-filters block in index.html")

    # --- embedded item data -------------------------------------------
    data = [{k: i[k] for k in FIELDS} for i in items]
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html, n_data = re.subn(
        r'(<script id="catalog-data" type="application/json">)(.*?)(</script>)',
        lambda m: m.group(1) + payload + m.group(3),
        html, flags=re.S)
    if not n_data:
        raise SystemExit("Could not find #catalog-data in index.html")

    INDEX.write_text(html, encoding="utf-8")
    print(f"index.html updated: {len(items)} items, {len(buttons)} filters")


if __name__ == "__main__":
    main()
