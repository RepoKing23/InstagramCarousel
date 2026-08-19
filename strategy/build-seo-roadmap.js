/**
 * Builds strategy/seo-roadmap-6-month.docx — the client-facing local SEO,
 * website and Instagram plan for Luxury Beauty by Cleo R.
 *
 * Six months, 17 Aug 2026 to 14 Feb 2027. The website build is approved: design
 * runs the week of 24 Aug, sign-off 31 Aug, build starts 1 Sep, launch the week
 * of 5 Oct. Keep this document and strategy/build-seo-tracker.py in step —
 * every task in the tracker traces back to a section here.
 *
 * Run from the repo root:
 *   npm install docx
 *   node strategy/build-seo-roadmap.js
 *
 * Everything in the document is sourced from the client onboarding form or from
 * research recorded in the "Where you stand today" section. No invented search
 * volumes, no invented pricing. Keep it that way when editing.
 */

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, HeadingLevel, PageBreak,
  LevelFormat, convertInchesToTwip,
} = require('docx');

const REPO = path.resolve(__dirname, '..');
const OUT = path.join(REPO, 'strategy', 'seo-roadmap-6-month.docx');

// Palette lifted from design/botox-myths.html so the document sits alongside
// her carousels rather than looking like a stranger's report.
const INK = '2E2A23';
const GOLD = 'C9A85C';
const GOLD_DARK = 'B99753';
const CREAM = 'F3EEE5';
const CREAM_DEEP = 'E5DCCA';
const MUTED = '6E6557';

const SERIF = 'Georgia';
const SANS = 'Calibri';

const CONTENT_W = 10080; // Letter (12240) minus 1080 twip margins each side

// ---------------------------------------------------------------- primitives

const label = (text) => new Paragraph({
  spacing: { before: 360, after: 80 },
  children: [new TextRun({
    text: text.toUpperCase(), font: SANS, size: 16, bold: true,
    color: GOLD_DARK, characterSpacing: 60,
  })],
});

const h1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 80, after: 200 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 8 } },
  children: [new TextRun({ text, font: SERIF, size: 36, bold: true, color: INK })],
});

const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 280, after: 100 },
  children: [new TextRun({ text, font: SERIF, size: 25, bold: true, color: INK })],
});

const h3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  spacing: { before: 200, after: 60 },
  children: [new TextRun({ text, font: SANS, size: 21, bold: true, color: INK })],
});

const p = (text, opts = {}) => new Paragraph({
  spacing: { after: opts.after ?? 140, line: 300 },
  children: runs(text, opts),
});

// Inline **bold** so the copy below stays readable as prose.
function runs(text, opts = {}) {
  const base = {
    font: opts.font ?? SANS,
    size: opts.size ?? 21,
    color: opts.color ?? INK,
    italics: opts.italics ?? false,
  };
  return text.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map((chunk) => {
    const bold = chunk.startsWith('**') && chunk.endsWith('**');
    return new TextRun({ ...base, text: bold ? chunk.slice(2, -2) : chunk, bold });
  });
}

const bullet = (text, level = 0) => new Paragraph({
  numbering: { reference: 'dot', level },
  spacing: { after: 70, line: 300 },
  children: runs(text),
});

const quietNote = (text) => new Paragraph({
  spacing: { before: 120, after: 200, line: 300 },
  indent: { left: 220 },
  border: { left: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 10 } },
  children: runs(text, { italics: true, color: MUTED, size: 20 }),
});

function td(text, widthDxa, { header = false, bold = false, bg } = {}) {
  return new TableCell({
    width: { size: widthDxa, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: bg ?? (header ? CREAM_DEEP : 'FFFFFF'), color: 'auto' },
    margins: { top: 90, bottom: 90, left: 130, right: 130 },
    children: [new Paragraph({
      spacing: { after: 0, line: 270 },
      children: text.split('\n').length > 1
        ? runs(text.replace(/\n/g, ' '), { size: 19 })
        : [new TextRun({
          text, font: SANS, size: header ? 18 : 19,
          bold: header || bold, color: INK,
        })],
    })],
  });
}

function table(widths, rows) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: CREAM_DEEP },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: CREAM_DEEP },
      left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
      right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: CREAM_DEEP },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
    },
    rows: rows.map((cells, ri) => new TableRow({
      tableHeader: ri === 0,
      children: cells.map((text, ci) => td(text, widths[ci], { header: ri === 0 })),
    })),
  });
}

const spacer = (after = 200) => new Paragraph({ spacing: { after }, children: [] });

// -------------------------------------------------------------- title page

const logo = fs.readFileSync(path.join(REPO, 'design', 'brand', 'logo-full.png'));

const titlePage = [
  spacer(700),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 340 },
    children: [new ImageRun({
      type: 'png', data: logo,
      transformation: { width: 105, height: 105 },
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 140 },
    children: [new TextRun({
      text: 'L O C A L   S E O   +   I N S T A G R A M',
      font: SANS, size: 17, bold: true, color: GOLD_DARK,
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 90 },
    children: [new TextRun({
      text: 'Getting Found in Oakville',
      font: SERIF, size: 54, bold: true, color: INK,
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({
      text: 'A six-month plan for Luxury Beauty by Cleo R.',
      font: SERIF, size: 26, italics: true, color: MUTED,
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 300 },
    border: { top: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 12 } },
    children: [],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({ text: '17 August 2026 – 14 February 2027', font: SANS, size: 21, color: INK })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({
      text: 'Prepared for Cleo Rukovo, NP  ·  3060 Preserve Drive, Oakville, Ontario',
      font: SANS, size: 19, color: MUTED,
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Prepared by ______________________', font: SANS, size: 19, color: MUTED })],
  }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ------------------------------------------------------------------ content

const body = [];

// ---- 1. Where you stand today
body.push(label('Section one'));
body.push(h1('Where you stand today'));
body.push(p('We looked you up the way a woman in Oakville would if a friend mentioned your name: searched, clicked through, read the reviews, tried the website. Some of what follows is not in your onboarding form. It is better that you hear it from us now than discover it in six months.'));

body.push(h2('Your website is not live yet'));
body.push(p('You own **luxurybeautybycleo.ca** and Google still holds old pages from it in its index. But the domain does not resolve. Nothing loads there. Anyone who clicks that link from a directory, from your Google listing, or from a search result lands on an error. Old pages in the index with no live site behind them is worse than having no domain at all, because the links exist and all of them fail.'));
body.push(p('That is being fixed. The build is approved, design runs the week of 24 August and the site goes live in early October. Section two has the dates. Until then your Google profile points at your booking link rather than at nothing.'));

body.push(h2('You share an address with a direct competitor'));
body.push(p('3060 Preserve Drive is **Allure Laser & Skin Studio**, twenty-two years in business, roughly 168 reviews, and they offer Botox and fillers as well. Google is deliberately careful about showing two businesses in the same category at the same address. It usually picks one and quietly filters the other. Right now the one it picks is not you.'));
body.push(p('This is workable. It does mean your Google profile needs to be built as a distinct practitioner listing with its own suite designation and its own category set, rather than a second version of Allure. That is the first real piece of work in this plan and it starts this week.'));

body.push(h2('Your postal code is wrong almost everywhere'));
body.push(p('Your listings carry **L6M 4L9**. The postal code for 3060 Preserve Drive is **L6M 0T9**. Google cross-checks address data across directories, and a mismatch like this weakens every listing you have. It is a small fix with a disproportionate effect, and it is most of what the rest of August is for.'));

body.push(h2('There are two of you, as far as your contact details are concerned'));
body.push(p('Your onboarding form gives crukovo@gmail.com. Your old website used luxury.beautyaestheticz@gmail.com. Your phone number is a 416 mobile rather than a local 905 or 289 line. Before we touch anything we need to know which email holds your Google Business Profile, because whoever controls that address controls the listing.'));

body.push(h2('Twelve reviews'));
body.push(p('Five stars, which is genuinely excellent and says something real about the work. But twelve of them. The Oakville clinics you are competing against sit between fifty and one hundred and seventy. Review count and review recency are among the strongest signals in local search, and this is the number you can move fastest without spending anything.'));

body.push(h2('Your hours are probably wrong'));
body.push(p('The only hours on record anywhere are Sunday, 12 to 5. If that is what your Google profile says, you are invisible six days a week to every person filtering for somewhere open now.'));

body.push(h2('Who you are actually up against'));
body.push(p('Skin Vitality Oakville, APT Medical Aesthetics, thepurglow, Sun & Shade Med Spa, Rejuuv Medi Spa, Impact Cosmetics, Fyxson Medical Aesthetics, Burlington Medical Aesthetics, and Allure at your own address. Several of these are multi-location operations with marketing budgets you will not match.'));
body.push(p('You are not going to outspend them. You can out-specific them. They are clinics with a menu. You are one nurse practitioner, in one town, doing a handful of treatments properly, with your licence on the line every time. That is a sharper story than any of them can tell, and local search rewards specificity.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 2. The website build
body.push(label('Section two'));
body.push(h1('The website build'));
body.push(p('The decision is made. A full site, built properly, on the domain you already own. This section exists so that everyone is working to the same dates, because half of this plan keys off them.'));

body.push(h2('What gets built'));
body.push(bullet('**Home and contact**, carrying the corrected address at L6M 0T9, your real hours, the booking link, and the structured data Google reads to understand what you are.'));
body.push(bullet('**A page per treatment**: lip filler, dermal filler and facial balancing, anti-wrinkle injections, skin boosters, dermaplaning, electrolysis, Belkyra. One page, one job, one search it is trying to win.'));
body.push(bullet('**An Oakville and surrounding-area page** covering Burlington, Milton, Mississauga, Glen Abbey, Joshua Creek and Bronte.'));
body.push(bullet('**Room to grow into**: articles answering real consult questions, a before-and-after gallery once the consent form is settled, and the weight-loss page ahead of that launch.'));

body.push(h2('The dates'));
body.push(p('**Planning and design run the week of 24 August. Sign-off is due Monday 31 August. The build starts 1 September.** Everything after the sign-off moves one-for-one with it, so that is the date to protect.'));
body.push(spacer(120));
body.push(table([2100, 4580, 3400], [
  ['When', 'What we do', 'What we need from you'],
  ['Aug 24 – 28', 'Planning and design. Sitemap, page inventory, wireframes for home, contact and the treatment template, the keyword-to-page map, brand kit', 'Registrar login, treatment list with pricing, photos of the room, headshot, logo files'],
  ['Aug 31', 'Design sign-off. Nothing is built before this clears', 'Sign off the wireframes and the look, in writing'],
  ['Sep 1 – 6', 'Build starts. Hosting sorted, DNS pointed, platform set up, page structure scaffolded', 'Nothing. This week is ours'],
  ['Sep 7 – 13', 'Home and contact complete in staging, with schema, title tags and meta descriptions', 'Read the home page copy and approve it'],
  ['Sep 14 – 27', 'Treatment pages: lip filler, dermal filler and facial balancing, anti-wrinkle injections, skin boosters. Internal linking, image compression, alt text', 'Read the copy and confirm every claim is one you can stand behind'],
  ['Sep 28 – Oct 4', 'Remaining treatment pages, the Oakville area page, mobile speed pass', 'Nothing. This week is ours'],
  ['Oct 5 – 11', 'Launch. Search Console verified, sitemap submitted, analytics running, Google profile repointed, every listing updated to the new URL', 'Final sign-off before it goes live'],
  ['Oct 12 – Nov 8', 'Indexing and on-page. Fix whatever Search Console flags, FAQ schema, the first three articles', 'The questions you get asked most in consults'],
  ['Nov 9 – Feb 14', 'Depth. Weight-loss page, gallery, five more articles, near-miss query work, technical audit, handover', 'Consent-cleared photos as they come'],
]));
body.push(spacer(160));
body.push(p('Two dates are worth writing on a wall. **31 August**, because the build cannot start without it. **5 October**, because that is launch week, and it gives the site four full months of indexing inside these six. A site that launches in October is a site Google has largely made its mind up about by February. That is the whole reason the build is not being left until later.'));

body.push(quietNote('One thing happens in the first week regardless of the build: your Google profile stops pointing at a domain that does not load. Until the site is live it points at your booking link, so nobody hits a dead end in the meantime.'));

body.push(p('Costs for the build are quoted separately: ______________________'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 3. Your daily routine
body.push(label('Section three'));
body.push(h1('Your daily routine'));
body.push(p('The rest of this document is what we do. This section is what **you** do, and it is short on purpose.'));
body.push(p('Five slots every weekday, six on a Wednesday. This is the part of the plan that compounds, and it is also the part that quietly stops happening around week nine if nobody has written it down. So it is written down, and it is on its own tab in the tracker with a box to tick for every slot on every day between now and February.'));
body.push(spacer(120));
body.push(table([2400, 2100, 5580], [
  ['Slot', 'When', 'What it actually means'],
  ['Google profile post', 'Every weekday', 'One post a day, rotating the five types across the week: treatment spotlight, FAQ or myth, before and after, offer or availability, practice update. Copy and images come from the content calendar. Every post ends with the booking link'],
  ['Instagram post or stories', 'Every weekday', 'A feed post on the calendar days, two or three stories on the rest. Oakville location tag every time, alt text every time, the local hashtag set every time'],
  ['Reel', 'Wednesday', 'One a week, filmed and cut in the Wednesday batch block. Rotate the four types across the month: a treatment in fifteen seconds, a myth-buster, behind the scenes in the room, a patient question answered to camera. Each cut is reused as a story and as a Google profile video'],
  ['On-page optimisation', 'Every weekday', 'Before launch this is preparation: keyword mapping, title tags, meta descriptions, page copy. After launch it is one real page improved a day, on rotation, so no page sits six months untouched'],
  ['Review ask', 'Every weekday', 'The WhatsApp message inside 24 hours to every patient seen that day, and a reply to any review that landed. The highest-return five minutes in this document'],
  ['Citations', 'Daily to week 4, then weekly', 'One directory a day claimed or corrected until the list is clean, then one a week to keep it clean'],
]));
body.push(spacer(160));

body.push(h2('Every week'));
body.push(bullet('**Monday.** Google profile insights and a rank check on the three target searches. Two minutes, written down.'));
body.push(bullet('**Wednesday.** Batch the content. Film the reel, write the week\'s posts and captions, so the daily slots are a five-minute publish rather than a blank page.'));
body.push(bullet('**Friday.** Log the week\'s numbers, close out the task list, flag anything blocked. Ad review every second Friday.'));

body.push(h2('Every month'));
body.push(bullet('Fill the metrics tab, comparing against the baseline rather than against last month.'));
body.push(bullet('Refresh the Google profile: services list, questions and answers, photos. A profile that never changes stops earning.'));
body.push(bullet('Check the three named competitors, and check which searches you are sitting just outside the first page for.'));
body.push(bullet('Look at the month\'s best posts and best pages, and do more of those.'));

body.push(quietNote('Both halves of this live in the tracker. The Daily Routine tab explains each slot; the Daily Log is the grid you tick, one row per weekday from 17 August to 12 February. Every column is a status dropdown — Done, Missed, or not applicable. There are no time targets on the sheet and nothing to stopwatch. The reel column is only live on Wednesdays, so a Tuesday with five ticks is a complete day.'));

body.push(p('One caution about the reel. Once a week, done properly, beats four a week done at midnight. If a Wednesday is impossible, move it, do not drop it.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 4. Month one
body.push(label('Section four'));
body.push(h1('Month one — fix what is broken, and design the site'));
body.push(p('**17 August to 13 September.** The rest of August is Google Business Profile and citations, and nothing else. It is unglamorous, it produces almost no visible result, and it is the highest-return work in the entire plan. The website planning happens alongside it in the week of 24 August.'));

body.push(h3('Google Business Profile — week one'));
body.push(bullet('Establish who owns the profile and under which email, then get it verified. Nothing else can happen until this is settled.'));
body.push(bullet('Correct the address to L6M 0T9 and add the suite designation, so you read as a practitioner inside the building rather than a duplicate of Allure.'));
body.push(bullet('Set your real hours. All of them, not just Sunday.'));
body.push(bullet('Choose a primary category, then secondary categories that deliberately avoid colliding head-on with Allure\'s laser and facial listing. Where you overlap, Google filters you out. Where you do not, you both show.'));
body.push(bullet('Replace the dead website link with the booking link, and add the booking link properly as a booking action.'));
body.push(bullet('Load real photos of the room, of you, of the space. Google puts photos front and centre in the map pack, and a listing without any reads as abandoned.'));

body.push(h3('Clean up your details everywhere else'));
body.push(bullet('Settle on one email and one phone number and use them everywhere without variation.'));
body.push(bullet('Audit every listing that mentions the practice first, so we know the size of the job before we start fixing it.'));
body.push(bullet('Correct L6M 4L9 to L6M 0T9 on Birdeye, Facebook, Fresha, Yelp.ca, Yellow Pages, Apple Maps, Bing Places, RateMDs and the Canadian chamber directories.'));
body.push(bullet('Claim any listing that exists about you but is not yours to control.'));
body.push(bullet('Then verify. A correction you did not check is a correction that did not happen.'));

body.push(h3('Website planning and design — week of 24 August'));
body.push(bullet('Sitemap and the full page inventory, agreed with you rather than presented to you.'));
body.push(bullet('The keyword-to-page map, so every page has exactly one search it is trying to win.'));
body.push(bullet('Wireframes for the home page, the contact page and the treatment page template.'));
body.push(bullet('Brand kit pulled from the work already done on your carousels, so the site and the Instagram look like the same practice.'));
body.push(bullet('Design review with you at the end of the week. Sign-off Monday 31 August.'));

body.push(h3('Set up the measuring instruments'));
body.push(bullet('Record the starting numbers: 12 reviews, 5.0 average, and whatever your Google profile currently shows for calls, views and direction requests. Everything after this is measured against that line.'));
body.push(bullet('Analytics configured and waiting, so there is history in place the day the site launches.'));
body.push(bullet('The daily routine starts in week one, before there is a site to optimise. The on-page slot goes into preparing the build.'));

body.push(quietNote('The one date this month that everything else waits on: design sign-off, Monday 31 August. If it slips a week, launch slips a week, and the site gets a month less indexing inside these six.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 5. Month two
body.push(label('Section five'));
body.push(h1('Month two — build it, and start the review engine'));
body.push(p('**14 September to 11 October.** The foundation is fixed. The site gets built and launched, and the thing that actually moves you up the map gets switched on.'));

body.push(h2('The review engine'));
body.push(p('This is the single highest-return activity in this document and it costs nothing but consistency. Going from twelve reviews to thirty over six months changes how Google ranks you and changes how people choose you.'));
body.push(bullet('A short, specific ask sent over WhatsApp within 24 hours of the appointment, while she is still pleased. WhatsApp because it is the channel you already use and the one people actually answer.'));
body.push(bullet('A card with a QR code in the treatment room, so the ask is not always coming from you personally.'));
body.push(bullet('A target of eighteen to twenty-two new Google reviews across the six months. That is roughly one every ten days, achievable without ever making it awkward.'));
body.push(bullet('Every review gets a reply, including the good ones, within a couple of days. Replies are visible to everyone reading and they are a ranking signal in their own right.'));
body.push(bullet('One caution: never offer anything in exchange for a review. It breaches Google\'s terms and it is a problem under the College of Nurses\' advertising rules. The ask has to be clean.'));

body.push(h2('The site'));
body.push(bullet('Treatment pages built and copy approved: lip filler, dermal filler and facial balancing, anti-wrinkle injections, skin boosters, then dermaplaning, electrolysis and Belkyra.'));
body.push(bullet('Address, phone and hours in the footer of every page, matching your listings exactly.'));
body.push(bullet('Structured data marking you as a local medical business, so Google can read your address, hours and treatments without guessing.'));
body.push(bullet('Internal linking, image compression, alt text and a mobile speed pass before anything goes live.'));
body.push(bullet('**Launch, week of 5 October.** Search Console verified, sitemap submitted, analytics confirmed running, the Google profile repointed, and every directory updated to the new URL on the same day.'));

body.push(h2('Google profile, worked daily now'));
body.push(bullet('The services list filled out with each treatment and a plain description.'));
body.push(bullet('The questions section seeded with the questions you genuinely get asked, answered properly.'));
body.push(bullet('A post every weekday from the content calendar. No new production. The material exists, it just needs putting where Google can see it.'));

body.push(h2('Ads'));
body.push(bullet('Local radius audience, roughly 15km around Oakville, taking most of the budget.'));
body.push(bullet('Retargeting on anyone who engaged in the last 30 days. The cheapest bookings you will get.'));
body.push(bullet('A lookalike built from your patient list once you can export it.'));
body.push(bullet('Three or four creatives at once, pulled from carousels you already have. You are looking for the outlier and you cannot find it without something to compare against.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 6. Month three
body.push(label('Section six'));
body.push(h1('Month three — indexing, on-page and local links'));
body.push(p('**12 October to 8 November.** The site is live. This month is about getting Google to read it properly and getting other Oakville websites to mention it.'));
body.push(bullet('Confirm every page is indexed in Search Console, and fix whatever is not. A page Google has not seen is a page that does not exist.'));
body.push(bullet('On-page passes on the home page first, then the four highest-intent treatment pages: title, H1, opening copy, internal links.'));
body.push(bullet('FAQ blocks with FAQ schema on every treatment page, written from real consult questions rather than invented ones.'));
body.push(bullet('Local mentions and links: Oakville business directories, Halton-area partners, and a cross-link with Allure if that relationship allows it. Being mentioned on other Oakville websites is what tells Google you are genuinely of this town.'));
body.push(bullet('The weight-loss launch you flagged: a service entry on your Google profile now, so it has age on it before you start promoting it.'));
body.push(bullet('The first three articles, each linked to the treatment page it relates to.'));
body.push(bullet('First real read on the numbers: Search Console impressions, which queries you are appearing for, and a rank check on the map pack terms.'));

body.push(spacer(160));

// ---- 7. Month four
body.push(label('Section seven'));
body.push(h1('Month four — depth on the pages that earn'));
body.push(p('**9 November to 6 December.** Nothing new gets started. What exists gets deeper, and the thin pages get filled in.'));
body.push(bullet('Expand the thin treatment pages: pricing ranges, aftercare, and an honest paragraph on who the treatment is not for. That last one converts better than anything else on the page.'));
body.push(bullet('The weight-loss pre-launch page, and a refreshed Google profile photo set.'));
body.push(bullet('A before-and-after gallery, using consent-cleared photos only, with a compliance pass before it goes live.'));
body.push(bullet('Articles four, five and six, from the consult questions you have been collecting.'));
body.push(bullet('An internal linking pass now that there are articles to link from.'));
body.push(bullet('One Oakville community listing, sponsorship or event. Local links are earned in person more often than online.'));
body.push(bullet('The holiday review push: ask every patient seen in November, while December is still ahead of you.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 8. Month five
body.push(label('Section eight'));
body.push(h1('Month five — hold the cadence through the holidays'));
body.push(p('**7 December to 10 January.** This is the month plans like this one usually die. The work drops to something sustainable rather than stopping, because two quiet weeks in December costs more than it looks like it should.'));
body.push(bullet('Holiday opening hours set on the Google profile for December and January, then checked on an actual search to confirm they show correctly.'));
body.push(bullet('Gift-card and holiday content planned in advance, and a holiday offer block on the home page.'));
body.push(bullet('Ad budget moved to the gift-card creative for the fortnight it works, then moved back.'));
body.push(bullet('Between Christmas and New Year, reduced cadence: stories rather than feed posts, one reel, but **keep posting to the Google profile every weekday**. That slot is five minutes and it is the one that holds the map position.'));
body.push(bullet('A year-end read on everything, and the January content calendar planned before January starts.'));
body.push(bullet('Back to full cadence the first week of January, with new-year treatment content and a review push while people are making plans.'));

body.push(spacer(160));

// ---- 9. Month six
body.push(label('Section nine'));
body.push(h1('Month six — compound it, then plan the next six'));
body.push(p('**11 January to 14 February.** The last month is not new work. It is finding what nearly worked and pushing it over the line.'));
body.push(bullet('A full query review in Search Console: every term you rank between five and fifteen for. Those are the pages a fortnight of work turns into first-page pages.'));
body.push(bullet('Optimise the pages behind those near-miss terms, and refresh the three lowest performers.'));
body.push(bullet('The full weight-loss treatment page, now the service is live.'));
body.push(bullet('A second round of local link approaches, with six months of results behind the ask.'));
body.push(bullet('A technical audit: speed, schema, broken links, redirects.'));
body.push(bullet('The six-month report against the week-one baseline, a recommendation for the next six months, and handover of the site documentation and every login.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 10. Keywords
body.push(label('Section ten'));
body.push(h1('What we would rank you for'));
body.push(p('These are the searches worth owning in your catchment, and what would have to exist for you to appear in them. The timings assume launch in the week of 5 October.'));
body.push(spacer(120));
body.push(table([3200, 3400, 3480], [
  ['Search', 'What would rank for it', 'Realistic by 14 February?'],
  ['botox oakville', 'Google profile (map pack)', 'Map pack from month two. Organic from around December'],
  ['lip filler oakville', 'Treatment page', 'Competitive. Ranking by February, first page not guaranteed'],
  ['nurse injector oakville', 'Google profile + treatment page', 'Strong fit and your least contested term. Expect it'],
  ['skin booster oakville', 'Treatment page', 'Low competition. Expect it'],
  ['dermaplaning oakville', 'Treatment page', 'Low competition. Expect it'],
  ['electrolysis oakville', 'Treatment page', 'Low competition, and your reviews already mention this. Expect it'],
  ['med spa near me', 'Google profile', 'Depends entirely on resolving the Allure filtering'],
  ['"how much is lip filler in oakville" and similar', 'Article or FAQ', 'From month four onward, as the articles age'],
]));
body.push(quietNote('A note on honesty: we have not attached monthly search volumes to these. Our keyword data subscription was out of credits at the time of writing, and we would rather show you nothing than show you a number we made up. Volumes get validated and added before we commit to targets. It does not hold up any of the work above.'));

body.push(p('The pattern in that right-hand column is why the build is not being deferred. The map pack is winnable this autumn with the Google profile alone. Everything underneath it needs pages, and pages need time.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 11. Compliance
body.push(label('Section eleven'));
body.push(h1('What we can and cannot say'));
body.push(p('This section exists because you are a nurse practitioner in Ontario, not a retail business, and the rules that apply to you are stricter than the ones your competitors appear to follow. We would rather you rank a little slower than put your licence in play.'));

body.push(h2('Health Canada'));
body.push(p('Botox is a prescription drug in Canada. Advertising a prescription drug directly to the public is restricted to name, price and quantity. You may not describe what it does or what it achieves. That is a real constraint and most Oakville clinics are ignoring it.'));
body.push(h3('So instead of'));
body.push(bullet('"Botox softens lines and leaves you looking rested"'));
body.push(bullet('"Botox vs Dysport: the real difference"'));
body.push(h3('We write'));
body.push(bullet('"Anti-wrinkle injections" or "wrinkle relaxing treatment" when describing what a treatment does'));
body.push(bullet('Brand names only where they carry no benefit claim, or inside genuine educational content rather than advertising'));

body.push(h2('The College of Nurses of Ontario'));
body.push(bullet('No guarantees of outcome.'));
body.push(bullet('No superiority claims. No "best injector in Oakville", no "Oakville\'s number one".'));
body.push(bullet('Before-and-after images must be honest, consented, and not misleading about typical results.'));
body.push(bullet('Risks and realistic outcomes disclosed rather than glossed over.'));

body.push(h2('This applies to the daily posting too'));
body.push(p('It is worth saying plainly, because the daily routine puts a post on your Google profile every weekday and a reel up every Wednesday, and those are advertising in exactly the way an Instagram caption is. **The same rules apply to a Google post, a reel script, a page title and a meta description as apply to a carousel.** Speed is where compliance usually slips, and the daily slots are the fast ones.'));

body.push(h2('What this means for the content already scheduled'));
body.push(p('Your Instagram calendar runs to 65 posts. **Twenty-one of them name Botox or Dysport in the headline, hook or caption**, and fourteen carry Botox hashtags. Most pair the brand name with a description of its effect, which is exactly the combination Health Canada restricts.'));
body.push(p('None of that content is wasted. The ideas are good and the design work is done. It needs a compliance pass on the wording: brand names swapped for treatment descriptions, benefit claims rephrased. We would scope that separately once you have read this and decided how cautious you want to be.'));
body.push(quietNote('There is an upside here worth naming. "The injector who follows the rules" is a genuinely differentiating position in a market where most do not, and it is the same message as the content you have already built: honest, careful, no shortcuts. The compliant version of your marketing is also the more persuasive version.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 12. Instagram
body.push(label('Section twelve'));
body.push(h1('Instagram'));
body.push(p('You already have a content system and section three covers what gets posted and when. This section is about two things the daily routine does not: making the account findable, and paying to put the best of it in front of the right women in Oakville.'));

body.push(h2('The profile as a search surface'));
body.push(p('Instagram is a search engine that most clinics treat as a scrapbook. These are one-off fixes, done in the last week of August, and then they keep working.'));
body.push(bullet('**The name field**, not the username. This is what Instagram search actually indexes. It should read along the lines of "Cleo | Nurse Injector Oakville". Right now that field is doing nothing for you.'));
body.push(bullet('**The bio** names the town and the treatments in plain language, then gives one instruction.'));
body.push(bullet('**Hashtags weighted local** rather than global. #oakvillemedspa and #oakvilleaesthetics put you in front of people who could actually book with you. #botox puts you in a feed with millions of posts where nobody will ever see yours. Keep the local tags clear of prescription brand names, for the reasons in section eleven.'));
body.push(bullet('**Highlights organised by treatment**, so a stranger can find what you do in one tap.'));
body.push(bullet('**A link that works.** Right now, if it points at the domain, it points at nothing. It goes to the booking link until October, then to the site.'));

body.push(h2('Paid'));
body.push(p('You told us most patients already come from Instagram and Google ads, so this is not a new channel. It is a channel to run properly.'));

body.push(h3('Audiences'));
body.push(bullet('**Local radius.** Women within roughly 15km of Oakville. Your form left the age range blank, so we would start at 28 to 55 and narrow it against who actually books. This is the core audience and it should take most of the budget.'));
body.push(bullet('**Retargeting.** Anyone who engaged with the account or watched a video in the last 30 days. Cheapest bookings you will get, every time.'));
body.push(bullet('**Lookalike.** Built from your existing patient list once you can export it from your booking system. Worth doing after the first two are running, not before.'));

body.push(h3('Creative'));
body.push(bullet('Pull directly from the carousels already produced, and from the Wednesday reels once there are a few of them. Testing them as ads tells you which topics are worth more of your budget organically too.'));
body.push(bullet('Run three or four at once, not one. You are looking for the outlier, and you cannot find it without something to compare against.'));
body.push(bullet('Face-to-camera tends to beat graphics for a practice built on one person. You are the product, which is also the argument for the weekly reel.'));

body.push(h3('The flow'));
body.push(p('Ad to DM to consultation, matching the "DM to book" call to action already in your content. From October the ads can land on a real page instead, which is when the cost per booking should start to move.'));

body.push(h3('Budget and testing'));
body.push(bullet('Your onboarding form did not include current ad spend, so we need that number before recommending a figure. What we can say is the structure: a fixed monthly budget split roughly 70 / 20 / 10 across local radius, retargeting and lookalike.'));
body.push(bullet('Review every fortnight. Kill anything below the account average on cost per DM. Move that money to whatever is beating it. Nothing runs unchanged for a month.'));
body.push(bullet('Judge ads on DMs and bookings, not likes. Reach is not the point.'));

body.push(quietNote('How the halves of this plan connect: ads produce DMs, DMs become appointments, appointments feed the review engine, reviews lift you in the map pack, and the map pack sends people to a site that is finally worth landing on. Paid and organic are not separate programmes here. The paid work is what makes the local SEO compound faster than it would on its own.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 13. What we need
body.push(label('Section thirteen'));
body.push(h1('What we need from you'));
body.push(p('Most of the delay in work like this comes from waiting on access. These are in date order, and the first five are what the build waits on.'));
body.push(spacer(120));
body.push(table([2100, 5580, 2400], [
  ['Needed by', 'What we need', 'Type'],
  ['Fri 21 Aug', 'Google Business Profile, and confirmation of which email holds it', 'Access'],
  ['Fri 21 Aug', 'Your real opening hours, every day of the week', 'Answer'],
  ['Fri 21 Aug', 'Your agreement to the daily routine in section three', 'Answer'],
  ['Sun 23 Aug', 'Whether your arrangement with Allure allows your own signage and suite designation', 'Answer'],
  ['Sun 23 Aug', 'The three local competitors you most want to be measured against', 'Answer'],
  ['Wed 26 Aug', 'Treatment list with current pricing', 'Asset'],
  ['Fri 28 Aug', 'Domain registrar login for luxurybeautybycleo.ca', 'Access'],
  ['Fri 28 Aug', 'Photos of the treatment room and the space, and a current headshot', 'Asset'],
  ['Fri 28 Aug', 'Logo files and any brand assets you already have', 'Asset'],
  ['Fri 28 Aug', 'Instagram collaborator invitation (we do not need your password)', 'Access'],
  ['Mon 31 Aug', 'DESIGN SIGN-OFF on the wireframes and the look', 'Answer'],
  ['Sun 6 Sep', 'Your signed before-and-after consent form', 'Asset'],
  ['Sun 6 Sep', 'Your booking system login, whichever system it is', 'Access'],
  ['Sun 13 Sep', 'Approval of the home page copy', 'Answer'],
  ['Sun 13 Sep', 'What you currently spend on Instagram and Google ads each month', 'Answer'],
  ['Sun 13 Sep', 'Your ideal patient, described in a sentence or two in your own words', 'Answer'],
  ['Sun 20 Sep', 'Meta Business account and ad account', 'Access'],
  ['Sun 27 Sep', 'Approval of the treatment page copy', 'Answer'],
  ['Sun 18 Oct', 'The questions you get asked most in consults', 'Answer'],
]));
body.push(spacer(160));
body.push(p('The same list is on the **Waiting On Cleo** tab of the tracker, where anything past its date turns red on its own.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 14. Measurement
body.push(label('Section fourteen'));
body.push(h1('How we will measure it'));
body.push(p('Reported monthly against the starting point, in this order of importance. Six checkpoints: end of September, October, November, December, January, and a final read on 14 February.'));
body.push(spacer(120));
body.push(table([3400, 3200, 3480], [
  ['What we track', 'Where it starts', 'Where we want it by 14 February'],
  ['Google reviews', '12, averaging 5.0', '30 to 34, still at or near 5.0'],
  ['Calls and direction requests from Google', 'To be baselined in week one', 'Up every month, with the trend line mattering more than the number'],
  ['Map pack position for the target searches', 'To be baselined in week one', 'Visible for "nurse injector oakville" and "botox oakville"'],
  ['Google profile posts published', 'None', 'Twenty or more a month, every month'],
  ['Instagram profile visits and link taps', 'To be baselined in week one', 'Up, with taps rising faster than visits'],
  ['Reels published', 'None', 'Four a month, one a week'],
  ['DMs and booked consultations', 'Not currently tracked', 'Tracked from week one, attributed to source'],
  ['Website sessions and Search Console impressions', 'No site', 'Rising month on month from the October launch'],
  ['Daily slot completion rate', 'Nothing logged', '85 per cent or better across the six months'],
]));
body.push(spacer(200));
body.push(p('One honest expectation to set. Local search moves slowly and most of the first month produces no visible result at all. It is repair work. The reviews will move first, usually around week six. Map position follows the reviews. The site\'s rankings arrive last: it launches in October, Google spends a month or two making up its mind, and the real organic numbers land in January and February. Anyone promising you faster than that is selling you something.'));
body.push(p('That is also the argument for the six months rather than three. Ninety days would have ended the week the site started ranking.'));

// ------------------------------------------------------------------- assemble

const doc = new Document({
  creator: 'Luxury Beauty by Cleo R. growth plan',
  title: 'Getting Found in Oakville: Six-Month Local SEO, Website and Instagram Plan',
  description: 'Six-month local SEO, website and Instagram roadmap for Luxury Beauty by Cleo R., Oakville, Ontario',
  numbering: {
    config: [{
      reference: 'dot',
      levels: [
        {
          level: 0, format: LevelFormat.BULLET, text: '•',
          alignment: AlignmentType.LEFT,
          style: {
            paragraph: { indent: { left: 360, hanging: 220 } },
            run: { color: GOLD_DARK },
          },
        },
        {
          level: 1, format: LevelFormat.BULLET, text: '◦',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 220 } } },
        },
      ],
    }],
  },
  styles: {
    default: {
      document: { run: { font: SANS, size: 21, color: INK } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1180, right: 1080, bottom: 1080, left: 1080 },
      },
    },
    children: [...titlePage, ...body],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log(`wrote ${path.relative(REPO, OUT)} (${(buf.length / 1024).toFixed(0)} KB)`);
});
