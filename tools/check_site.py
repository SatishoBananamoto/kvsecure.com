#!/usr/bin/env python3
"""Static checks for the kvsecure.com launch site."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = ["index.html", "guide.html", "faq.html", "feedback.html"]
REQUIRED_FILES = ["CNAME", "README.md", "styles.css", "site.js", "LICENSE", *HTML_FILES]
ALLOWED_EXTERNAL_HOSTS = {
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "github.com",
    "kvsecure.com",
    "pypi.org",
    "formsubmit.co",
}
BLOCKED_CLAIMS = [
    (re.compile(r"\bmilitary-grade\b", re.I), "avoid overstated encryption marketing"),
    (re.compile(r"\bagent never sees secrets?\b", re.I), "avoid absolute agent-secret claims"),
    (re.compile(r"\bsecret never enters the agent", re.I), "scope agent-process claims to brokered tools"),
    (re.compile(r"\bnever enters the agent", re.I), "avoid absolute agent-memory claims"),
    (re.compile(r"\bwithout ever\b", re.I), "qualify blanket without-ever claims"),
    (re.compile(r"\babsolute guarantee\b", re.I), "avoid absolute security guarantees"),
    (re.compile(r"\bsafe by default\b", re.I), "avoid broad default-safety claims"),
    (re.compile(r"\bsecure by default\b", re.I), "avoid broad default-safety claims"),
    (re.compile(r"\bteam sync is available\b", re.I), "team sync is not public production"),
    (re.compile(r"\bcloud sync is available\b", re.I), "cloud sync is not public production"),
    (re.compile(r"\b\$[0-9]+(?:/[a-z]+)?\b", re.I), "avoid fixed pricing claims"),
]
REQUIRED_PHRASES = [
    "Team/cloud sync is not a public production feature yet.",
    "Do not paste live secrets into this form.",
    "if you approve a command with selected secrets",
    "genuinely need environment variables",
]


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value for key, value in attrs}
        if attr.get("id"):
            self.ids.add(attr["id"] or "")
        for name in ("href", "src", "action"):
            value = attr.get(name)
            if value:
                self.links.append((name, value))


def local_target(link: str, current_file: str) -> tuple[str, str | None] | None:
    if link.startswith("#"):
        return current_file, link[1:] or None
    if link.startswith("/#"):
        return "index.html", link[2:] or None
    if link == "/":
        return "index.html", None
    if link.startswith("/"):
        link = link[1:]
    if "#" in link:
        path, anchor = link.split("#", 1)
        return (path or current_file), anchor or None
    if "://" not in link and not link.startswith("mailto:"):
        return link, None
    return None


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            failures.append(f"missing required file: {rel}")

    cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    if cname != "kvsecure.com":
        failures.append(f"CNAME should be kvsecure.com, got {cname!r}")

    parsers: dict[str, SiteParser] = {}
    combined_text = []
    for rel in HTML_FILES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        parser = SiteParser()
        try:
            parser.feed(text)
        except Exception as exc:  # pragma: no cover - defensive parser guard
            failures.append(f"{rel}: HTML parser failed: {exc}")
        parsers[rel] = parser
        combined_text.append(text)

    all_text = "\n".join(combined_text + [(ROOT / "README.md").read_text(encoding="utf-8")])
    for regex, reason in BLOCKED_CLAIMS:
        match = regex.search(all_text)
        if match:
            failures.append(f"blocked claim ({reason}): {match.group(0)!r}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in all_text:
            failures.append(f"missing required boundary phrase: {phrase}")

    for current_file, parser in parsers.items():
        for attr, link in parser.links:
            if link.startswith("data:"):
                continue
            parsed = urlparse(link)
            if parsed.scheme in {"http", "https"}:
                if parsed.hostname not in ALLOWED_EXTERNAL_HOSTS:
                    failures.append(f"{current_file}: unexpected external {attr}: {link}")
                continue
            if parsed.scheme and parsed.scheme != "mailto":
                failures.append(f"{current_file}: unexpected link scheme in {attr}: {link}")
                continue

            target = local_target(link, current_file)
            if not target:
                continue
            rel, anchor = target
            if rel in {"styles.css", "site.js"}:
                if not (ROOT / rel).exists():
                    failures.append(f"{current_file}: missing asset {rel}")
                continue
            if rel == "":
                rel = current_file
            target_path = ROOT / rel
            if not target_path.exists():
                failures.append(f"{current_file}: broken local {attr}: {link}")
                continue
            if anchor and rel in parsers and anchor not in parsers[rel].ids:
                failures.append(f"{current_file}: missing anchor {link}")

    if failures:
        print("site check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"site check: OK ({len(HTML_FILES)} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
