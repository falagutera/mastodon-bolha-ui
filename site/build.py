#!/usr/bin/env python3
"""Build ui.bolha.us: one page about the Bolha UI theme, pt-BR at / and English at /en/.

Reads VERSION and CHANGELOG.md from the repository, so a release updates the page by itself.
Usage: python3 site/build.py [output dir, default public]
"""
import html
import pathlib
import re
import shutil
import sys

SITE = pathlib.Path(__file__).parent
REPO_DIR = SITE.parent
OUT = REPO_DIR / (sys.argv[1] if len(sys.argv) > 1 else "public")

VERSION = (REPO_DIR / "VERSION").read_text().strip()
REPO = "https://gitlab.gutocarvalho.net/open/bolha/mastodon-bolha-ui"
TARBALL = f"{REPO}/-/jobs/artifacts/v{VERSION}/raw/mastodon-bolha-ui.tar.gz?job=release"
IMAGES = ["advanced-dark", "advanced-light", "advanced-gcn", "simple-light", "simple-dark", "tinted-surfaces"]


def releases(limit=5):
    """(version, date) of the newest CHANGELOG entries."""
    out = re.findall(r"^## (\d+\.\d+\.\d+) — (\d{4}-\d{2}-\d{2})", (REPO_DIR / "CHANGELOG.md").read_text(), re.M)
    return out[:limit]


SERVER = f"""# como usuário mastodon
cd ~
curl -fsSL "{TARBALL}" | tar -xz
./mastodon-bolha-ui-{VERSION}-*/install.sh ~/live
cd ~/live && RAILS_ENV=production bundle exec rails assets:precompile

# como root
systemctl restart mastodon-web mastodon-sidekiq mastodon-streaming"""

DOCKER = f"""git clone https://github.com/mastodon/mastodon.git && cd mastodon
git checkout v4.7.5                      # a versão que você roda
curl -fsSL "{TARBALL}" | tar -xz -C ..
../mastodon-bolha-ui-{VERSION}-*/install.sh .
docker build -t meu-registry/mastodon:v4.7.5-bolha-ui ."""

EN_CODE = {
    "# como usuário mastodon": "# as the mastodon user",
    "# como root": "# as root",
    "# a versão que você roda": "# the version you run",
    "meu-registry": "my-registry",
}

T = {
    "pt": {
        "lang": "pt-BR", "path": "", "other_href": "/en/", "other_label": "EN", "theme": "tema",
        "title": "Bolha UI · tema para Mastodon",
        "desc": "Bolha UI: um tema quente e amigável para a interface web do Mastodon, em amarelo ou vermelho, claro e escuro. Como instalar no seu servidor.",
        "kicker": f"tema para mastodon · v{VERSION}",
        "h1": "Bolha UI, o Mastodon com a <em>cara da bolha</em>",
        "lede": "Um tema para a interface web do Mastodon. Colunas viram cartões, títulos e horários em fonte mono, botões em pílula e o amarelo da bolha em tudo (ou o vermelho, na variante GCN). Claro, escuro e alto contraste, do jeito que cada pessoa escolher.",
        "cta_install": "Como instalar", "cta_repo": "Código no GitLab",
        "s_shots": "como fica",
        "caps": ["Interface avançada, escuro", "Interface avançada, claro", "Variante GCN (vermelho)",
                 "Coluna única, claro", "Coluna única, escuro", "Fundos tingidos (desde a 1.1.0)"],
        "mock": "As imagens são simulações com pessoas e posts inventados; o tema de verdade roda no bolha.us e no jornalismo.social.",
        "s_what": "o que vem",
        "what": [
            ("Dois temas", "<b>Bolha UI</b> (amarelo) e <b>Bolha UI GCN</b> (vermelho), ao lado dos temas do próprio Mastodon."),
            ("Claro, escuro e alto contraste", "Segue o esquema de cores e o contraste que cada pessoa escolhe em Preferências › Aparência."),
            ("Fontes Ubuntu", "Ubuntu e Ubuntu Mono vêm junto, então todo mundo vê a mesma letra."),
            ("Pequeno e resistente", "Cerca de 110 linhas sobre o tema padrão, quase tudo variável de design. Atualizar o Mastodon raramente quebra."),
        ],
        "s_install": "como instalar",
        "install_p": "Três jeitos, do mais completo ao mais rápido. Testado no Mastodon 4.7.",
        "opt1_t": "1. No seu servidor (recomendado)",
        "opt1_p": "Para instalações a partir do código-fonte. O <code>install.sh</code> copia o tema, as fontes e os nomes, e acrescenta duas linhas em <code>config/themes.yml</code>. Use <code>--dry-run</code> para ver antes e <code>--uninstall</code> para remover.",
        "opt1_after": "Depois cada pessoa escolhe o tema em <b>Preferências › Aparência › Tema</b>. Para virar o padrão de quem chega: <b>Administração › Configurações do servidor › Aparência</b>.",
        "opt2_t": "2. Com Docker",
        "opt2_p": "As imagens oficiais já vêm com os assets compilados, então o tema precisa de uma imagem própria. Use-a nos serviços <code>web</code> e <code>sidekiq</code>; o <code>streaming</code> não muda.",
        "opt3_t": "3. Como CSS personalizado (sem acesso ao servidor)",
        "opt3_p": "Cole o CSS pronto em <b>Administração › Configurações do servidor › Aparência › CSS personalizado</b>: <a href=\"{repo}/-/raw/main/dist/bolha-ui.css\">bolha-ui.css</a> (amarelo) ou <a href=\"{repo}/-/raw/main/dist/bolha-ui-gcn.css\">bolha-ui-gcn.css</a> (vermelho). O mesmo arquivo funciona como estilo pessoal no <a href=\"https://github.com/openstyles/stylus\">Stylus</a>, em qualquer servidor Mastodon 4.7. Esse jeito não traz as fontes.",
        "s_ver": "versões",
        "ver_p": "A versão é <code>X.Y.Z-BUILD</code>, e o tema mostra a sua onde houver a classe <code>bolha-ui-version</code>. O que mudou em cada uma está no <a href=\"{repo}/-/blob/main/CHANGELOG.md\">CHANGELOG</a> (em inglês).",
        "th_ver": ["Versão", "Data", ""], "latest": "atual",
        "s_where": "onde roda",
        "where_p": "Feito para a <a href=\"https://bolha.us\">bolha.us</a> e as outras comunidades da <a href=\"https://bolha.io\">bolha.io</a>. O Mastodon da bolha, com o tema e outros recursos, está em <a href=\"https://custom.bolha.us\">custom.bolha.us</a>.",
        "license": "Código aberto, AGPL-3.0, como o Mastodon. Inspirado no Tangerine UI.",
        "footer": "feito pela comunidade bolha",
    },
    "en": {
        "lang": "en", "path": "en", "other_href": "/", "other_label": "PT", "theme": "theme",
        "title": "Bolha UI · a Mastodon theme",
        "desc": "Bolha UI: a warm, friendly theme for Mastodon's web interface, in yellow or red, light and dark. How to install it on your server.",
        "kicker": f"mastodon theme · v{VERSION}",
        "h1": "Bolha UI, Mastodon with the <em>bolha look</em>",
        "lede": "A theme for Mastodon's web interface. Columns become cards, headers and times are set in mono, buttons are pills, and everything wears the bolha yellow (or red, in the GCN variant). Light, dark and high contrast, the way each person picks.",
        "cta_install": "How to install", "cta_repo": "Code on GitLab",
        "s_shots": "how it looks",
        "caps": ["Advanced interface, dark", "Advanced interface, light", "GCN variant (red)",
                 "Single column, light", "Single column, dark", "Tinted surfaces (since 1.1.0)"],
        "mock": "The screenshots are mockups with made-up people and posts; the real theme runs on bolha.us and jornalismo.social.",
        "s_what": "what you get",
        "what": [
            ("Two themes", "<b>Bolha UI</b> (yellow) and <b>Bolha UI GCN</b> (red), next to Mastodon's own."),
            ("Light, dark and high contrast", "Follows the colour scheme and contrast each person picks in Preferences › Appearance."),
            ("Ubuntu fonts", "Ubuntu and Ubuntu Mono are bundled, so everyone sees the same type."),
            ("Small and sturdy", "About 110 lines on top of the default theme, almost all design tokens. Mastodon upgrades rarely break it."),
        ],
        "s_install": "how to install",
        "install_p": "Three ways, from the most complete to the quickest. Tested on Mastodon 4.7.",
        "opt1_t": "1. On your server (recommended)",
        "opt1_p": "For from-source installs. <code>install.sh</code> copies the theme, the fonts and the names, and adds two lines to <code>config/themes.yml</code>. Use <code>--dry-run</code> to look first and <code>--uninstall</code> to remove it.",
        "opt1_after": "Then each person picks the theme in <b>Preferences › Appearance › Theme</b>. To make it the default for newcomers: <b>Administration › Server settings › Appearance</b>.",
        "opt2_t": "2. With Docker",
        "opt2_p": "The official images have their assets built in, so the theme needs its own image. Use it for the <code>web</code> and <code>sidekiq</code> services; <code>streaming</code> doesn't change.",
        "opt3_t": "3. As custom CSS (no server access)",
        "opt3_p": "Paste the ready CSS into <b>Administration › Server settings › Appearance › Custom CSS</b>: <a href=\"{repo}/-/raw/main/dist/bolha-ui.css\">bolha-ui.css</a> (yellow) or <a href=\"{repo}/-/raw/main/dist/bolha-ui-gcn.css\">bolha-ui-gcn.css</a> (red). The same file works as a personal style with <a href=\"https://github.com/openstyles/stylus\">Stylus</a> on any Mastodon 4.7 server. This way has no bundled fonts.",
        "s_ver": "versions",
        "ver_p": "Versions look like <code>X.Y.Z-BUILD</code>, and the theme shows its own wherever there is the class <code>bolha-ui-version</code>. What changed in each one is in the <a href=\"{repo}/-/blob/main/CHANGELOG.md\">CHANGELOG</a>.",
        "th_ver": ["Version", "Date", ""], "latest": "current",
        "s_where": "where it runs",
        "where_p": "Made for <a href=\"https://bolha.us\">bolha.us</a> and the other <a href=\"https://bolha.io\">bolha.io</a> communities. The bolha Mastodon, with the theme and other features, is at <a href=\"https://custom.bolha.us/en/\">custom.bolha.us</a>.",
        "license": "Open source, AGPL-3.0, like Mastodon. Inspired by Tangerine UI.",
        "footer": "made by the bolha community",
    },
}

ICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='11' fill='%23F5B301'/%3E%3C/svg%3E"
THEME_JS = "(function(){var t=document.getElementById('tg'),r=document.documentElement;function c(){return r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}t.addEventListener('click',function(){r.setAttribute('data-theme',c()==='dark'?'light':'dark')})})();"


def e(s):
    return html.escape(s, quote=False)


def cat(title, anchor=""):
    a = f' id="{anchor}"' if anchor else ""
    return f'<div class="cat"{a}><h2>{title}</h2><span class="rule"></span></div>'


def code(body):
    body = re.sub(r"(#[^\n]*)", lambda m: f'<span class="c">{m.group(1)}</span>', e(body))
    return f'<pre class="code">{body}</pre>'


def page(t):
    en = t["lang"] == "en"
    fix = (lambda s: s) if not en else (lambda s: [s := s.replace(a, b) for a, b in EN_CODE.items()][-1])
    shots = "".join(
        f'<figure class="shot{" wide" if i in (0, 5) else ""}"><a href="/img/{n}.png"><img src="/img/{n}.png" alt="{c}" loading="{"eager" if i == 0 else "lazy"}"></a><figcaption>{c}</figcaption></figure>'
        for i, (n, c) in enumerate(zip(IMAGES, t["caps"]))
    )
    what = "".join(f'<div class="cc"><b>{a}</b><p>{b}</p></div>' for a, b in t["what"])
    badge = f'<span class="badge on">{t["latest"]}</span>'
    vers = "".join(
        f'<tr><td class="mono">{v}</td><td class="dim">{d}</td><td>{badge if i == 0 else ""}</td></tr>'
        for i, (v, d) in enumerate(releases())
    )
    th = "".join(f"<th>{h}</th>" for h in t["th_ver"])
    r = lambda k: t[k].replace("{repo}", REPO)
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<meta property="og:title" content="{t['title']}"><meta property="og:description" content="{t['desc']}">
<meta property="og:image" content="https://ui.bolha.us/img/advanced-dark.png">
<link rel="alternate" hreflang="pt-BR" href="https://ui.bolha.us/"><link rel="alternate" hreflang="en" href="https://ui.bolha.us/en/">
<link rel="icon" href="{ICON}">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="wrap">
  <div class="bar">
    <a class="brand" href="https://bolha.io"><span class="bubble"></span> bolhaverse</a>
    <span class="bar-r">
      <a class="toggle" href="{t['other_href']}" hreflang="{'pt-BR' if en else 'en'}">{t['other_label']}</a>
      <button class="toggle" id="tg" type="button" aria-label="{t['theme']}">{t['theme']}</button>
    </span>
  </div>
  <header class="hero">
    <p class="kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <p class="ctas"><a class="btn primary" href="#install">{t['cta_install']}</a><a class="btn" href="{REPO}">{t['cta_repo']}</a></p>
  </header>
  <main>
    {cat(t['s_shots'])}
    <div class="shots">{shots}</div>
    <p class="note">{t['mock']}</p>

    {cat(t['s_what'])}
    <div class="what">{what}</div>

    {cat(t['s_install'], 'install')}
    <p class="txt">{t['install_p']}</p>
    <div class="opt"><b>{t['opt1_t']}</b><p>{t['opt1_p']}</p>{code(fix(SERVER))}<p>{t['opt1_after']}</p></div>
    <div class="opt"><b>{t['opt2_t']}</b><p>{t['opt2_p']}</p>{code(fix(DOCKER))}</div>
    <div class="opt"><b>{t['opt3_t']}</b><p>{r('opt3_p')}</p></div>

    {cat(t['s_ver'])}
    <p class="txt">{r('ver_p')}</p>
    <div class="tblwrap"><table class="srvtbl"><thead><tr>{th}</tr></thead><tbody>{vers}</tbody></table></div>

    {cat(t['s_where'])}
    <p class="txt">{t['where_p']}</p>
    <p class="txt">{t['license']}</p>
  </main>
  <footer>
    <span>{t['footer']}</span>
    <span class="sep">&middot;</span><a href="https://bolha.us">bolha.us</a>
    <span class="sep">&middot;</span><a href="https://custom.bolha.us{'/en/' if en else ''}">custom.bolha.us</a>
    <span class="sep">&middot;</span><a href="{REPO}">gitlab</a>
  </footer>
</div>
<script>{THEME_JS}</script>
</body></html>
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    css = (SITE / "static" / "base.css").read_text() + (SITE / "static" / "site.css").read_text()
    (OUT / "style.css").write_text(css)
    (OUT / "img").mkdir()
    for n in IMAGES:
        shutil.copy(REPO_DIR / "screenshots" / f"{n}.png", OUT / "img" / f"{n}.png")
    for t in T.values():
        d = OUT / t["path"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(t), encoding="utf-8")
    print(f"built {OUT} (Bolha UI {VERSION})")


if __name__ == "__main__":
    main()
