<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>RSS feed: <xsl:value-of select="rss/channel/title"/></title>
<link rel="icon" href="images/favicon.svg" type="image/svg+xml"/>
<style>
@font-face{font-family:'Bricolage Grotesque';font-weight:200 800;font-display:swap;src:url(fonts/bricolage-grotesque-latin-var.woff2) format('woff2')}
@font-face{font-family:'DM Sans';font-weight:100 1000;font-display:swap;src:url(fonts/dm-sans-latin-var.woff2) format('woff2')}
:root{--paper:#F3F6F4;--sheet:#fff;--ink:#0F2430;--muted:#475D68;--rule:#D3DED9;--green:#0B7A5C;--green-soft:#DDF0E8;--amber:#D68A00}
@media (prefers-color-scheme:dark){:root{--paper:#0A171D;--sheet:#112630;--ink:#E7EFEC;--muted:#A3B6BD;--rule:#25404B;--green:#3CC79A;--green-soft:#12372F}}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:400 1.0625rem/1.65 'DM Sans',system-ui,sans-serif}
.wrap{width:min(46rem,100% - 2rem);margin:0 auto;padding:3rem 0 4rem}
h1,h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;letter-spacing:-.03em;line-height:1.05}
h1{font-size:clamp(2rem,6vw,3rem);margin:.5rem 0 .75rem}
.tag{display:inline-block;font:500 .75rem ui-monospace,Menlo,monospace;background:var(--green-soft);color:var(--green);padding:.3rem .7rem;border-radius:999px}
.box{background:var(--sheet);border:1px solid var(--rule);border-radius:20px;padding:1.25rem 1.4rem;margin:1.5rem 0 2.5rem}
.box p{margin:.25rem 0}.muted{color:var(--muted)}
code{display:block;margin-top:.6rem;padding:.6rem .8rem;border-radius:10px;background:var(--paper);border:1px solid var(--rule);font:500 .9rem ui-monospace,Menlo,monospace;word-break:break-all}
a{color:var(--green);text-underline-offset:3px}
ol{list-style:none;margin:0;padding:0;display:grid;gap:.75rem}
li{background:var(--sheet);border:1px solid var(--rule);border-radius:16px;padding:1rem 1.25rem}
li h2{font-size:1.2rem;margin:0 0 .3rem}li h2 a{color:var(--ink);text-decoration:none}li h2 a:hover{color:var(--green)}
li p{margin:0;color:var(--muted)}.meta{font:500 .75rem ui-monospace,Menlo,monospace;color:var(--muted);margin-bottom:.35rem}
.back{font-weight:600}
</style></head>
<body><div class="wrap">
<a class="back" href="community.html">&#8592; Back to Notes</a>
<p style="margin-top:2rem"><span class="tag">RSS feed</span></p>
<h1><xsl:value-of select="rss/channel/title"/></h1>
<p class="muted"><xsl:value-of select="rss/channel/description"/></p>
<div class="box">
<p><strong>This is a feed you can follow.</strong> Copy the address below into a feed reader such as Feedly, Inoreader or NetNewsWire, and new notes will arrive there automatically.</p>
<code>https://alhajiimehemoh.github.io/feed.xml</code>
<p class="muted" style="margin-top:.75rem">Prefer email or WhatsApp? <a href="contact.html">Contact me</a> and I will send new notes directly.</p>
</div>
<ol>
<xsl:for-each select="rss/channel/item">
<li><div class="meta"><xsl:value-of select="category"/> &#183; <xsl:value-of select="substring(pubDate,6,11)"/></div>
<h2><a href="{link}"><xsl:value-of select="title"/></a></h2>
<p><xsl:value-of select="description"/></p></li>
</xsl:for-each>
</ol>
</div></body></html>
</xsl:template>
</xsl:stylesheet>
