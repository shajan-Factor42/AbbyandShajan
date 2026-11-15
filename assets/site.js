(function () {
  var MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"];
  var CHECK = '<svg class="ico" aria-hidden="true" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" fill="#1E6B47"/><path d="M5.5 10.5l3 3 6-6.5" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var BOX = '<svg class="ico" aria-hidden="true" viewBox="0 0 20 20"><rect x="1.5" y="1.5" width="17" height="17" rx="5" fill="none" stroke="#1E6B47" stroke-width="2" stroke-dasharray="4 3"/></svg>';

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
  function dish(d, mine) {
    var tag = d.kerala ? '<span class="tag">KERALA</span>' : '';
    var status = '';
    if (!mine) status = d.by ? '<span class="status taken">Claimed by ' + esc(d.by) + '</span>' : '<span class="status open">Up for grabs</span>';
    return '<li>' + (mine || d.by ? CHECK : BOX) + '<div><div class="dish-name">' + esc(d.name) + tag + '</div><div class="dish-desc">' + esc(d.desc) + '</div>' + status + '</div></li>';
  }

  var ours = document.getElementById("ours"), bring = document.getElementById("bring");
  if (ours && window.THANKSGIVING) {
    var claims = {};
    THANKSGIVING.bring.forEach(function (d) { if (d.by) claims[d.name] = d.by; });
    var openForm = null;
    ours.innerHTML = THANKSGIVING.ours.map(function (d) { return dish(d, true); }).join("");

    function renderBring() {
      bring.innerHTML = THANKSGIVING.bring.map(function (d, i) {
        var tag = d.kerala ? '<span class="tag">KERALA</span>' : '';
        var by = claims[d.name];
        var head = '<div class="dish-name">' + esc(d.name) + tag + '</div><div class="dish-desc">' + esc(d.desc) + '</div>';
        if (by) return '<li>' + CHECK + '<div>' + head + '<span class="status taken">' + esc(by) + '’s bringing this</span></div></li>';
        if (openForm === i) {
          return '<li>' + BOX + '<div style="flex:1">' + head +
            '<form class="claim-form" data-i="' + i + '"><label for="claim-name">Your name</label>' +
            '<div class="claim-row"><input id="claim-name" name="name" autocomplete="name" maxlength="40" required placeholder="e.g. Shibu">' +
            '<input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">' +
            '<button class="btn" type="submit">I’ll bring it</button><button class="btn btn-ghost" type="button" data-cancel>Cancel</button></div>' +
            '<p class="claim-msg" role="status" aria-live="polite"></p></form></div></li>';
        }
        return '<li>' + BOX + '<div>' + head + '<button class="claim-btn" type="button" data-i="' + i + '">Up for grabs · tap to claim</button></div></li>';
      }).join("");
      var left = THANKSGIVING.bring.filter(function (d) { return !claims[d.name]; }).length;
      var c = document.getElementById("open-count");
      if (c) c.textContent = left ? left + " still up for grabs" : "Everything’s claimed. Thank you!";
      var inp = document.getElementById("claim-name");
      if (inp) inp.focus();
    }

    bring.addEventListener("click", function (e) {
      var b = e.target.closest(".claim-btn");
      if (b) { openForm = +b.getAttribute("data-i"); renderBring(); return; }
      if (e.target.closest("[data-cancel]")) { openForm = null; renderBring(); }
    });
    bring.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target, d = THANKSGIVING.bring[+f.getAttribute("data-i")];
      var name = f.elements.name.value.trim(), msg = f.querySelector(".claim-msg"), btn = f.querySelector('button[type="submit"]');
      if (name.length < 2) { msg.textContent = "Please enter your name."; return; }
      btn.disabled = true; msg.textContent = "Saving…";
      fetch(SITE_API + "/claim", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event: THANKSGIVING_EVENT, dish: d.name, name: name, website: f.elements.website.value }) })
        .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); })
        .then(function (res) {
          if (res.status === 200) { claims[d.name] = res.body.name || name; openForm = null; renderBring(); }
          else if (res.status === 409) { if (res.body.by) claims[d.name] = res.body.by; openForm = null; renderBring(); alertMsg(d.name + " was just claimed by " + (res.body.by || "someone else") + "."); }
          else { btn.disabled = false; msg.textContent = res.body.error || "Something went wrong. Please try again."; }
        })
        .catch(function () { btn.disabled = false; msg.textContent = "Couldn’t save right now. Please try again, or text Shajan or Abby."; });
    });
    function alertMsg(t) { var c = document.getElementById("open-count"); if (c) c.textContent = t; }

    renderBring();
    if (window.SITE_API && window.fetch) {
      fetch(SITE_API + "/claims?event=" + encodeURIComponent(THANKSGIVING_EVENT))
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) { if (j && j.claims) { for (var k in j.claims) claims[k] = j.claims[k]; if (openForm === null) renderBring(); } })
        .catch(function () {});
    }
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

  var fc = document.getElementById("fund-current");
  if (fc && window.FUNDRAISER) {
    var F = FUNDRAISER, money = function (n) { return "$" + Number(n).toLocaleString("en-US"); };
    if (!F.charity) {
      fc.innerHTML = '<div class="when">' + F.year + ' fundraiser</div><div class="what">We’re choosing this year’s cause</div>' +
        '<p>The family is deciding right now. Check back soon to see who we’re raising money for and how to give.</p>';
    } else {
      var bar = "";
      if (F.goal && F.raised) {
        var pct = Math.min(100, Math.round(F.raised / F.goal * 100));
        bar = '<div class="meter" role="img" aria-label="' + money(F.raised) + ' raised of ' + money(F.goal) + '"><span style="width:' + pct + '%"></span></div>' +
          '<p class="meter-label"><strong>' + money(F.raised) + '</strong> raised of ' + money(F.goal) + ' goal</p>';
      } else if (F.goal) {
        bar = '<p class="meter-label">Goal: <strong>' + money(F.goal) + '</strong></p>';
      }
      var btns = '';
      if (F.gofundme) btns += '<a class="btn" href="' + esc(F.gofundme) + '">Give on GoFundMe</a>';
      if (F.charityLink) btns += '<a class="btn btn-ghost" href="' + esc(F.charityLink) + '">Give to the charity directly</a>';
      fc.innerHTML = '<div class="when">' + F.year + ' fundraiser · ends ' + esc(F.deadline) + '</div><div class="what">' + esc(F.charity) + '</div>' +
        (F.why ? '<p>' + esc(F.why) + '</p>' : '') + bar + (btns ? '<div class="btn-row">' + btns + '</div>' : '');
    }
  }
  var fp = document.getElementById("fund-past");
  if (fp && window.FUNDRAISER_PAST && FUNDRAISER_PAST.length) {
    document.getElementById("fund-past-wrap").hidden = false;
    fp.innerHTML = FUNDRAISER_PAST.slice().sort(function (a, b) { return b.year - a.year; }).map(function (p) {
      return '<li class="event"><div class="date-chip"><span class="m">YEAR</span><span class="d" style="font-size:22px">' + p.year + '</span></div>' +
        '<div><div class="t">' + esc(p.charity) + '</div>' + (p.raised ? '<div class="s">Raised $' + Number(p.raised).toLocaleString("en-US") + '</div>' : '') + '</div></li>';
    }).join("");
  }
})();
