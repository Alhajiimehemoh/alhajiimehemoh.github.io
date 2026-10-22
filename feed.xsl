<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>RSS feed: <xsl:value-of select="rss/channel/title"/></title>
<link rel="icon" href="images/favicon-32.png" type="image/png"/>
<style>
@font-face{font-family:'Bricolage Grotesque';font-weight:200 800;font-display:swap;src:url(fonts/bricolage-grotesque-latin-var.woff2) format('woff2')}
@font-face{font-family:'DM Sans';font-weight:100 1000;font-display:swap;src:url(fonts/dm-sans-latin-var.woff2) format('woff2')}
@font-face{font-family:'JetBrains Mono';font-weight:500;font-display:swap;src:url(fonts/jetbrains-mono-latin-500-normal.woff2) format('woff2')}
:root{--paper:#F3F6F4;--sheet:#fff;--ink:#0F2430;--muted:#475D68;--rule:#D3DED9;--green:#0B7A5C;--green-soft:#DDF0E8;--amber:#D68A00}
@media (prefers-color-scheme:dark){:root{--paper:#0A171D;--sheet:#112630;--ink:#E7EFEC;--muted:#A3B6BD;--rule:#25404B;--green:#3CC79A;--green-soft:#12372F}}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(50rem 24rem at 85% -10%,rgba(11,122,92,.14),transparent 70%),var(--paper);color:var(--ink);font:400 1.0625rem/1.65 'DM Sans',system-ui,sans-serif}
.bar{position:sticky;top:0;background:color-mix(in srgb,var(--paper) 85%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--rule)}
.bar .in{width:min(64rem,100% - 2rem);margin:0 auto;display:flex;align-items:center;gap:.7rem;min-height:4rem}
.bar img{height:26px}.bar b{font-family:'Bricolage Grotesque',sans-serif;font-weight:750;letter-spacing:-.02em}
.bar a{color:var(--ink);text-decoration:none;display:flex;align-items:center;gap:.6rem}.bar .r{margin-left:auto;font-weight:600;color:var(--green)}
.wrap{width:min(64rem,100% - 2rem);margin:0 auto;padding:3rem 0 4rem}
h1,h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;letter-spacing:-.035em;line-height:1.02}
h1{font-size:clamp(2.2rem,6vw,3.6rem);margin:.6rem 0 .8rem}
.tag{display:inline-flex;align-items:center;gap:.4rem;font:500 .75rem 'JetBrains Mono',monospace;background:var(--green-soft);color:var(--green);padding:.3rem .7rem;border-radius:999px}
.box{display:flex;gap:1rem;align-items:center;flex-wrap:wrap;background:var(--sheet);border:1.5px solid var(--rule);border-radius:18px;padding:1rem 1.2rem;margin:1.5rem 0 2.5rem;box-shadow:0 22px 44px -18px rgba(15,36,48,.28)}
.box p{margin:0;flex:1;min-width:16rem}.muted{color:var(--muted)}
code{display:block;margin-top:.4rem;font:500 .9rem 'JetBrains Mono',monospace;word-break:break-all;color:var(--green)}
.btn{display:inline-block;padding:.8rem 1.3rem;border-radius:999px;background:var(--green);color:#fff;font-weight:600;text-decoration:none}
a{color:var(--green);text-underline-offset:3px}
ol{list-style:none;margin:0;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(18rem,1fr))}
li{background:var(--sheet);border:1px solid var(--rule);border-radius:20px;padding:1.2rem 1.3rem;display:flex;flex-direction:column;gap:.4rem;transition:transform .25s,box-shadow .25s}
li:hover{transform:translateY(-4px);box-shadow:0 22px 44px -18px rgba(15,36,48,.28)}
li h2{font-size:1.15rem;margin:0;letter-spacing:-.02em;line-height:1.25}li h2 a{color:var(--ink);text-decoration:none}li h2 a:hover{color:var(--green)}
li p{margin:0;color:var(--muted);font-size:.93rem}.meta{font:500 .72rem 'JetBrains Mono',monospace;color:var(--muted)}
.cat{align-self:flex-start;font:500 .7rem 'JetBrains Mono',monospace;color:var(--green);background:var(--green-soft);padding:.2rem .55rem;border-radius:999px}
</style></head>
<body>
<div class="bar"><div class="in"><a href="index.html"><img src="images/brand/logo-mark.png" alt=""/><b>Alhaji Ibrahim Mehemoh</b></a><a class="r" href="community.html">All notes</a></div></div>
<div class="wrap">
<span class="tag">RSS feed</span>
<h1><xsl:value-of select="rss/channel/title"/></h1>
<p class="muted"><xsl:value-of select="rss/channel/description"/></p>
<div class="box"><p><strong>This is a feed you can follow.</strong> Copy this page address into a feed reader such as Feedly, Inoreader or NetNewsWire, and new notes arrive automatically.<code>https://alhajiimehemoh.github.io/feed.xml</code></p><a class="btn" href="rss.html">How to follow</a></div>
<ol>
<xsl:for-each select="rss/channel/item">
<li><span class="cat"><xsl:value-of select="category"/></span>
<h2><a href="{link}"><xsl:value-of select="title"/></a></h2>
<p><xsl:value-of select="description"/></p>
<span class="meta"><xsl:value-of select="substring(pubDate,6,11)"/></span></li>
</xsl:for-each>
</ol>
</div></body></html>
</xsl:template>
</xsl:stylesheet>
