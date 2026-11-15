// Thomas family site API: lets guests claim an open potluck dish.
// Claims can only be added (first claim wins). Changes and removals are done by the family directly in the database.
const EVENTS = {
  "thanksgiving-2026": [
    "Appetizers", "Pappadam", "Chicken Curry & Appam", "Mashed Potatoes", "Stuffing / Dressing",
    "Sweet Potatoes", "Vegetable Side", "Dinner Rolls", "Pumpkin Pie", "Whipped Cream", "Dessert", "Drinks"
  ]
};
const ALLOWED_ORIGINS = ["https://abbyandshajan.com", "https://www.abbyandshajan.com"];

function cors(request) {
  const origin = request.headers.get("Origin") || "";
  const ok = ALLOWED_ORIGINS.includes(origin) || /^https:\/\/[a-z0-9-]+\.github\.io$/i.test(origin);
  return {
    "Access-Control-Allow-Origin": ok ? origin : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin"
  };
}
function json(request, data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...cors(request) } });
}
function cleanName(s) {
  return String(s || "").replace(/[\u0000-\u001f<>]/g, "").replace(/\s+/g, " ").trim().slice(0, 40);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(request) });

    if (url.pathname === "/claims" && request.method === "GET") {
      const event = url.searchParams.get("event") || "";
      if (!EVENTS[event]) return json(request, { error: "Unknown event" }, 404);
      const { results } = await env.DB.prepare("SELECT dish, name FROM claims WHERE event = ?").bind(event).all();
      const claims = {};
      for (const r of results) claims[r.dish] = r.name;
      return json(request, { claims });
    }

    if (url.pathname === "/claim" && request.method === "POST") {
      let body;
      try { body = await request.json(); } catch { return json(request, { error: "Bad request" }, 400); }
      if (body.website) return json(request, { ok: true }); // honeypot field: bots fill it, people don't see it
      const event = String(body.event || ""), dish = String(body.dish || ""), name = cleanName(body.name);
      if (!EVENTS[event] || !EVENTS[event].includes(dish)) return json(request, { error: "That dish isn't on the list." }, 400);
      if (name.length < 2) return json(request, { error: "Please enter your name." }, 400);
      const res = await env.DB.prepare("INSERT INTO claims (event, dish, name) VALUES (?, ?, ?) ON CONFLICT(event, dish) DO NOTHING")
        .bind(event, dish, name).run();
      if (!res.meta.changes) {
        const row = await env.DB.prepare("SELECT name FROM claims WHERE event = ? AND dish = ?").bind(event, dish).first();
        return json(request, { error: "Someone just claimed that one.", by: row && row.name }, 409);
      }
      return json(request, { ok: true, dish, name });
    }

    return json(request, { error: "Not found" }, 404);
  }
};
