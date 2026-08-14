/**
 * Builds strategy/seo-roadmap-90-day.docx — the client-facing local SEO and
 * Instagram plan for Luxury Beauty by Cleo R.
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
const OUT = path.join(REPO, 'strategy', 'seo-roadmap-90-day.docx');

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
      text: 'A 90-day plan for Luxury Beauty by Cleo R.',
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
    children: [new TextRun({ text: 'September – November 2026', font: SANS, size: 21, color: INK })],
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

body.push(h2('Your website is not live'));
body.push(p('You own **luxurybeautybycleo.ca** and Google still holds old pages from it in its index. But the domain does not resolve. Nothing loads there. Anyone who clicks that link from a directory, from your Google listing, or from a search result lands on an error. Old pages in the index with no live site behind them is worse than having no domain at all, because the links exist and all of them fail.'));

body.push(h2('You share an address with a direct competitor'));
body.push(p('3060 Preserve Drive is **Allure Laser & Skin Studio**, twenty-two years in business, roughly 168 reviews, and they offer Botox and fillers as well. Google is deliberately careful about showing two businesses in the same category at the same address. It usually picks one and quietly filters the other. Right now the one it picks is not you.'));
body.push(p('This is workable. It does mean your Google profile needs to be built as a distinct practitioner listing with its own suite designation and its own category set, rather than a second version of Allure. That decision is the first real piece of work in this plan.'));

body.push(h2('Your postal code is wrong almost everywhere'));
body.push(p('Your listings carry **L6M 4L9**. The postal code for 3060 Preserve Drive is **L6M 0T9**. Google cross-checks address data across directories, and a mismatch like this weakens every listing you have. It is a small fix with a disproportionate effect.'));

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

// ---- 2. The website decision
body.push(label('Section two'));
body.push(h1('The website decision'));
body.push(p('Almost everything below depends on one choice, so it comes first. There are three honest options and they buy different things.'));

body.push(h3('Path A — no website this quarter'));
body.push(p('We work Google Business Profile, reviews, citations and Instagram only.'));
body.push(bullet('What you get: a properly built map listing, review growth, and Instagram driving bookings through DMs.'));
body.push(bullet('Where it stops: you can appear in the map pack at the top of a local search, but never in the ordinary results underneath it. Ad traffic has nowhere to land except your Instagram profile. Every directory listing keeps pointing at a domain that does not load.'));

body.push(h3('Path B — one page, live in two weeks'));
body.push(p('A single page on the domain you already own: name, address, phone, hours, treatment list, booking link, and the structured data Google reads to understand what you are.'));
body.push(bullet('What you get: the dead link problem gone, a real destination for ads, and consistency across every listing that mentions you.'));
body.push(bullet('Where it stops: one page will not rank for individual treatments. It is a floor, not a strategy.'));

body.push(h3('Path C — the full site'));
body.push(p('A page for each treatment you want to be found for, service-area content covering Oakville and the towns around it, and room to add articles later.'));
body.push(bullet('What you get: the only version of this plan that competes for searches like "lip filler Oakville" in the organic results, not just the map.'));
body.push(bullet('Where it stops: it takes roughly six weeks to build and another month before Google settles on where to rank it.'));

body.push(h3('What we recommend'));
body.push(p('**Path B is the floor and Path C is the goal.** If the budget is not there for a full build this quarter, do Path B anyway. A registered domain that fails to load is not neutral. It is actively costing you every click that reaches it.'));

body.push(quietNote('Whatever you decide, one thing happens in week one regardless: your Google profile stops pointing at a domain that does not load. Until something is live we will point it at your Instagram or your booking link so no one hits a dead end.'));

body.push(h2('If you approve the build, here is the timeline'));
body.push(p('Weeks are counted from the day you say yes, not from the start of the quarter, because the decision date is yours.'));
body.push(spacer(120));
body.push(table([1500, 5180, 3400], [
  ['Week', 'What we do', 'What we need from you'],
  ['1', 'Hosting sorted, DNS pointed at the new site, platform set up, page structure agreed', 'Domain registrar access, final treatment list and pricing'],
  ['2', 'Home and contact pages live with the correct address (L6M 0T9), real hours, booking link and structured data. Under Path B this is where it ends and you are live', 'Photos of the room and of you, headshot, logo files'],
  ['3–4', 'Treatment pages built: lip filler, dermal filler and facial balancing, anti-wrinkle injections, skin boosters, dermaplaning, electrolysis, Belkyra', 'Read the copy and confirm every claim is one you can stand behind'],
  ['5', 'Oakville and surrounding-area content, internal linking, mobile speed pass, Google profile repointed to the live site', 'Nothing. This week is ours'],
  ['6', 'Launch. Search Console verified, sitemap submitted, analytics running, every directory listing updated to the new address', 'Final sign-off'],
  ['7–12', 'Indexing and iteration. Articles answering the questions patients actually ask, and the weight-loss page ahead of that launch', 'The questions you get asked most in consults'],
]));
body.push(spacer(160));
body.push(p('If you decide in week two of the quarter as scheduled, the site is live around week eight and gets roughly a month of indexing inside these ninety days. Decide later than that and launch falls outside the quarter. That is not a scare tactic, it is just the arithmetic of how long Google takes.'));
body.push(p('Costs for each path are quoted separately: ______________________'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 3. Month one
body.push(label('Section three'));
body.push(h1('Month one — fix what is broken'));
body.push(p('**Weeks 1 to 4.** None of this needs a website, so it starts immediately regardless of what you decide above. This month is unglamorous and it is the highest-return work in the entire plan.'));

body.push(h3('Google Business Profile'));
body.push(bullet('Establish who owns the profile and under which email, then get it verified. Nothing else can happen until this is settled.'));
body.push(bullet('Correct the address to L6M 0T9 and add the suite designation so you read as a practitioner inside the building rather than a duplicate of Allure.'));
body.push(bullet('Set your real hours. All of them, not just Sunday.'));
body.push(bullet('Choose a primary category, then secondary categories that deliberately avoid colliding head-on with Allure\'s laser and facial listing. Where you overlap, Google filters you out. Where you do not, you both show.'));
body.push(bullet('Add a working booking link and replace the dead website link.'));
body.push(bullet('Load real photos of the room, of you, of the space. Google puts photos front and centre in the map pack, and a listing without any reads as abandoned.'));

body.push(h3('Clean up your details everywhere else'));
body.push(bullet('Settle on one email and one phone number and use them everywhere without variation.'));
body.push(bullet('Correct L6M 4L9 to L6M 0T9 on Birdeye, Facebook, Fresha, Yelp.ca, Yellow Pages, Apple Maps, Bing Places, RateMDs and the Canadian chamber directories.'));
body.push(bullet('Claim any listing that exists about you but is not yours to control.'));

body.push(h3('Set up the measuring instruments'));
body.push(bullet('Google Search Console and analytics go up this month even if there is no site yet, so there is history in place the day one launches.'));
body.push(bullet('Record the starting numbers: 12 reviews, 5.0 average, and whatever your Google profile currently shows for calls and direction requests. Everything after this is measured against that line.'));

body.push(quietNote('Decision due in week two: the website. Month two branches depending on your answer.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 4. Month two
body.push(label('Section four'));
body.push(h1('Month two — reviews, and pages if you want them'));
body.push(p('**Weeks 5 to 8.** The foundation is fixed. Now we build the thing that actually moves you up the map.'));

body.push(h2('The review engine'));
body.push(p('This is the single highest-return activity in this document and it costs nothing but consistency. Going from twelve reviews to twenty-two over a quarter changes how Google ranks you and changes how people choose you.'));
body.push(bullet('A short, specific ask sent over WhatsApp within 24 hours of the appointment, while she is still pleased. WhatsApp because it is the channel you already use and the one people actually answer.'));
body.push(bullet('A card with a QR code in the treatment room, so the ask is not always coming from you personally.'));
body.push(bullet('A target of eight to ten new Google reviews this quarter. That is roughly one every ten days, achievable without ever making it awkward.'));
body.push(bullet('Every review gets a reply, including the good ones, within a couple of days. Replies are visible to everyone reading and they are a ranking signal in their own right.'));
body.push(bullet('One caution: never offer anything in exchange for a review. It breaches Google\'s terms and it is a problem under the College of Nurses\' advertising rules. The ask has to be clean.'));

body.push(h2('Google profile, worked weekly'));
body.push(bullet('A post a week, pulled straight from the carousels already built in your content calendar. No new production. The material exists, it just needs reposting where Google can see it.'));
body.push(bullet('Fill out the services list with each treatment and a plain description.'));
body.push(bullet('Seed the questions section with the questions you genuinely get asked, and answer them properly.'));

body.push(h2('If you approved the site'));
body.push(bullet('One page per treatment: lip filler, dermal filler and facial balancing, anti-wrinkle injections, skin boosters, dermaplaning, electrolysis, Belkyra.'));
body.push(bullet('Address, phone and hours in the footer of every page, matching your listings exactly.'));
body.push(bullet('Structured data marking you as a local medical business, so Google can read your address, hours and treatments without guessing.'));
body.push(bullet('A service-area section covering Oakville plus Burlington, Milton, Mississauga, Glen Abbey, Joshua Creek and Bronte.'));

body.push(h2('If you did not'));
body.push(p('That effort goes into Instagram instead. Your Highlights become the treatment menu, one Highlight per service, each opening with what it is, who it suits and what it costs. It is a worse version of a website, but it is the version you would have.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 5. Month three
body.push(label('Section five'));
body.push(h1('Month three — make it compound'));
body.push(p('**Weeks 9 to 12.** Nothing new gets started. What exists gets deeper.'));
body.push(bullet('Local mentions and links: Oakville business directories, Halton-area partners, and a cross-link with Allure if that relationship allows it. Being mentioned on other Oakville websites is what tells Google you are genuinely of this town.'));
body.push(bullet('The weight-loss launch you flagged: a service entry on your Google profile now, and a page if the site is live, so it has a few weeks of age before you start promoting it.'));
body.push(bullet('If the site is live, two or three articles answering real consult questions, each linked to the treatment page it relates to.'));
body.push(bullet('Full review of the numbers against the baseline, and a recommendation for the next quarter.'));

body.push(spacer(200));

// ---- 6. Keywords
body.push(label('Section six'));
body.push(h1('What we would rank you for'));
body.push(p('These are the searches worth owning in your catchment, and what would have to exist for you to appear in them.'));
body.push(spacer(120));
body.push(table([3200, 3400, 3480], [
  ['Search', 'What would rank for it', 'Realistic in 90 days?'],
  ['botox oakville', 'Google profile (map pack)', 'Map pack yes, organic needs Path C'],
  ['lip filler oakville', 'Treatment page', 'Only with Path C'],
  ['nurse injector oakville', 'Google profile + treatment page', 'Strong fit. Your least contested term'],
  ['skin booster oakville', 'Treatment page', 'Only with Path C, but low competition'],
  ['dermaplaning oakville', 'Treatment page', 'Only with Path C'],
  ['electrolysis oakville', 'Treatment page', 'Only with Path C, and your reviews already mention this'],
  ['med spa near me', 'Google profile', 'Depends entirely on resolving the Allure filtering'],
  ['"how much is lip filler in oakville" and similar', 'Article or FAQ', 'Month three, site permitting'],
]));
body.push(quietNote('A note on honesty: we have not attached monthly search volumes to these. Our keyword data subscription was out of credits at the time of writing, and we would rather show you nothing than show you a number we made up. Volumes get validated and added before we commit to targets. It does not hold up any of the work above.'));

body.push(p('The pattern in that right-hand column is the argument for the website, put plainly. Without one you can compete in the map and nowhere else.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 7. Compliance
body.push(label('Section seven'));
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

body.push(h2('What this means for the content already scheduled'));
body.push(p('Your Instagram calendar runs to 65 posts. **Twenty-one of them name Botox or Dysport in the headline, hook or caption**, and fourteen carry Botox hashtags. Most pair the brand name with a description of its effect, which is exactly the combination Health Canada restricts.'));
body.push(p('None of that content is wasted. The ideas are good and the design work is done. It needs a compliance pass on the wording: brand names swapped for treatment descriptions, benefit claims rephrased. We would scope that separately once you have read this and decided how cautious you want to be.'));
body.push(quietNote('There is an upside here worth naming. "The injector who follows the rules" is a genuinely differentiating position in a market where most do not, and it is the same message as the content you have already built: honest, careful, no shortcuts. The compliant version of your marketing is also the more persuasive version.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 8. Instagram
body.push(label('Section eight'));
body.push(h1('Instagram'));
body.push(p('You already have a content system: 65 posts, three months, designed and briefed. This section is not about what to post. It is about making the account findable, and about paying to put the best of it in front of the right women in Oakville.'));

body.push(h2('The profile as a search surface'));
body.push(p('Instagram is a search engine that most clinics treat as a scrapbook. A few structural things matter more than any individual post.'));
body.push(bullet('**The name field**, not the username. This is what Instagram search actually indexes. It should read along the lines of "Cleo | Nurse Injector Oakville". Right now that field is doing nothing for you.'));
body.push(bullet('**The bio** names the town and the treatments in plain language, then gives one instruction.'));
body.push(bullet('**Location tag on every post.** Oakville, every time. It is the cheapest local signal available and it takes two seconds.'));
body.push(bullet('**Hashtags weighted local** rather than global. #oakvillemedspa and #oakvilleaesthetics put you in front of people who could actually book with you. #botox puts you in a feed with millions of posts where nobody will ever see yours. Keep the local tags clear of prescription brand names, for the reasons in section seven.'));
body.push(bullet('**Alt text** written properly on each image. It is indexed, almost nobody uses it, and it costs nothing.'));
body.push(bullet('**Highlights organised by treatment**, so a stranger can find what you do in one tap. If there is no website this quarter, these are your service pages.'));
body.push(bullet('**A link that works.** Right now, if it points at the domain, it points at nothing.'));

body.push(h2('Paid'));
body.push(p('You told us most patients already come from Instagram and Google ads, so this is not a new channel. It is a channel to run properly.'));

body.push(h3('Audiences'));
body.push(bullet('**Local radius.** Women within roughly 15km of Oakville. Your form left the age range blank, so we would start at 28 to 55 and narrow it against who actually books. This is the core audience and it should take most of the budget.'));
body.push(bullet('**Retargeting.** Anyone who engaged with the account or watched a video in the last 30 days. Cheapest bookings you will get, every time.'));
body.push(bullet('**Lookalike.** Built from your existing patient list once you can export it from your booking system. Worth doing after the first two are running, not before.'));

body.push(h3('Creative'));
body.push(bullet('Pull directly from the carousels already produced. They are designed, they are on brand, and testing them as ads tells you which topics are worth more of your budget organically too.'));
body.push(bullet('Run three or four at once, not one. You are looking for the outlier, and you cannot find it without something to compare against.'));
body.push(bullet('Face-to-camera tends to beat graphics for a practice built on one person. You are the product.'));

body.push(h3('The flow'));
body.push(p('Ad to DM to consultation, matching the "DM to book" call to action already in your content. Do not send paid traffic to a dead domain, and do not send it to a profile with no Highlights and no clear booking route. That is where the money leaks.'));

body.push(h3('Budget and testing'));
body.push(bullet('Your onboarding form did not include current ad spend, so we need that number before recommending a figure. What we can say is the structure: a fixed monthly budget split roughly 70 / 20 / 10 across local radius, retargeting and lookalike.'));
body.push(bullet('Review every fortnight. Kill anything below the account average on cost per DM. Move that money to whatever is beating it. Nothing runs unchanged for a month.'));
body.push(bullet('Judge ads on DMs and bookings, not likes. Reach is not the point.'));

body.push(quietNote('How the two halves of this plan connect: ads produce DMs, DMs become appointments, appointments feed the review engine, and reviews are what lift you in the map pack. Paid and organic are not separate programmes here. The paid work is what makes the local SEO compound faster than it would on its own.'));

body.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 9. What we need
body.push(label('Section nine'));
body.push(h1('What we need from you'));
body.push(p('Most of the delay in work like this comes from waiting on access. The sooner these arrive, the sooner month one starts.'));

body.push(h3('Access'));
body.push(bullet('Google Business Profile, and confirmation of which email holds it'));
body.push(bullet('Domain registrar login for luxurybeautybycleo.ca'));
body.push(bullet('Meta Business account and ad account'));
body.push(bullet('Instagram (a collaborator invitation is enough, we do not need your password)'));
body.push(bullet('Your booking system, whichever it is. The form did not say'));

body.push(h3('Assets'));
body.push(bullet('Photos of the treatment room and the space'));
body.push(bullet('A current headshot'));
body.push(bullet('Your signed before-and-after consent form, so we know what we can publish'));
body.push(bullet('Your treatment list with current pricing'));

body.push(h3('Answers'));
body.push(p('Your onboarding form left these blank and each one changes what we do:'));
body.push(bullet('The three local competitors you most want to be measured against'));
body.push(bullet('Your ideal patient, described in a sentence or two in your own words'));
body.push(bullet('What you currently spend on Instagram and Google ads each month'));
body.push(bullet('Your real opening hours'));
body.push(bullet('Whether your arrangement with Allure allows you your own signage and your own suite designation. This determines how we build the Google listing'));
body.push(bullet('The website decision'));

body.push(spacer(220));

// ---- 10. Measurement
body.push(label('Section ten'));
body.push(h1('How we will measure it'));
body.push(p('Reported monthly against the starting point, in this order of importance.'));
body.push(spacer(120));
body.push(table([3400, 3200, 3480], [
  ['What we track', 'Where it starts', 'Where we want it in 90 days'],
  ['Google reviews', '12, averaging 5.0', '20 to 22, still at or near 5.0'],
  ['Calls and direction requests from Google', 'To be baselined in week one', 'Up, with the trend line mattering more than the number'],
  ['Map pack position for the target searches', 'To be baselined in week one', 'Visible for "nurse injector oakville" and "botox oakville"'],
  ['Instagram profile visits and link taps', 'To be baselined in week one', 'Up, with taps rising faster than visits'],
  ['DMs and booked consultations', 'Not currently tracked', 'Tracked from week one, attributed to source'],
  ['Organic website sessions', 'No site', 'Only applies under Path B or C'],
]));
body.push(spacer(200));
body.push(p('One honest expectation to set. Local search moves slowly and most of month one produces no visible result at all. It is repair work. The reviews will move first, usually around week six. Map position follows the reviews. If there is a website, its rankings arrive last and largely after this quarter ends. Anyone promising you faster than that is selling you something.'));

// ------------------------------------------------------------------- assemble

const doc = new Document({
  creator: 'Luxury Beauty by Cleo R. growth plan',
  title: 'Getting Found in Oakville: 90-Day Local SEO and Instagram Plan',
  description: 'Local SEO and Instagram roadmap for Luxury Beauty by Cleo R., Oakville, Ontario',
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
