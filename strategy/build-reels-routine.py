# -*- coding: utf-8 -*-
import csv, datetime

W1MON = datetime.date(2026, 8, 17)

def wk_date(week, weekday_offset):
    return W1MON + datetime.timedelta(days=7 * (week - 1) + weekday_offset)

def theme(d):
    if d < datetime.date(2026, 9, 1):  return "Botox, Honestly (Launch)"
    if d < datetime.date(2026, 10, 1): return "Botox Education Month"
    if d < datetime.date(2026, 11, 1): return "Fillers, Naturally"
    if d < datetime.date(2026, 11, 16):return "Rested by the Holidays"
    if d < datetime.date(2026, 12, 1): return "Gift Season Opens"
    if d < datetime.date(2027, 1, 1):  return "Glow Into the New Year"
    return "New Year, Real Results"

SETS = {"Education": "Set A", "Trust & Proof": "Set C",
        "Personality & BTS": "Set D", "Promo & CTA": "Set E"}

# (week, slot_index) -> fields
# slot_index: 0 = Wed reel, 1 = Fri image/ad, 2 = Sun reel
# fields: format, pillar, topic, hook3s, script, onscreen, caption, cta, hashtag_override, audio, asset, source
R = []
def a(week, slot, fmt, pillar, topic, hook, script, onscreen, caption, cta, audio, asset, source="", hset=None):
    R.append(dict(week=week, slot=slot, fmt=fmt, pillar=pillar, topic=topic, hook=hook,
                  script=script, onscreen=onscreen, caption=caption, cta=cta,
                  hset=hset or SETS[pillar], audio=audio, asset=asset, source=source))

# ---------------- Week 2 ----------------
a(2,0,"Reel (video)","Education",
  "3 Botox Myths in 30 Seconds",
  "Three things about Botox that are just not true.",
  "Talking head, three fast cuts. Cut 1: 'It freezes your face' - no, dosing does. Cut 2: 'You get addicted' - no, you get used to looking rested. Cut 3: 'Wait until you have wrinkles' - the earlier conversation is cheaper. End on camera, no music.",
  "MYTH 1 / MYTH 2 / MYTH 3 + final card: Ask before you book",
  "The Monday carousel in 30 seconds, because not everyone swipes. Which of the three did you believe? Tell me below.",
  "DM BOTOX or link in bio","Trending audio, low volume under voice. Vertical 9:16, natural window light.",
  "Film 3 takes at the window seat. Captions burned in.","Repurpose: Aug 17 carousel '5 Botox Lies You Still Believe'")
a(2,1,"Paid ad (static)","Promo & CTA",
  "Boost: 5 Red Flags at a Med Spa",
  "Your face deserves better than a bargain.",
  "No filming. Take slide 1 of the Aug 20 carousel, resize to 1:1 and 4:5, add a Learn More button frame.",
  "5 RED FLAGS AT A MED SPA",
  "Five things worth walking away from. Save this before you book anywhere, not just here.",
  "Save this before you book","Meta Ads Manager. Audience: women 28-55, Oakville / Burlington / Milton / Mississauga, 15km radius. Budget: start at $10/day, 5 days.",
  "1:1 + 4:5 ad crops from the existing carousel cover","Reuse: Aug 20 carousel folder")
a(2,2,"Reel (video)","Personality & BTS",
  "The Prep Tray, Start to Finish",
  "The part nobody films.",
  "Silent, ASMR style. Top-down on the tray. New gloves, sealed vial turned to camera so the lot number reads, alcohol swab, face marked while she moves. No talking, text only.",
  "New tray. Sealed product. Marked while you move. / Ask to watch. Anyone doing it properly will say yes.",
  "No music, no voiceover. This is just what every appointment looks like before anyone touches your face. Ask to watch next time.",
  "Zero shortcuts. Ever.","Silent with soft room tone or a quiet ambient track. Top-down tripod.",
  "Film one continuous top-down take, 25-40 sec","Reuse: Aug 21 prep tray photo set")

# ---------------- Week 3 ----------------
a(3,0,"Reel (video)","Education",
  "What 20 Units Actually Looks Like",
  "Twenty units. That is all it is.",
  "Hold the syringe to camera, show the volume against a fingertip. Explain forehead vs elevens vs crow's feet unit ranges. End: 'Anyone quoting you a flat price without seeing your face is guessing.'",
  "20 UNITS = about this much / Dose follows your muscle, not a price list",
  "People hear units and picture something enormous. Here is the actual amount. Your number depends on your muscle strength, not on what your friend had.",
  "DM UNITS to ask about yours","Voiceover, no trending audio. Macro close-up on the syringe.",
  "Film macro syringe shot + talking head","")
a(3,1,"Image post + boost","Trust & Proof",
  "Quote card: Rested, Not Frozen",
  "You should still be able to frown.",
  "Static quote card in the editorial template. Dark tone.",
  "Rested, not frozen.",
  "If you cannot frown, squint or smile afterwards, that was too much. Movement is not a failure of the treatment. It is the point.",
  "Save this","Boost $8/day for 4 days to the local radius.",
  "Design quote card, 4:5","")
a(3,2,"Reel (video)","Personality & BTS",
  "Meet NP Cleo in 20 Seconds",
  "Hi, I am the person actually holding the needle.",
  "Straight to camera, one take. Name, credential (NP, RN(EC)), why she opened a one-client-at-a-time studio, what she will tell you no about. Warm, unscripted.",
  "NP Cleo / Nurse Practitioner + Injector / Oakville",
  "Ask any clinic who is actually holding the needle. Here it is me, every time. Nurse practitioner, registered and insured, one client in the room at a time.",
  "DM to book a consult","No music or very soft. Seated in the treatment room.",
  "Film 20-30 sec intro, 3 takes","Repurpose: Aug 27 Meet NP Cleo carousel")

# ---------------- Week 4 ----------------
a(4,0,"Reel (video)","Education",
  "Botox vs Dysport, Plainly",
  "Same job. Different personality.",
  "Split screen or two-card cutaway. Onset speed, spread, how long each lasts, who each suits. End: 'Neither is better. One is better for you.'",
  "BOTOX vs DYSPORT / onset / spread / longevity",
  "Two products, one job. The difference is how fast they start and how far they spread. That is genuinely it.",
  "DM which one you are curious about","Voiceover with clean cuts. No trending audio.",
  "Film talking head + two title cards","Repurpose: Sep 7 carousel")
a(4,1,"Image post + boost","Education",
  "Aftercare in 6 Rules",
  "Save this for the 24 hours after.",
  "Static checklist card, light template, six numbered lines.",
  "THE FIRST 24 HOURS / 6 rules",
  "Upright for four hours. No gym, no facials, no heat. Do not rub. Everything else is normal life.",
  "Save this for after your appointment","Boost $8/day for 4 days.",
  "Design 6-rule checklist card, 4:5","Repurpose: Sep 10 aftercare carousel")
a(4,2,"Reel (video)","Education",
  "Your First Visit, Filmed",
  "Nervous about a first appointment? Watch this.",
  "Walk-through POV: door, seat, consultation table, face mapping, tray. Voiceover over B-roll. 45 minutes and most of it is talking.",
  "45 minutes / most of it is talking / you can say no at any point",
  "A first visit runs about 45 minutes and most of that is conversation. You can leave without booking anything. That is a normal outcome here.",
  "DM to book your consult","Soft instrumental. Handheld POV walkthrough.",
  "Film studio walkthrough B-roll, 60-90 sec of footage","Repurpose: Aug 24 First Visit carousel")

# ---------------- Week 5 ----------------
a(5,0,"Reel (video)","Education",
  "Preventative Botox: When to Actually Start",
  "It is not about your age.",
  "Talking head. The test: does the line stay when your face relaxes? If yes, it is a static line. If no, you are still preventing. Show with own forehead.",
  "Does the line stay when you relax? / YES = treating / NO = preventing",
  "Nobody needs to start at a specific birthday. The only question that matters is whether the line is still there when your face is at rest.",
  "DM PREVENT to ask about yours","Voiceover. Mirror or front-on framing.",
  "Film talking head with forehead demo","Repurpose: Aug 31 Preventative Botox carousel")
a(5,1,"Image post + boost","Trust & Proof",
  "Quote card: Why I Say No",
  "The best injectors turn work away.",
  "Static quote card, dark template.",
  "A good injector will tell you no.",
  "I have turned down work that would have paid well. If the plan does not suit your face, you should hear that out loud before anyone opens a vial.",
  "Save this before you book","Boost $8/day for 4 days.",
  "Design quote card, 4:5","")
a(5,2,"Reel (video)","Trust & Proof",
  "5 Things Botox Will Not Fix",
  "Let me save you some money.",
  "Fast list to camera: deep static folds, volume loss, skin texture, sun damage, under-eye hollows. For each, name what actually helps instead.",
  "WILL NOT FIX: 1-5 + what actually helps",
  "If someone tells you Botox fixes all five of these, walk. Different problems need different tools, and some of them are not injectables at all.",
  "Save this","Voiceover, quick cuts, no music.",
  "Film 5-beat list, 40 sec","Repurpose: Sep 14 carousel")

# ---------------- Week 6 ----------------
a(6,0,"Reel (video)","Education",
  "The Face Map: Where the Units Go",
  "Three areas. Very different jobs.",
  "Overlay a face map graphic on a still of NP Cleo. Point to forehead, glabella, crow's feet. Explain the muscle behind each and why over-treating the forehead drops brows.",
  "FOREHEAD / ELEVENS / CROW'S FEET",
  "Your forehead lifts your brows. Treat it too hard and everything drops. This is why the plan matters more than the product.",
  "DM MAP with your question","Voiceover over animated overlay.",
  "Design face-map overlay + film narration","Repurpose: Sep 14 face map post")
a(6,1,"Image post + boost","Promo & CTA",
  "Consults Are Free",
  "You can leave without booking anything.",
  "Static card, light template, plain typographic offer.",
  "CONSULTS ARE FREE / and you can walk out with nothing booked",
  "A consultation is not a sales appointment. We go through your goals, map your face in motion, and if injectables are not the answer I will tell you.",
  "DM CONSULT to book","Boost $10/day for 5 days. Lead objective.",
  "Design offer card, 4:5 + 1:1","")
a(6,2,"Reel (video)","Personality & BTS",
  "Ask NP Cleo: The 3 Questions I Get Every Day",
  "Same three questions. Every single week.",
  "Talking head, three chapters: Will it hurt? Will people notice? What if I hate it? Honest answers, no softening.",
  "Q1 / Q2 / Q3",
  "Three questions, asked in the DMs every week. Here are the honest answers, including the one about hating it.",
  "Drop your question below","Conversational, seated, soft music.",
  "Film 3-chapter Q&A, 60 sec","Repurpose: Sep 24 Ask NP Cleo carousel")

# ---------------- Week 7 ----------------
a(7,0,"Reel (video)","Education",
  "How Long Does It Really Last",
  "Three to four months, and here is why yours may be shorter.",
  "Talking head + simple timeline graphic. Metabolism, muscle strength, dose, exercise load. End with the honest line about the first round often fading faster.",
  "WEEK 2 peak / MONTH 3 softening / MONTH 4 back to baseline",
  "Your first round often fades a little faster. That is normal, not a bad product. The second round usually holds longer.",
  "DM to plan your timing","Voiceover with a timeline animation.",
  "Design timeline graphic + film narration","Repurpose: Sep 28 carousel")
a(7,1,"Image post + boost","Trust & Proof",
  "What Natural Results Actually Look Like",
  "If you can tell, it was too much.",
  "Static card pairing a real healed result crop with the line. Use consented Pair E.",
  "Still you. Just rested.",
  "Nobody should be able to point at what you had done. They should just think you slept well.",
  "Save this","Boost $8/day for 4 days.",
  "Crop Pair E after image, add hook overlay","Photo library: img_9912.jpg (Pair E, consent not needed)")
a(7,2,"Reel (video)","Education",
  "Botox or Filler? 20-Second Answer",
  "Lines or volume. That is the whole decision.",
  "Two-card cutaway. Lines from movement = neuromodulator. Volume loss or structure = filler. Most faces need a bit of both, in that order.",
  "MOVEMENT = relaxer / VOLUME = filler",
  "It is not a personality test. Movement lines get a relaxer. Lost volume gets filler. If someone sells you both on day one without looking at your face in motion, leave.",
  "DM which one you think you need","Fast cuts, voiceover.",
  "Film 2-beat explainer, 25 sec","Repurpose: Sep 21 Botox or Filler carousel")

# ---------------- Week 8 ----------------
a(8,0,"Reel (video)","Education",
  "Lip Filler: Natural vs Overdone",
  "The difference is not the amount. It is the shape.",
  "Side-by-side stills with annotation arrows. Ratio, border, projection. Explain why chasing volume without respecting the existing lip shape reads as fake.",
  "SHAPE first / VOLUME second",
  "Overdone lips are usually not too much product. They are product placed against the lip you already have instead of with it.",
  "DM LIPS to ask","Voiceover over annotated stills.",
  "Annotate consented stills + film narration","Photo library: Pair B (img_0962 / img_0998, consent not needed)")
a(8,1,"Image post + boost","Education",
  "Filler Will Not Make You Look Like Someone Else",
  "You will still look like you.",
  "Static card, light template.",
  "Filler cannot give you someone else's face. It can only sharpen yours.",
  "The photo you brought in is someone else's bone structure. What we can do is make your own read better. That is the honest ceiling.",
  "Save this before your consult","Boost $8/day for 4 days.",
  "Design card, 4:5","Repurpose: Oct 5 carousel")
a(8,2,"Reel (video)","Trust & Proof",
  "One Syringe. Day 0 to Day 14.",
  "This is what one syringe actually does.",
  "Photo transition reel. Before, day 0 swollen, day 14 settled. Voiceover naming what changed and what was left alone.",
  "BEFORE / DAY 0 / DAY 14",
  "One syringe, her own lip shape kept. The middle photo is swelling, not the result. This is why I ask you not to judge anything before two weeks.",
  "DM LIPS to book a consult","Soft music, slow cross-dissolves.",
  "Sequence 3 consented stills into a 20-sec reel","Photo library: img_9848 / img_9850 (Pair F, consent on file)")

# ---------------- Week 9 ----------------
a(9,0,"Reel (video)","Education",
  "Cheek Filler: The Lift Nobody Notices",
  "Everyone thinks it is about cheeks. It is not.",
  "Talking head + face map overlay. Midface support lifts the lower face. Explain why treating the nasolabial fold directly is usually the wrong move.",
  "SUPPORT the midface / not fill the fold",
  "The fold you keep looking at is usually a symptom. Support the midface and it softens on its own.",
  "DM CHEEK to ask","Voiceover with overlay.",
  "Film narration + design midface overlay","Repurpose: Oct 12 carousel")
a(9,1,"Image post + boost","Education",
  "Facial Balancing, Explained",
  "One area at a time is how faces go wrong.",
  "Static card, light template, 3 short lines.",
  "FACIAL BALANCING / the plan, not the product",
  "Chasing one line at a time is how people end up looking treated. A plan looks at the whole face and often does less, not more.",
  "Save this","Boost $8/day for 4 days.",
  "Design card, 4:5","Repurpose: Oct 29 carousel")
a(9,2,"Reel (video)","Trust & Proof",
  "Real Lips, Real Settle Time",
  "Two weeks. Then judge it.",
  "Before and after stills, matched 3/4 profile, colour corrected. Voiceover on why day-0 photos mislead.",
  "BEFORE / 2 WEEKS",
  "Same angle, same light, two weeks apart. Nothing added to the shape she already had.",
  "DM LIPS to book","Soft music, slow transitions.",
  "Colour-match and sequence Pair B","Photo library: img_0962 / img_0998 (Pair B)")

# ---------------- Week 10 ----------------
a(10,0,"Reel (video)","Education",
  "Lip Filler Aftercare: The First 48 Hours",
  "Do these five things and swelling behaves.",
  "Talking head over B-roll of ice pack, water bottle, pillow. Five rules: ice, upright sleep, hydrate, no gym, no flights.",
  "48 HOURS / 5 rules",
  "Swelling peaks on day two and it always looks worse than the result. These five things keep it short.",
  "Save this for the day after","Voiceover over B-roll.",
  "Film aftercare B-roll + narration","Repurpose: Oct 22 aftercare carousel")
a(10,1,"Image post + boost","Education",
  "Filler Dissolves. Here Is the Timeline.",
  "It is not permanent, and that is a feature.",
  "Static timeline card, dark template.",
  "6-12 MONTHS / and reversible in 20 minutes if needed",
  "Hyaluronic acid filler breaks down. If you hate it, it can be dissolved. Anyone offering something permanent for lips should worry you.",
  "Save this before you book","Boost $8/day for 4 days.",
  "Design timeline card, 4:5","Repurpose: Oct 19 carousel")
a(10,2,"Reel (video)","Trust & Proof",
  "Swelling Is Not Your Result",
  "Day zero is a lie. Here is proof.",
  "Show the reclined day-0 heavily swollen shot, then the healed one. Voiceover: 'If you had judged it here, you would have panicked.'",
  "DAY 0 / DAY 14 / do not judge the middle",
  "This is the photo people screenshot and panic about. Two weeks later it is a completely different lip. Patience is part of the treatment.",
  "DM if you are in your swelling week","Voiceover, no music.",
  "Sequence day-0 and healed stills","Photo library: img_7715.jpg (day 0) + Pair F healed")

# ---------------- Week 11 ----------------
a(11,0,"Reel (video)","Education",
  "5 Filler Lies in 40 Seconds",
  "Five things about filler that are simply not true.",
  "Rapid list to camera. It migrates always / it stretches your skin / more is better / it is permanent / cheap filler is the same product.",
  "LIE 1 through LIE 5",
  "Five things I hear every week. The last one is the one that actually costs people money.",
  "Save and send to whoever needs it","Quick cuts, trending audio low.",
  "Film 5-beat list, 40 sec","Repurpose: Oct 26 carousel")
a(11,1,"Paid ad (static)","Trust & Proof",
  "Before and After: Pair A",
  "Front-on, honest, nothing retouched.",
  "Side-by-side ad crop, cropped above the collarbone per the consent note.",
  "BEFORE / AFTER / one appointment",
  "Same light, same angle, one appointment apart. Consent on file and cropped as agreed.",
  "DM to book a consult","Meta ad, $12/day for 5 days, local radius. Check platform policy on before/after before running.",
  "Crop and pair img_0221 / img_0233 above the collarbone","Photo library: Pair A, consent on file")
a(11,2,"Reel (video)","Personality & BTS",
  "A Day in the Treatment Room",
  "One client at a time. All day.",
  "Time-lapse day in the life: room reset between clients, tray builds, notes, last light. Voiceover about why the schedule is deliberately small.",
  "ONE client in the room / no overlap / no rushing",
  "The room is reset completely between every client. It is slower and it books fewer people. That is the trade I chose.",
  "DM to book","Soft instrumental, time-lapse cuts.",
  "Film a full clinic day, edit to 45 sec","")

# ---------------- Week 12 ----------------
a(12,0,"Reel (video)","Promo & CTA",
  "Book Now to Glow by December",
  "If you want to look rested at the party, this is your week.",
  "Calendar graphic with a countdown. Explain the two-week settle window and the top-up window. End with the last safe booking date.",
  "TREAT BY / SETTLES BY / PARTY SEASON",
  "Injectables need two weeks to settle and sometimes a small top-up at week two. Work backwards from your first December event and you land on right now.",
  "DM HOLIDAY to book","Voiceover over calendar animation.",
  "Design countdown calendar + film narration","Repurpose: Nov 2 Holiday Timeline carousel")
a(12,1,"Paid ad (static)","Promo & CTA",
  "Holiday Booking Timeline",
  "Work backwards from your first party.",
  "Static timeline ad, dark template, 1:1 and 4:5 crops.",
  "BOOK BY [date] TO GLOW BY DECEMBER",
  "The calendar does the arguing for me. Two weeks to settle, one week of buffer, then party season.",
  "DM HOLIDAY to book","Meta ad, $15/day for 7 days. Traffic to DM.",
  "Design timeline ad, 1:1 + 4:5","")
a(12,2,"Reel (video)","Trust & Proof",
  "Every Angle, Healed",
  "Six angles. Nothing hidden.",
  "Slow rotation through the six healed-result angles. No hook overlay after the first two seconds. Voiceover: 'Most clinics post one angle. Here are six.'",
  "SIX ANGLES / healed and settled",
  "One result, photographed from every side once it had fully settled. If a clinic only ever shows you one angle, ask why.",
  "DM to book","Slow music, cross-dissolves.",
  "Tight-crop the six angles and sequence","Photo library: img_4775 / 4777 / 4778 / 4780 / 4781 / 4782 (Pair G, consent on file)")

# ---------------- Week 13 ----------------
a(13,0,"Reel (video)","Promo & CTA",
  "Gift Certificates Are Live",
  "Finally, a gift nobody returns.",
  "Show the physical gift card, the envelope, the handwriting. Voiceover on how it works and that the recipient still gets a full consultation first.",
  "GIFT CERTIFICATES / any amount / consult always included",
  "Any amount, and whoever receives it still gets a proper consultation before anything is decided. Nobody gets talked into anything as a gift.",
  "DM GIFT to order","Warm music, close-up product B-roll.",
  "Film gift card B-roll, 30 sec","Repurpose: Nov 9 Gift of Glow carousel")
a(13,1,"Image post + boost","Promo & CTA",
  "Party Season Starts Here",
  "December is closer than the calendar admits.",
  "Static promo card, dark template.",
  "PARTY SEASON / book your December face in November",
  "November bookings are the ones that look effortless in December. December bookings are the ones that look done.",
  "DM HOLIDAY to book","Boost $10/day for 5 days.",
  "Design promo card, 4:5","Repurpose: Nov 5 Party Season carousel")
a(13,2,"Reel (video)","Trust & Proof",
  "Three Months of Honest Injecting",
  "Ninety days in. Here is what you taught me.",
  "Talking head retrospective. The three most-asked questions, the thing she changed because of DMs, the post that surprised her. Warm, direct.",
  "MONTH 1 / MONTH 2 / MONTH 3",
  "Three months of posting the unglamorous parts. The DMs told me people want the honest version more than the pretty one, so that is what continues.",
  "Tell me what to cover next","No music, one continuous take.",
  "Film 60-sec retrospective","Repurpose: Nov 12 '3 Months' carousel")

# ---------------- Week 14 : Gift Season Opens ----------------
a(14,0,"Reel (video)","Promo & CTA",
  "What to Ask For This Year (That Is Not a Candle)",
  "Put this on your list instead.",
  "Light, funny. Hold up a candle, set it aside, hold up the gift certificate. Voiceover on how to actually ask for it without it being awkward.",
  "NOT A CANDLE / a consultation and a plan",
  "Send this to whoever asks what you want. Screenshot it. Leave it open on their phone. I do not judge.",
  "DM GIFT to order","Trending audio, playful edit.",
  "Film 20-sec comedy beat","")
a(14,1,"Image post + boost","Promo & CTA",
  "The Gift Certificate Card",
  "Any amount. Consultation always included.",
  "Static product shot of the printed card in its envelope, light template.",
  "GIFT CERTIFICATES / any amount",
  "Printed, handwritten, and posted or picked up. Any amount, and a full consultation comes with it.",
  "DM GIFT to order","Boost $10/day for 5 days.",
  "Shoot the card flat-lay, 4:5","")
a(14,2,"Reel (video)","Education",
  "How Late Is Too Late Before an Event",
  "Your event is in ten days. Should you book?",
  "Straight answer reel. Neuromodulator: 14 days minimum. Filler: 3-4 weeks minimum. Under ten days: skin only. Say no clearly.",
  "14 DAYS for relaxer / 3-4 WEEKS for filler / under 10 days = skin only",
  "I will turn you away if the timing is wrong, and you should want an injector who does. Swollen lips in a wedding photo last longer than the filler does.",
  "DM your event date and I will tell you honestly","Voiceover, calendar graphic.",
  "Design countdown graphic + film narration","Idea bank: Before your event checklist")

# ---------------- Week 15 ----------------
a(15,0,"Reel (video)","Promo & CTA",
  "Black Friday, Done Honestly",
  "I am not discounting the needle.",
  "Talking head, firm. Why unit discounts push over-treatment, what is actually on offer instead (gift certificate bonus value), and why that difference matters.",
  "NO unit discounts / bonus value on gift cards only",
  "Discounting units encourages people to buy more than their face needs. So the offer is on gift certificates instead. Same value to you, no pressure on the plan.",
  "DM GIFT for the Black Friday terms","No music, direct to camera.",
  "Film 40-sec position piece","")
a(15,1,"Paid ad (static)","Promo & CTA",
  "Black Friday Gift Certificate Offer",
  "Bonus value, not discounted units.",
  "Static offer ad, dark template, 1:1 and 4:5.",
  "BLACK FRIDAY / bonus value on every gift certificate",
  "The one week a year there is an offer, and it is on gift certificates. The treatment plan is never on sale.",
  "DM GIFT to order","Meta ad, $20/day Nov 27-30. Highest-spend week of the plan.",
  "Design offer ad, 1:1 + 4:5","")
a(15,2,"Reel (video)","Trust & Proof",
  "Why the Needle Is Never on Sale",
  "Cheap injectables are expensive.",
  "Talking head. What bargain pricing usually means: diluted product, rushed appointments, no complication plan. Reference the red flags carousel.",
  "CHEAP PRODUCT / RUSHED ROOM / NO PLAN",
  "When the price is impossible, something is being cut. Usually it is the time somebody should have spent looking at your face.",
  "Save this before you chase a deal","No music, direct to camera.",
  "Film 40-sec piece","Repurpose: Aug 20 Red Flags carousel")

# ---------------- Week 16 : Glow Into the New Year ----------------
a(16,0,"Reel (video)","Education",
  "Your December Face Plan, Week by Week",
  "Four weeks. Here is the order.",
  "Calendar graphic, four beats. Week 1 treat, week 2 settle, week 3 top-up if needed, week 4 skin and hydration only.",
  "W1 TREAT / W2 SETTLE / W3 TOP-UP / W4 SKIN ONLY",
  "December works if you run it in this order. It falls apart if you try to compress it into the last ten days.",
  "DM DECEMBER to book","Voiceover over calendar animation.",
  "Design 4-week calendar + film narration","")
a(16,1,"Paid ad (static)","Promo & CTA",
  "Last Call for Party-Season Botox",
  "After this week the maths stops working.",
  "Static urgency ad, dark template.",
  "LAST CALL / treat by [date] to settle by NYE",
  "Two weeks to settle. Count backwards from New Year's Eve and this is the week.",
  "DM DECEMBER to book","Meta ad, $15/day for 6 days.",
  "Design urgency ad, 1:1 + 4:5","")
a(16,2,"Reel (video)","Personality & BTS",
  "GRWM: A Day of Consults",
  "Get ready with me for a day of saying no.",
  "GRWM format. Morning routine, drive, room setup, first client prep. Voiceover about what a consult day actually involves.",
  "GRWM / injector edition",
  "A consult day is mostly listening and occasionally telling someone their money is better spent elsewhere. Here is the whole morning.",
  "DM to book a consult","Trending GRWM audio.",
  "Film morning routine + studio setup, edit to 45 sec","Idea bank: GRWM injector edition")

# ---------------- Week 17 ----------------
a(17,0,"Reel (video)","Education",
  "Skincare Before Injectables: The Right Order",
  "Do this before you spend a dollar on filler.",
  "Talking head + product B-roll (unbranded). Sunscreen, retinoid, consistency for 3 months. Explain why texture and tone problems do not respond to filler.",
  "SPF / RETINOID / 3 MONTHS / then talk injectables",
  "If your concern is texture, tone or dullness, injectables will not touch it. Fix the skin first. It is cheaper and it makes everything after it look better.",
  "Save this","Voiceover over product B-roll.",
  "Film B-roll + narration","Idea bank: Skincare before injectables")
a(17,1,"Image post + boost","Education",
  "The Week Before Your Event",
  "Seven days out. Do these, skip those.",
  "Static checklist card, light template, do/do-not columns.",
  "7 DAYS OUT / do / do not",
  "No new treatments, no new products, no fish oil, no last-minute anything. Sleep, water, and the plan you already made.",
  "Save this for event week","Boost $8/day for 4 days.",
  "Design do/do-not card, 4:5","Idea bank: Before your event checklist")
a(17,2,"Reel (video)","Trust & Proof",
  "The 3 Questions to Ask Any Injector",
  "Ask these three before anyone touches your face.",
  "Direct to camera. Who is injecting and what is their licence? What product and what lot? What happens if something goes wrong, and who do I call at 9pm?",
  "Q1 licence / Q2 product and lot / Q3 complication plan",
  "Ask these anywhere, including here. If a clinic gets defensive about any of the three, that is your answer.",
  "Save this and take it to your next consult","No music, direct to camera.",
  "Film 40-sec piece","Repurpose: Aug 20 Red Flags carousel")

# ---------------- Week 18 ----------------
a(18,0,"Reel (video)","Promo & CTA",
  "Last Day to Order Gift Certificates for Christmas",
  "After today it will not arrive in time.",
  "Urgent but warm. Show the card, the envelope, the post box. State the cutoff date clearly twice.",
  "ORDER BY [date] / pickup available until [date]",
  "Ordering closes today for anything posted. Pickup stays open a little longer. After that it is a January gift, which is honestly also fine.",
  "DM GIFT today","Warm music, quick cuts.",
  "Film 20-sec urgency piece","")
a(18,1,"Paid ad (static)","Promo & CTA",
  "Last-Minute Gift",
  "Still nothing for her? Sorted in one message.",
  "Static ad, warm holiday styling, 1:1 and 4:5.",
  "LAST-MINUTE / one DM and it is done",
  "One message, any amount, sent digitally within the hour. You did not forget. You planned it this way.",
  "DM GIFT to order","Meta ad, $18/day for 5 days. Broaden age range to include partners.",
  "Design last-minute ad, 1:1 + 4:5","")
a(18,2,"Reel (video)","Personality & BTS",
  "The Studio, Dressed for December",
  "Come see the room.",
  "Slow room tour, holiday styling, candles, the chair, the tray station. Minimal talking, mostly ambience.",
  "the room / one client at a time",
  "Quiet, private, and one person in it at a time. That does not change in December, it just gets better lighting.",
  "DM to book","Soft holiday instrumental.",
  "Film slow room tour, 30 sec","")

# ---------------- Week 19 ----------------
a(19,0,"Reel (video)","Personality & BTS",
  "Holiday Hours and a Thank You",
  "Closing dates, and something I want to say.",
  "Talking head. State closing and reopening dates on screen. Then a genuine thank-you to the first-year clients.",
  "CLOSED [dates] / REOPEN [date]",
  "The dates are on screen. The rest of this is just a thank you to everyone who trusted a new studio in its first months.",
  "DM for January availability","No music, one take.",
  "Film 30-sec message","")
a(19,1,"Image post","Personality & BTS",
  "Merry Christmas from the Studio",
  "Whatever today looks like for you.",
  "Simple static card, warm template. No offer, no CTA button.",
  "Merry Christmas / see you in the new year",
  "No offer today. Just thank you, and I hope the day is a kind one.",
  "See you in January","Organic only. Do not boost this one.",
  "Design a simple warm card, 4:5","")
a(19,2,"Reel (video)","Education",
  "The Quietest Week Is the Best Week to Book",
  "Nobody books between Christmas and New Year. That is the point.",
  "Talking head. Downtime is invisible this week, the calendar is open, and everything has settled by mid-January.",
  "SETTLE NOW / look rested by mid-January",
  "This is the week where a little swelling costs you nothing socially. It is quietly the best booking window of the year.",
  "DM JANUARY to book","Voiceover, calm.",
  "Film 30-sec piece","")

# ---------------- Week 20 ----------------
a(20,0,"Reel (video)","Trust & Proof",
  "2026 in Results",
  "The year, in thirty seconds.",
  "Montage of consented healed results with dates. Voiceover naming what stayed constant: one client at a time, honest no's, natural results.",
  "2026 / one room / one client at a time",
  "Every face in this is someone who agreed to be here. Thank you for a first year that looked like this.",
  "DM to book your 2027 consult","Slow music, cross-dissolves.",
  "Sequence consented result stills, 30 sec","Photo library: consented images only, Pairs A, C, F, G")
a(20,1,"Image post + boost","Promo & CTA",
  "New Year, Same Face. Just Rested.",
  "No resolutions here.",
  "Static card, light template.",
  "NEW YEAR / same face, just rested",
  "Nothing about you needs fixing in January. If you want to look less tired, that is a different and much smaller conversation.",
  "DM CONSULT to book","Boost $10/day for 5 days.",
  "Design card, 4:5","")
a(20,2,"Reel (video)","Education",
  "New to Injectables? Start Here.",
  "If you have never done this, watch this first.",
  "Beginner primer. What a consult is, what a first treatment usually is (small), what it costs in time, and what you can walk away from.",
  "CONSULT / SMALL FIRST DOSE / REVIEW AT 2 WEEKS",
  "Nobody sensible starts big. A small first dose and a two-week review is how you find out what your face actually needs.",
  "DM NEW to book a consult","Calm voiceover.",
  "Film 60-sec primer","")

# ---------------- Week 21 : New Year, Real Results ----------------
a(21,0,"Reel (video)","Education",
  "January Reset: What Works and What Does Not",
  "Half of what you are about to buy will not work.",
  "Fast list. What actually moves the needle (SPF, sleep, retinoid, targeted injectables) vs what does not (gadget devices, collagen drinks, panic buying).",
  "WORKS / DOES NOT",
  "January sells a lot of hope. This is the short list of what actually changes a face, and it is boring.",
  "Save this","Quick cuts, voiceover.",
  "Film 45-sec list","")
a(21,1,"Paid ad (static)","Promo & CTA",
  "January Consults Are Open",
  "Free, honest, and you can leave with nothing booked.",
  "Static ad, light template, 1:1 and 4:5.",
  "JANUARY CONSULTS OPEN / free / no pressure",
  "A consultation costs you 45 minutes and nothing else. Come in, get a straight answer, decide later.",
  "DM CONSULT to book","Meta ad, $15/day for 7 days. Lead objective.",
  "Design ad, 1:1 + 4:5","")
a(21,2,"Reel (video)","Trust & Proof",
  "Price Transparency: What It Actually Costs",
  "Let us talk prices. For real.",
  "Direct to camera with ranges on screen. Explain why there is no flat price list, then give honest ranges anyway so nobody is guessing.",
  "RANGES, not a price list / your dose is yours",
  "I do not post a price list because doses differ from face to face. That is not an excuse to leave you guessing, so here are honest ranges.",
  "DM for a quote on your plan","No music, direct to camera.",
  "Film 60-sec piece with on-screen ranges","Idea bank: Price transparency (flagged as a strong differentiator)")

# ---------------- Week 22 ----------------
a(22,0,"Reel (video)","Education",
  "Men and Botox",
  "Brotox is not a trend. It is a Tuesday.",
  "Talking head. Why male dosing is higher, why the goal is different (not smoothing, just softening), and how to keep it undetectable.",
  "HIGHER DOSE / DIFFERENT GOAL / same discretion",
  "Men are the fastest-growing group in the chair and almost nobody markets to them honestly. Higher dose, lighter touch, nobody knows.",
  "DM to ask anything, discreetly","Voiceover, plain styling.",
  "Film 40-sec piece","Idea bank: Men and Botox, untapped audience")
a(22,1,"Image post + boost","Education",
  "Brotox Is Not a Trend",
  "It is just Tuesday.",
  "Static card, dark template, plain type.",
  "MEN'S TREATMENTS / higher dose, lighter goal",
  "No special branding, no different room. Same consultation, same honesty, a different dose.",
  "DM to ask","Boost $10/day for 5 days. Target men 30-55 in the local radius.",
  "Design card, 4:5 + 1:1","")
a(22,2,"Reel (video)","Trust & Proof",
  "Under-Eye Filler: The Honest Truth",
  "The most requested and most misunderstood treatment I do.",
  "Serious tone. Who is a candidate, who is absolutely not, what goes wrong (festooning, Tyndall), and why she turns most people down for it.",
  "WHO IT SUITS / WHO IT DOES NOT / what goes wrong",
  "I turn down more under-eye requests than I accept. When it is wrong it is very visibly wrong and it lasts a long time.",
  "DM UNDER EYE for an honest assessment","No music, direct to camera.",
  "Film 60-sec piece","Idea bank: Under-eye filler, high search volume")

# ---------------- Week 23 ----------------
a(23,0,"Reel (video)","Education",
  "What Filters Did to Beauty Standards",
  "Your face is not supposed to look like a filter.",
  "Emotional piece. Show a filtered vs unfiltered still of herself. Talk about clients bringing in filtered photos of their own faces as the goal.",
  "FILTERED / REAL / one of these is a face",
  "People bring me filtered photos of themselves and ask to look like that. A filter is not a face. It is a shape no bone structure produces.",
  "Share this with someone who needs it","Soft music, honest edit.",
  "Film 45-sec piece with filter comparison","Idea bank: What filters did to beauty standards, highly shareable")
a(23,1,"Paid ad (static)","Promo & CTA",
  "Retargeting: Book a Consult",
  "You have been reading for a while.",
  "Static ad, light template. Retarget viewers of the last 90 days of video and profile visitors.",
  "STILL THINKING ABOUT IT? / the consult is free",
  "No pressure and no sales script. Forty-five minutes, an honest answer, and you decide afterwards.",
  "DM CONSULT to book","Meta ad, $12/day for 7 days. Custom audience: video viewers 75% + profile engagers, last 90 days.",
  "Design retargeting ad, 1:1 + 4:5","")
a(23,2,"Reel (video)","Trust & Proof",
  "Three Sessions, One Client",
  "Watch what six months actually looks like.",
  "Progress series. Three consented time points with dates on screen. Voiceover on why slow beats dramatic.",
  "SESSION 1 / SESSION 2 / SESSION 3",
  "Six months, three appointments, nothing dramatic on any single day. That is what a plan looks like from the outside.",
  "DM to start your own plan","Slow music, cross-dissolves.",
  "Sequence 3 consented time points","Idea bank: Progress series. NEEDS fresh client consent and photos over time - confirm before filming")

# ---------------- Week 24 ----------------
a(24,0,"Reel (video)","Personality & BTS",
  "Ask Me Anything: The January Live, Clipped",
  "You asked. Here are the three best ones.",
  "Clip the three strongest answers from the monthly IG Live into one reel with chapter cards.",
  "LIVE Q&A / Q1 / Q2 / Q3",
  "Clipped from Monday's live. If your question did not get answered, put it below and it goes in February's.",
  "Drop your question for next month","Native live audio, chapter cards.",
  "Run the IG Live first, then clip 3 answers","Idea bank: IG Live AMA. Each live produces 3-5 reels")
a(24,1,"Image post + boost","Trust & Proof",
  "Six Months of Honest Work",
  "Every result here belongs to someone who said yes.",
  "Static grid of consented healed results, 3x3, light template.",
  "SIX MONTHS / every face here consented",
  "Six months of a one-room studio. Every image posted with permission and nothing retouched beyond colour.",
  "DM to book","Boost $12/day for 5 days.",
  "Build 3x3 consented results grid, 4:5 + 1:1","Photo library: consented images only")
a(24,2,"Reel (video)","Promo & CTA",
  "Month 6: What Is Next",
  "Six months in. Here is what changes.",
  "Talking head. What the next six months add (new treatments, booking page launch, referral programme), and a direct ask to book.",
  "MONTH 6 / what is next",
  "Six months of posting the honest version. Next up: a proper booking page so you stop having to DM me at midnight.",
  "DM to book, or use the link in bio","No music, one take.",
  "Film 45-sec forward-look","Swap every DM CTA to the booking link once the page is live")

# ---------------- emit ----------------
DAYOFF = {0: 2, 1: 4, 2: 6}   # Wed, Fri, Sun
SLOTNAME = {0: "Slot 1 - Reel", 1: "Slot 2 - Image / Ad", 2: "Slot 3 - Reel"}

HEADER = ["Week","Date","Day","Slot","Month Theme","Format","Platforms","Pillar",
          "Topic & Hook","Hook (first 3 sec)","Script / Shot List","On-screen Text",
          "Caption Draft","CTA","Hashtag Set","Audio / Style / Ad Spend","Asset to Create",
          "Source Assets & Notes","Filmed","Edited","Status","Posted Link",
          "Views","Saves","Shares","DMs","Bookings"]

rows = []
for r in R:
    d = wk_date(r["week"], DAYOFF[r["slot"]])
    if "Reel" in r["fmt"]:
        plats = "IG Reels + Facebook Reels + TikTok"
    elif "ad" in r["fmt"].lower():
        plats = "Meta Ads (IG + FB) + GBP"
    else:
        plats = "IG feed + Facebook + GBP"
    rows.append([
        r["week"], d.strftime("%b %-d, %Y"), d.strftime("%a"), SLOTNAME[r["slot"]],
        theme(d), r["fmt"], plats, r["pillar"], r["topic"], r["hook"], r["script"],
        r["onscreen"], r["caption"], r["cta"], r["hset"], r["audio"], r["asset"],
        r["source"], "", "", "Idea", "", "", "", "", "", "",
    ])

assert len(rows) == 69, len(rows)

out = "/home/user/InstagramCarousel/strategy/reels-video-weekly-routine-w2-w24.csv"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    w.writerows(rows)
print("wrote", out, len(rows), "rows")
print("first", rows[0][1], "last", rows[-1][1])
