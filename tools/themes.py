# -*- coding: utf-8 -*-
"""Colour themes: five per design version.

Theme 1 of each version is the version's own default palette (defined in its
stylesheet); it is listed here only so the switcher can show its swatch.
Themes 2 to 5 are written to css/themes.css by tools/build_versions.py.

Keys: bg, surface, surface2, text, muted, line, accent, on (text on accent),
dark (True for dark themes), head (optional heading gradient, from/to),
extra (optional version-specific variables).
"""

RED = "oklch(0.55 0.19 27)"
LIGHT_HEAD = ("#000000", "#666666")
DARK_HEAD = ("#FFFFFF", "#9B9B9B")


def light(name, bg, surface2, text, muted, line, accent, surface="#FFFFFF", on="#FFFFFF", **kw):
    d = dict(name=name, bg=bg, surface=surface, surface2=surface2, text=text, muted=muted, line=line,
             accent=accent, on=on, dark=False)
    d.update(kw)
    return d


def dark(name, bg, surface, surface2, text, muted, line, accent, on="#181818", **kw):
    d = dict(name=name, bg=bg, surface=surface, surface2=surface2, text=text, muted=muted, line=line,
             accent=accent, on=on, dark=True)
    d.update(kw)
    return d


THEMES = {
    # ---- Version 1, "Lab bench" ----
    1: [
        light("Paper and red", "#F6F3EE", "#ECE7DF", "#1A1917", "#6B665E", "#DDD6CB", RED, head=LIGHT_HEAD),
        light("Sand and forest", "#F4F1E8", "#E8E3D3", "#1B1F1A", "#5F665C", "#D8D3C2", "oklch(0.45 0.09 155)", head=LIGHT_HEAD),
        light("Mist and cobalt", "#F2F4F7", "#E4E8EE", "#131722", "#5A6272", "#D5DAE3", "oklch(0.5 0.17 258)", head=LIGHT_HEAD),
        light("Porcelain and teal", "#F7F8F8", "#E6EBEB", "#0F1717", "#566363", "#D6DEDE", "oklch(0.5 0.085 200)", head=LIGHT_HEAD),
        dark("Night and amber", "#181818", "#1F1F1F", "#272727", "#F4F4F4", "#A3A3A3", "#313131", "oklch(0.8 0.15 75)", head=DARK_HEAD),
    ],
    # ---- Version 2, "Control room" ----
    2: [
        dark("Graphite and amber", "#181818", "#1F1F1F", "#272727", "#F2F2F2", "#A6A6A6", "#313131", "oklch(0.82 0.15 78)", head=DARK_HEAD),
        dark("Graphite and cyan", "#181818", "#1F1F1F", "#272727", "#F2F2F2", "#A6A6A6", "#313131", "oklch(0.82 0.12 205)", head=DARK_HEAD),
        dark("Black and signal red", "#000000", "#181818", "#1F1F1F", "#F4F4F4", "#A3A3A3", "#272727", "oklch(0.68 0.2 27)", on="#000000",
             head=DARK_HEAD, extra={"side-bg": "#131209"}),
        dark("Olive night and lime", "#131209", "#1F1F1F", "#272727", "#F1F1EA", "#A9A99C", "#313131", "oklch(0.86 0.14 125)", on="#131209",
             head=DARK_HEAD),
        light("Daylight and burnt orange", "#F5F5F4", "#EAEAE8", "#161616", "#5C5C5C", "#D9D9D6", "oklch(0.55 0.17 45)",
              head=LIGHT_HEAD, extra={"side-bg": "#FFFFFF", "soft": "#3D3D3D"}),
    ],
    # ---- Version 3, "Manuscript" ----
    3: [
        light("White and blue ink", "#FFFFFF", "#F3F3F1", "#151515", "#4A4A4A", "#D9D9D6", "oklch(0.42 0.14 262)"),
        light("Ivory and oxblood", "#FBF8F1", "#F0EBDF", "#1C1917", "#57504A", "#DDD5C7", "oklch(0.42 0.13 20)", surface="#FBF8F1"),
        light("White and forest", "#FFFFFF", "#F1F3F0", "#141714", "#4A504A", "#D6DAD5", "oklch(0.4 0.09 155)"),
        light("Grey paper, black only", "#F4F4F2", "#E9E9E6", "#151515", "#4A4A4A", "#CFCFCB", "#151515", surface="#F4F4F2"),
        dark("Dark reader", "#181818", "#1F1F1F", "#272727", "#EDEDED", "#B0B0B0", "#3A3A3A", "oklch(0.8 0.1 240)"),
    ],
    # ---- Version 4, "Blueprint" ----
    4: [
        light("Cobalt and yellow", "#EDF0F5", "#E1E6EF", "#0C1424", "#4A5568", "#C5CCDA", "oklch(0.5 0.2 262)",
              extra={"hi": "oklch(0.9 0.16 98)", "dot": "#C5CCDA"}),
        light("Teal and coral", "#EEF3F2", "#DFE8E6", "#0E1B1A", "#4A5C5A", "#C4D2CF", "oklch(0.5 0.09 195)",
              extra={"hi": "oklch(0.84 0.11 35)", "dot": "#C4D2CF", "on-hi": "#0E1B1A"}),
        light("Ink and orange", "#F3F1EC", "#E6E2D9", "#171512", "#5A554D", "#D3CFC4", "#171512",
              extra={"hi": "oklch(0.8 0.15 60)", "dot": "#D3CFC4", "on-hi": "#171512"}),
        light("Forest and lime", "#EFF2EA", "#E1E7D8", "#10190F", "#4C5A49", "#CBD3C0", "oklch(0.42 0.1 150)",
              extra={"hi": "oklch(0.9 0.16 120)", "dot": "#CBD3C0", "on-hi": "#10190F"}),
        dark("Night blueprint", "#181818", "#1F1F1F", "#272727", "#F2F2F2", "#A8A8A8", "#3A3A3A", "oklch(0.62 0.19 262)", on="#FFFFFF",
             extra={"hi": "oklch(0.88 0.16 98)", "dot": "#313131", "on-hi": "#181818", "foot-bg": "#000000"}),
    ],
    # ---- Version 5, "Cover" ----
    5: [
        light("Cloud and indigo", "#FAFAFB", "#EEF0F4", "#14161C", "#5B6070", "#E1E4EA", "oklch(0.5 0.19 275)"),
        light("Cream and terracotta", "#FBF7F2", "#F1E9DF", "#1E1A17", "#6A5F56", "#E5DBCF", "oklch(0.58 0.14 40)"),
        light("Snow and emerald", "#F8FAF9", "#E9EFEC", "#121A16", "#55635C", "#DDE5E0", "oklch(0.5 0.11 160)"),
        dark("Deep navy and sky", "#131926", "#1A2233", "#232D42", "#EEF2F8", "#A3AEC2", "#2C3750", "oklch(0.78 0.11 230)", on="#131926"),
        dark("Charcoal and rose", "#181818", "#1F1F1F", "#272727", "#F3F3F3", "#A8A8A8", "#313131", "oklch(0.78 0.11 10)"),
    ],
    # ---- Version 6, "Split" ----
    6: [
        light("Sage", "#F3F5F0", "#E5E9DF", "#161A14", "#5B6356", "#D6DCCD", "oklch(0.45 0.08 150)"),
        light("Bone and orange", "#F5F3EF", "#E9E5DD", "#191715", "#615B53", "#DAD4C9", "oklch(0.6 0.17 45)"),
        light("Ice and navy", "#F1F5F9", "#E2E8F0", "#0F172A", "#52607A", "#CFD8E3", "oklch(0.42 0.13 262)"),
        dark("Plum night", "#191720", "#211E2A", "#2B2736", "#F1EFF5", "#ABA6B8", "#353044", "oklch(0.78 0.11 310)", on="#191720"),
        dark("Carbon and yellow", "#181818", "#1F1F1F", "#272727", "#F3F3F3", "#A8A8A8", "#313131", "oklch(0.88 0.16 98)"),
    ],
}


def css():
    """The stylesheet for themes 2 to 5 of every version."""
    out = ["/* GENERATED by tools/build_versions.py from tools/themes.py. Do not edit by hand. */\n"]
    for v in sorted(THEMES):
        scope = "html:not([data-version])" if v == 1 else 'html[data-version="%d"]' % v
        for i, t in enumerate(THEMES[v], 1):
            if i == 1:
                continue
            head = t.get("head", (t["text"], t["text"]))
            rows = [
                ("bg", t["bg"]), ("surface", t["surface"]), ("surface-2", t["surface2"]),
                ("text", t["text"]), ("muted", t["muted"]), ("line", t["line"]),
                ("accent", t["accent"]), ("accent-text", t["on"]),
                ("head-from", head[0]), ("head-to", head[1]),
                ("nav-bg", "color-mix(in srgb, %s 76%%, transparent)" % t["bg"]),
                ("id-c", "oklch(0.8 0.11 350)" if t["dark"] else "oklch(0.5 0.12 350)"),
                ("oc-c", "oklch(0.8 0.09 255)" if t["dark"] else "oklch(0.47 0.12 255)"),
            ]
            rows += sorted(t.get("extra", {}).items())
            out.append("/* version %d, theme %d: %s */\n%s[data-theme=\"%d\"] {\n%s\n  color-scheme: %s;\n}\n" % (
                v, i, t["name"], scope, i,
                "\n".join("  --%s: %s;" % kv for kv in rows), "dark" if t["dark"] else "light"))
    return "\n".join(out)
