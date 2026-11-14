(function () {
  var MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"];
  var CHECK = '<svg class="ico" aria-hidden="true" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" fill="#F2B632"/><path d="M5.5 10.5l3 3 6-6.5" fill="none" stroke="#173A2B" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var BOX = '<svg class="ico" aria-hidden="true" viewBox="0 0 20 20"><rect x="1.5" y="1.5" width="17" height="17" rx="5" fill="none" stroke="#F2B632" stroke-width="2" stroke-dasharray="4 3"/></svg>';

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
  function dish(d, mine) {
    var tag = d.kerala ? '<span class="tag">KERALA</span>' : '';
    var status = '';
    if (!mine) status = d.by ? '<span class="status taken">Claimed by ' + esc(d.by) + '</span>' : '<span class="status open">Up for grabs</span>';
    return '<li>' + (mine || d.by ? CHECK : BOX) + '<div><div class="dish-name">' + esc(d.name) + tag + '</div><div class="dish-desc">' + esc(d.desc) + '</div>' + status + '</div></li>';
  }

  var ours = document.getElementById("ours"), bring = document.getElementById("bring");
  if (ours && window.THANKSGIVING) {
    ours.innerHTML = THANKSGIVING.ours.map(function (d) { return dish(d, true); }).join("");
    bring.innerHTML = THANKSGIVING.bring.map(function (d) { return dish(d, false); }).join("");
    var left = THANKSGIVING.bring.filter(function (d) { return !d.by; }).length;
    var c = document.getElementById("open-count");
    if (c) c.textContent = left ? left + " still up for grabs" : "Everything’s claimed — thank you!";
  }

  function nextDate(e, today) {
    if (e.year) return new Date(e.year, e.month - 1, e.day);
    var d = new Date(today.getFullYear(), e.month - 1, e.day);
    if (d < today) d = new Date(today.getFullYear() + 1, e.month - 1, e.day);
    return d;
  }
  var list = document.getElementById("events"), soon = document.getElementById("next-up");
  if ((list || soon) && window.EVENTS) {
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var items = EVENTS.map(function (e) { return { e: e, d: nextDate(e, today) }; })
      .filter(function (x) { return x.d >= today; })
      .sort(function (a, b) { return a.d - b.d; });
    function row(x) {
      var days = Math.round((x.d - today) / 86400000);
      var away = days === 0 ? "Today!" : days === 1 ? "Tomorrow" : "In " + days + " days";
      var title = x.e.link ? '<a href="' + x.e.link + '">' + esc(x.e.title) + '</a>' : esc(x.e.title);
      return '<li class="event"><div class="date-chip"><span class="m">' + MONTHS[x.d.getMonth()] + '</span><span class="d">' + x.d.getDate() + '</span></div>' +
        '<div><div class="t">' + title + '</div><div class="s">' + esc(x.e.detail || "") + '</div><div class="away">' + away + '</div></div></li>';
    }
    if (list) list.innerHTML = items.map(row).join("");
    if (soon) soon.innerHTML = items.slice(0, 3).map(row).join("");
  }
})();
