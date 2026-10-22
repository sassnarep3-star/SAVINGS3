// Table filter: any <input data-filter-for="tableId"> filters rows of that table.
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-filter-for]').forEach(function (inp) {
    var tbl = document.getElementById(inp.getAttribute('data-filter-for'));
    if (!tbl) return;
    inp.addEventListener('input', function () {
      var q = inp.value.toLowerCase();
      tbl.querySelectorAll('tbody tr').forEach(function (tr) {
        tr.style.display = tr.textContent.toLowerCase().indexOf(q) > -1 ? '' : 'none';
      });
    });
  });

  // Returns calculator (returns.html). Hypothetical: FV = P*(1+APY)^t.
  var btn = document.getElementById('calc-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var P = parseFloat(document.getElementById('calc-p').value);
      var apy = parseFloat(document.getElementById('calc-apy').value) / 100;
      var out = document.getElementById('calc-out');
      if (!isFinite(P) || P < 0 || !isFinite(apy) || apy < 0) {
        out.innerHTML = '<p>Please enter a deposit of $0 or more and an APY of 0% or more.</p>';
        return;
      }
      var horizons = [[0.5, '6 months (Apr 22, 2027)'], [1, '1 year (Oct 22, 2027)'], [2, '2 years (Oct 22, 2028)'], [3, '3 years (Oct 22, 2029)'], [5, '5 years (Oct 22, 2031)']];
      var fmt = function (n) { return n.toLocaleString('en-US', { style: 'currency', currency: 'USD' }); };
      var rows = horizons.map(function (h) {
        var fv = P * Math.pow(1 + apy, h[0]);
        var over = fv > 250000 ? ' — <strong>exceeds $250,000 single-category limit by ' + fmt(fv - 250000) + '</strong> (excess would be uninsured in that category at that bank)' : '';
        return '<tr><td>' + h[1] + '</td><td class="num">' + fmt(fv - P) + '</td><td class="num">' + fmt(fv) + over + '</td></tr>';
      }).join('');
      out.innerHTML = '<div class="tablebox"><table style="min-width:520px"><caption>Hypothetical growth if ' + (apy * 100).toFixed(2) + '% APY never changed — variable APYs <em>will</em> change. Before fees/taxes.</caption>' +
        '<thead><tr><th>Horizon from Oct 22, 2026</th><th class="num">Interest</th><th class="num">Ending balance</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
        '<p class="small muted">FDIC note: the $250,000 limit covers principal <em>plus</em> accrued interest, combined across all your deposits in the same ownership category at the same bank. See the FDIC-safe deposit table on this page.</p>';
    });
  }
});
