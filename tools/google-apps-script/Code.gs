// Thomas family site: lets Rocky (the site's chat helper) ADD events to the Family calendar.
// It can only add events. It cannot read, change or delete anything.
// Deploy: Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone.

const FAMILY_CALENDAR_ID = 'family06855826713832414617@group.calendar.google.com';
const SHARED_SECRET = 'SET-IN-GOOGLE-APPS-SCRIPT-ONLY'; // must match the CAL_WRITE_TOKEN secret on the Cloudflare worker

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents || '{}');
    if (body.secret !== SHARED_SECRET) return reply({ ok: false, error: 'unauthorized' });
    const title = String(body.title || '').slice(0, 100).trim();
    const location = String(body.location || '').slice(0, 150).trim();
    const m = String(body.date || '').match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if (!title || !m) return reply({ ok: false, error: 'bad event' });
    const cal = CalendarApp.getCalendarById(FAMILY_CALENDAR_ID);
    const note = 'Added via Rocky on abbyandshajan.com';
    let ev;
    if (!body.time) {
      ev = cal.createAllDayEvent(title, new Date(+m[1], +m[2] - 1, +m[3]), { location: location, description: note });
    } else {
      const t = String(body.time).match(/^(\d{1,2}):(\d{2})$/);
      if (!t) return reply({ ok: false, error: 'bad time' });
      const start = new Date(+m[1], +m[2] - 1, +m[3], +t[1], +t[2]);
      const mins = Math.min(Math.max(+body.durationMinutes || 60, 15), 720);
      ev = cal.createEvent(title, start, new Date(start.getTime() + mins * 60000), { location: location, description: note });
    }
    return reply({ ok: true, id: ev.getId() });
  } catch (err) {
    return reply({ ok: false, error: String(err).slice(0, 200) });
  }
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
