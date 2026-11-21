# -*- coding: utf-8 -*-
"""Build the alternative design versions (v2/ ... v6/) from the root pages.

Version 1 is the site at the root of the folder. The text lives ONLY there:
edit the root pages, then run

    python tools/build_versions.py

to copy the text into the other versions. Each version reuses css/site.css and
adds its own stylesheet (css/v2.css ... css/v6.css), so the wording is always
identical and only the presentation changes.

The script also writes css/themes.css from tools/themes.py (five colour themes
per version) and (re)inserts the small "Version / Theme" switcher in every page.
Once a version and a theme are chosen, the rest can be deleted.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from themes import THEMES, css as themes_css  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index", "research", "projects", "outreach"]
VERSIONS = [2, 3, 4, 5, 6]
# Versions 2 to 6 are kept (and still rebuilt) but no longer listed on the pages of version 1.
# Set to True to get the "Version" row back, or open v2/index.html ... v6/index.html directly.
SHOW_VERSIONS = False
# Designs for the top of the Research, Projects and Outreach pages, under review in version 1.
HEADS = ["1", "2", "3", "4", "5"]

G = "https://fonts.googleapis.com/css2?"
FONTS = {
    2: G + "family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap",
    3: G + "family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Geist:wght@500&display=swap",
    4: G + "family=Poppins:wght@400;500;600&family=Geist+Mono:wght@400;500&family=Geist:wght@500&display=swap",
    5: G + "family=Plus+Jakarta+Sans:wght@400;500;600&family=Geist:wght@500&display=swap",
    6: G + "family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif&family=Geist:wght@500&display=swap",
}
HTML_ATTRS = {3: ' data-motion="off"'}   # extra attributes on <html>
SCRIPTS = {2: "v2.js"}                   # optional extra script

# Version 5: a cover above the profile (video on the home page, a picture elsewhere).
COVER_VIDEO = ("aacoma-draping-2", "Two robots draping a composite fabric in the lab.")
COVER_IMG = {"research": "servoing-trajectories.jpg", "projects": "aacoma-cell-2.jpg", "outreach": "ai4work-2.jpg"}
# Version 6: one cover picture per page in the fixed side panel.
PANEL_IMG = {"index": "sawyer-cable-1.jpg", "research": "servoing-trajectories.jpg",
             "projects": "kuka-draping-2.jpg", "outreach": "sawyer-competition-4.jpg"}

SWITCH_RE = re.compile(r"\s*<!-- versions:start.*?versions:end -->", re.S)
INIT_RE = re.compile(r"\s*<script data-theme-init>.*?</script>", re.S)
DIR_SCRIPT_RE = re.compile(r"\s*<script>\s*/\* review only: restore the chosen direction.*?</script>", re.S)
DIRS_RE = re.compile(r"\s*<!-- review only: remove once a direction is chosen -->\s*<div class=\"dirs\".*?</div>", re.S)

SWITCH_STYLE = (
    "<style>.versions{position:fixed;left:16px;bottom:16px;z-index:70;display:grid;gap:2px;padding:4px;"
    "background:#111;color:#fff;border:1px solid #313131;border-radius:12px;"
    "font:500 12px/16px Geist,system-ui,sans-serif;letter-spacing:0;text-transform:none}"
    ".versions .vrow{display:flex;align-items:center;gap:2px}"
    ".versions .vlabel{width:56px;padding:0 8px;opacity:.6}"
    ".versions a{display:block;padding:6px 10px;border-radius:8px;color:#fff;text-decoration:none;box-shadow:none}"
    ".versions a:hover{background:#2a2a2a}"
    '.versions a[aria-current="true"]{background:#fff;color:#111}'
    ".versions button{width:22px;height:22px;margin:3px;padding:0;border-radius:50%;cursor:pointer;"
    "border:2px solid #555;background:radial-gradient(circle,var(--a) 0 36%,var(--b) 40%)}"
    '.versions button[aria-pressed="true"]{border-color:#fff}'
    ".versions .vname{padding:0 8px;opacity:.75;white-space:nowrap}"
    "@media(max-width:480px){.versions .vname{display:none}}</style>"
)


def read(path):
    return io.open(path, encoding="utf-8").read()


def write(path, text):
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)


def switcher(page, current):
    rows = ""
    if current != 1 or SHOW_VERSIONS:
        links = []
        for v in [1] + VERSIONS:
            if current == 1:
                href = "%s.html" % page if v == 1 else "v%d/%s.html" % (v, page)
            else:
                href = "../%s.html" % page if v == 1 else "../v%d/%s.html" % (v, page)
            cur = ' aria-current="true"' if v == current else ""
            links.append('<a href="%s"%s>%d</a>' % (href, cur, v))
        rows += '<div class="vrow"><span class="vlabel">Version</span>' + "".join(links) + "</div>"
    if current == 1 and page != "index" and HEADS:
        rows += ('<div class="vrow"><span class="vlabel">Header</span>'
                 + "".join('<a href="#" data-head="%d">%s</a>' % (i, n) for i, n in enumerate(HEADS, 1))
                 + "</div>")
    dots = "".join(
        '<button type="button" data-theme="%d" data-name="%s" title="%s" aria-label="Theme %d: %s" style="--b:%s;--a:%s"></button>'
        % (i, t["name"], t["name"], i, t["name"], t["bg"], t["accent"])
        for i, t in enumerate(THEMES[current], 1))
    rows += '<div class="vrow"><span class="vlabel">Theme</span>' + dots + '<span class="vname"></span></div>'
    script = (
        '<script>(function(){var k="theme-v%d",r=document.documentElement,'
        'b=document.querySelectorAll(".versions [data-theme]"),n=document.querySelector(".versions .vname"),'
        'L=document.querySelectorAll(".versions [data-head]");'
        "function s(t){r.setAttribute(\"data-theme\",t);try{localStorage.setItem(k,t)}catch(e){}"
        "b.forEach(function(x){var on=x.dataset.theme===t;x.setAttribute(\"aria-pressed\",on);"
        "if(on&&n)n.textContent=t+\". \"+x.dataset.name})}"
        "function l(t){r.setAttribute(\"data-head\",t);try{localStorage.setItem(\"head-v1\",t)}catch(e){}"
        "L.forEach(function(x){x.setAttribute(\"aria-current\",x.dataset.head===t)})}"
        "b.forEach(function(x){x.addEventListener(\"click\",function(){s(x.dataset.theme)})});"
        "L.forEach(function(x){x.addEventListener(\"click\",function(e){e.preventDefault();l(x.dataset.head)})});"
        "if(L.length)l(r.getAttribute(\"data-head\")||\"1\");"
        's(r.getAttribute("data-theme")||"1")})();</script>' % current)
    return ("\n\n  <!-- versions:start (review only: delete this block once a header and a theme are chosen) -->\n  "
            + SWITCH_STYLE + '\n  <div class="versions" role="group" aria-label="Design preview">' + rows + "</div>\n  "
            + script + "\n  <!-- versions:end -->")


def theme_init(v):
    layout = ('var l=localStorage.getItem("head-v1");if(l)document.documentElement.setAttribute("data-head",l);'
              if v == 1 and HEADS else "")
    return ('\n  <script data-theme-init>try{var t=localStorage.getItem("theme-v%d");'
            'if(t)document.documentElement.setAttribute("data-theme",t);%s}catch(e){}</script>' % (v, layout))


def finish(html, page, v, css_prefix):
    """Things every page gets: theme stylesheet, theme restore, switcher."""
    html = SWITCH_RE.sub("", html)
    html = INIT_RE.sub("", html)
    html = DIR_SCRIPT_RE.sub("", html)   # the old "Direction" preview is replaced by the themes
    html = DIRS_RE.sub("", html)
    if "css/themes.css" not in html:
        html = re.sub(r'(<link rel="stylesheet" href="%scss/site\.css"\s*/?>)' % re.escape(css_prefix),
                      r'\1\n  <link rel="stylesheet" href="%scss/themes.css">' % css_prefix, html, count=1)
    i = html.index("</head>")
    html = html[:i].rstrip() + theme_init(v) + "\n" + html[i:]
    i = html.rindex("</body>")
    return html[:i].rstrip() + switcher(page, v) + "\n" + html[i:]


def socials(html):
    m = re.search(r'<div class="socials">.*?</div>', html, re.S)
    return m.group(0) if m else ""


def build(page, v, src):
    s = SWITCH_RE.sub("", src)
    s = INIT_RE.sub("", s)
    # the video behind the name belongs to version 1 only
    s = re.sub(r"\s*<!-- intro-bg:start.*?intro-bg:end -->", "", s, flags=re.S)
    s = s.replace('class="intro intro-video"', 'class="intro"')
    # so does the map of research interests: the other versions keep the plain list
    s = s.replace(' about-sec"', '"')
    # ... and so do the pictures of the header designs
    s = re.sub(r"\s*<!-- head-media:start.*?head-media:end -->", "", s, flags=re.S)
    s = s.replace('class="interests interests-map"', 'class="interests"')
    s = re.sub(r"<html lang=\"en\"[^>]*>",
               '<html lang="en" data-version="%d" data-page="%s"%s>' % (v, page, HTML_ATTRS.get(v, "")), s, count=1)
    # paths: the version lives one folder down
    s = re.sub(r'((?:src|href|poster|content)=")assets/', r"\1../assets/", s)
    s = re.sub(r'<link rel="stylesheet" href="css/themes\.css"\s*/?>\s*', "", s)
    s = re.sub(r'href="css/site\.css"\s*/?>',
               'href="../css/site.css">\n  <link rel="stylesheet" href="../css/v%d.css">' % v, s, count=1)
    extra = ('\n  <script src="../js/%s"></script>' % SCRIPTS[v]) if v in SCRIPTS else ""
    s = re.sub(r'<script src="js/site\.js"></script>', '<script src="../js/site.js"></script>' + extra, s, count=1)
    s = re.sub(r'https://fonts\.googleapis\.com/css2\?[^"]*', FONTS[v], s, count=1)

    if v == 2:
        # the side panel repeats the position and the profile links
        s = re.sub(r'(<a class="nav-name"[^>]*>.*?</a>)',
                   r'<div class="nav-id">\1<span class="nav-role">PhD Candidate in Robotics</span></div>',
                   s, count=1, flags=re.S)
        s = re.sub(r'(<button class="nav-toggle")',
                   '<div class="nav-extra">' + socials(src).replace('class="socials"', 'class="socials nav-socials"')
                   + "</div>\n    " + r"\1", s, count=1)

    if v == 5:
        if page == "index":
            name, label = COVER_VIDEO
            cover = ('<div class="wrap cover-wrap"><div class="cover">'
                     '<video data-autoplay muted loop playsinline preload="metadata" poster="../assets/video/%s.jpg" aria-label="%s">'
                     '<source src="../assets/video/%s.mp4" type="video/mp4"></video></div></div>\n      ' % (name, label, name))
            s = re.sub(r'(<section class="intro">\s*)', lambda m: m.group(1) + cover, s, count=1)
        else:
            cover = ('<div class="wrap cover-wrap"><div class="cover">'
                     '<img src="../assets/img/%s" alt=""></div></div>\n      ' % COVER_IMG[page])
            s = re.sub(r'(<header class="page-head">\s*)', lambda m: m.group(1) + cover, s, count=1)

    if v == 6:
        panel = '\n\n  <aside class="panel" aria-hidden="true"><img src="../assets/img/%s" alt=""></aside>' % PANEL_IMG[page]
        s = re.sub(r"(</nav>)", lambda m: m.group(1) + panel, s, count=1)

    s = s.replace("<!DOCTYPE html>",
                  "<!DOCTYPE html>\n<!-- GENERATED from ../%s.html by tools/build_versions.py."
                  " Edit the root page, then re-run the script. -->" % page, 1)
    return finish(s, page, v, "../")


def main():
    write(os.path.join(ROOT, "css", "themes.css"), themes_css())
    for page in PAGES:
        path = os.path.join(ROOT, page + ".html")
        src = read(path)
        for v in VERSIONS:
            out = os.path.join(ROOT, "v%d" % v)
            if not os.path.isdir(out):
                os.makedirs(out)
            write(os.path.join(out, page + ".html"), build(page, v, src))
        # The root pages (version 1) are final: a header and a theme were chosen, the
        # "versions" switcher was removed from them by hand, and it must not come back.
        # v2 ... v6 above stay archived and rebuildable, with their own switcher, for later review.
        print("built", page)


if __name__ == "__main__":
    main()
