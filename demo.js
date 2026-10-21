(function () {
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var facs = ['Sample PHC 1','Sample PHC 2','Sample PHC 3','Sample PHC 4','Sample PHC 5'];
  var seed = 7; function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
  var data = facs.map(function (f, i) {
    var target = 60 + i * 14;
    return { name: f, target: target, m: months.map(function (_, k) {
      return Math.round(target * (0.62 + 0.3 * rnd() + (i === 3 ? -0.12 : 0) + k * 0.004));
    }) };
  });
  var $ = function (id) { return document.getElementById(id); };
  var facSel = $('dFac'), from = $('dFrom'), to = $('dTo'), view = $('dView');
  if (!facSel) return;
  facSel.innerHTML = '<option value="all">All facilities</option>' + facs.map(function (f, i) { return '<option value="' + i + '">' + f + '</option>'; }).join('');
  [from, to].forEach(function (s, n) { s.innerHTML = months.map(function (m, i) { return '<option value="' + i + '"' + (i === (n ? 11 : 0) ? ' selected' : '') + '>' + m + '</option>'; }).join(''); });
  function sum(a) { return a.reduce(function (x, y) { return x + y; }, 0); }
  function svgEl(t, a) { var e = document.createElementNS('http://www.w3.org/2000/svg', t); for (var k in a) e.setAttribute(k, a[k]); return e; }
  function render() {
    var f = facSel.value, a = +from.value, b = +to.value; if (b < a) { b = a; to.value = b; }
    var mode = view.value;
    if (mode === 'nurse' && f === 'all') { f = '0'; facSel.value = '0'; }
    facSel.disabled = mode === 'donor';
    var rows = data.filter(function (d, i) { return f === 'all' || +f === i || mode === 'donor'; });
    var span = b - a + 1;
    var doses = sum(rows.map(function (d) { return sum(d.m.slice(a, b + 1)); }));
    var tgt = sum(rows.map(function (d) { return d.target * span; }));
    var cov = Math.round(doses / tgt * 100);
    var low = rows.filter(function (d) { return sum(d.m.slice(a, b + 1)) / (d.target * span) < 0.8; }).length;
    var k = [['Doses given', doses], ['Coverage', cov + '%'], ['Facilities below 80%', low], ['Months shown', span]];
    $('dKpis').innerHTML = k.map(function (x) { return '<div class="kpi"><span>' + x[0] + '</span><strong>' + x[1] + '</strong></div>'; }).join('');
    // trend
    var t = $('dTrend'); t.innerHTML = '';
    var series = []; for (var i = a; i <= b; i++) series.push(sum(rows.map(function (d) { return d.m[i]; })));
    var max = Math.max.apply(null, series) * 1.15 || 1, W = 600, H = 260, p = 36;
    var pts = series.map(function (v, i) { return [p + (series.length > 1 ? i * (W - 2 * p) / (series.length - 1) : (W - 2 * p) / 2), H - p - v / max * (H - 2 * p)]; });
    t.appendChild(svgEl('line', { x1: p, y1: H - p, x2: W - p, y2: H - p, stroke: 'currentColor', 'stroke-opacity': .3 }));
    t.appendChild(svgEl('polyline', { points: pts.map(function (q) { return q.join(','); }).join(' '), fill: 'none', stroke: 'var(--green)', 'stroke-width': 3 }));
    pts.forEach(function (q, i) {
      var c = svgEl('circle', { cx: q[0], cy: q[1], r: 4, fill: 'var(--green)' }); var tt = svgEl('title', {}); tt.textContent = months[a + i] + ': ' + series[i]; c.appendChild(tt); t.appendChild(c);
      var l = svgEl('text', { x: q[0], y: H - 12, 'text-anchor': 'middle', 'font-size': 11, fill: 'currentColor' }); l.textContent = months[a + i]; t.appendChild(l);
    });
    // bars
    var s = $('dBars'); s.innerHTML = '';
    var all = data.map(function (d) { return { n: d.name, c: Math.round(sum(d.m.slice(a, b + 1)) / (d.target * span) * 100) }; });
    var bw = (W - 2 * p) / all.length;
    var y90 = H - p - 90 / 120 * (H - 2 * p);
    all.forEach(function (d, i) {
      var h = Math.min(d.c, 120) / 120 * (H - 2 * p);
      var r = svgEl('rect', { x: p + i * bw + 10, y: H - p - h, width: bw - 20, height: h, rx: 4, fill: d.c >= 90 ? 'var(--green)' : d.c >= 80 ? 'var(--amber)' : 'var(--blue)' });
      var tt = svgEl('title', {}); tt.textContent = d.n + ': ' + d.c + '%'; r.appendChild(tt); s.appendChild(r);
      var l = svgEl('text', { x: p + i * bw + bw / 2, y: H - 12, 'text-anchor': 'middle', 'font-size': 10.5, fill: 'currentColor' }); l.textContent = d.n.replace('Sample ', ''); s.appendChild(l);
      var v = svgEl('text', { x: p + i * bw + bw / 2, y: H - p - h - 6, 'text-anchor': 'middle', 'font-size': 11, fill: 'currentColor' }); v.textContent = d.c + '%'; s.appendChild(v);
    });
    s.appendChild(svgEl('line', { x1: p, y1: y90, x2: W - p, y2: y90, stroke: 'currentColor', 'stroke-dasharray': '5 4', 'stroke-opacity': .6 }));
    // table
    var tbl = $('dTable');
    if (mode === 'donor') { tbl.innerHTML = '<caption class="sr-only">Summary</caption><tr><th>Programme</th><th>Doses</th><th>Coverage</th></tr><tr><td>All sample facilities</td><td>' + doses + '</td><td>' + cov + '%</td></tr>'; return; }
    tbl.innerHTML = '<caption class="sr-only">Facility summary</caption><tr><th>Facility</th><th>Doses</th><th>Target</th><th>Coverage</th></tr>' + rows.map(function (d) {
      var x = sum(d.m.slice(a, b + 1)), tg = d.target * span, c = Math.round(x / tg * 100);
      return '<tr><td>' + d.name + '</td><td>' + x + '</td><td>' + tg + '</td><td>' + c + '%</td></tr>'; }).join('');
  }
  [facSel, from, to, view].forEach(function (e) { e.addEventListener('change', render); });
  render();
})();
