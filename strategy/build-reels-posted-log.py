# -*- coding: utf-8 -*-
"""Generate the log of reels/video/image posts that already went out.

Captions are recorded verbatim as supplied. Production columns (shot list,
on-screen text, audio, asset to create) are left blank: these are finished
posts, not briefs, and nothing about how they were made was recorded.
"""
import csv

HEADER = ["Week","Date","Day","Slot","Month Theme","Format","Platforms","Pillar",
          "Topic & Hook","Hook (first 3 sec)","Script / Shot List","On-screen Text",
          "Caption Draft","CTA","Hashtag Set","Audio / Style / Ad Spend","Asset to Create",
          "Source Assets & Notes","Filmed","Edited","Status","Posted Link",
          "Views","Saves","Shares","DMs","Bookings"]

REEL = "IG Reels + Facebook Reels + TikTok"
FEED = "IG feed + Facebook + GBP"
THEME = "Botox, Honestly (Launch)"

CAP_LIP = (   # ran Aug 18

    "Lip enhancement, thoughtfully done.\n\n"
    "Every treatment is customized to complement your natural features, adding beautiful volume "
    "and definition while keeping your results looking natural.\n\n"
    "Because the goal is to enhance your features, not change who you are.\n\n"
    "#LuxuryBeautyByCleo #LipFiller #AestheticResults #LipEnhancement #LuxuryAesthetics"
)
CAP_MYTHS = ( # ran Aug 17

    "Half of what you have heard about Botox came from someone who saw bad work. Let's set the "
    "record straight. Which myth did you believe? Drop it below and share this with a friend.\n\n"
    "#botox #botoxeducation #botoxmyths #preventativebotox #antiwrinkleinjections nurseinjector "
    "medspa naturalbotox botoxbeforeandafter aestheticnurse"
)
CAP_AUG20 = (
    "Did you know that Nurse Practitioners can have a seat at the research table? \U0001F3E5\U0001F4CA\n\n"
    "I recently had the incredible opportunity to attend a Novo Nordisk summit where we presented "
    "a research project focused on reducing diabetes through staying active.\n\n"
    "While we are known for our hands-on patient care, our role extends far beyond the clinic "
    "walls. NPs bring a unique, patient-centered perspective to clinical trials and public health "
    "initiatives. We don't just treat the numbers; we understand the human behind them.\n\n"
    "It was an honor to contribute to research that has the power to change lives. Here's to "
    "advocating for our patients not just in the exam room, but in the lab and beyond!\n\n"
    "#NursePractitioner #NP #DiabetesAwareness #Nursing #NursingResearch PhysicalActivity "
    "HealthcareInnovation BeyondTheBedside PublicHealth"
)
CAP_AUG24 = (
    "Most people arrive nervous and leave asking why they waited so long.\n\n"
    "Usually that is because nobody told them what actually happens. So here it is, start to "
    "finish, including the part where we agree on the areas, the units and the price before "
    "anything gets opened.\n\n"
    "The treatment itself is the short part. Ten to fifteen minutes for most people. Everything "
    "before it is what makes the difference.\n\n"
    "Swipe through. If you are still nervous at the end, send me the question you are embarrassed "
    "to ask. I have heard it before.\n\n"
    "#botoxoakville #oakvillemedspa #burlingtonbotox #miltonmedspa #mississaugainjector"
)
CAP_AUG27 = (
    "A little lip filler can make a beautiful difference. This before-and-after shows a more "
    "defined lip shape, balanced volume, and a natural-looking finish.\n\n"
    "Ready to enhance your natural features? Book your consultation with Cleo.\n\n"
    "\U0001F4E9 DM us to book your appointment"
)

# week, date, day, slot, format, platforms, pillar, topic, hook, caption, cta, hashtags, notes, filmed
ROWS = [
    (1, "Aug 17, 2026", "Mon", "Posted - Carousel", "Carousel", FEED, "Education",
     "5 Botox Lies You Still Believe",
     "Half of what you have heard about Botox came from someone who saw bad work.",
     CAP_MYTHS, "Drop your myth below and share this", "Set A, plus five tags posted without the # symbol",
     "Actually posted, on plan. Matches the Aug 17 carousel on Posting Schedule.",
     ""),
    (1, "Aug 18, 2026", "Tue", "Posted - Image", "Before/After image", FEED, "Trust & Proof",
     "Lip Enhancement, Thoughtfully Done",
     "Lip enhancement, thoughtfully done.",
     CAP_LIP, "DM to book a consultation", "Custom: lip filler tags",
     "Actually posted. Ran in place of the Service Spotlight: Botox single image that Posting Schedule had planned for this date. Same format, different subject.",
     ""),
    (1, "Aug 20, 2026", "Thu", "Posted - Reel", "Reel (video)", REEL, "Personality & BTS",
     "NPs at the Research Table: Novo Nordisk Summit",
     "Did you know that Nurse Practitioners can have a seat at the research table?",
     CAP_AUG20, "None in caption", "Custom: NP and research tags, four posted without the # symbol",
     "Actually posted. Authority and credential content, outside the injectables themes. Worth repeating: it is the strongest proof of expertise on the grid.",
     "Yes"),
    (2, "Aug 24, 2026", "Mon", "Posted - Carousel", "Carousel", FEED, "Education",
     "Your First Visit, Start to Finish",
     "Most people arrive nervous and leave asking why they waited so long.",
     CAP_AUG24, "Send me the question you are embarrassed to ask", "Set A",
     "Actually posted. Matches the Aug 24 First Visit carousel on Posting Schedule.",
     ""),
    (2, "Aug 27, 2026", "Thu", "Posted - Image", "Before/After image", FEED, "Trust & Proof",
     "A Little Lip Filler, A Beautiful Difference",
     "A little lip filler can make a beautiful difference.",
     CAP_AUG27, "DM us to book your appointment", "None used",
     "Actually posted. Posting Schedule had Meet NP Cleo planned for this date.",
     ""),
    (2, "Aug 28, 2026", "Fri", "Posted - Reel", "Reel (video)", REEL, "Personality & BTS",
     "Zen Meditation Highlight",
     "Not recorded",
     "", "Not recorded", "Not recorded",
     "Actually posted. Only the title was recorded: 'Zen video meditation highlight'. Paste the caption and link when you have them.",
     "Yes"),
]

out = "/home/user/InstagramCarousel/strategy/reels-video-posted-log.csv"
rows = []
for (wk, date, day, slot, fmt, plats, pillar, topic, hook, cap, cta, tags, notes, filmed) in ROWS:
    rows.append([
        wk, date, day, slot, THEME, fmt, plats, pillar, topic, hook,
        "", "",                      # Script / Shot List, On-screen Text: finished post, no brief
        cap, cta, tags,
        "", "",                      # Audio / Ad Spend, Asset to Create: not applicable
        notes, filmed, "Yes", "Posted", "",
        "", "", "", "", "",
    ])

with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    w.writerows(rows)
assert all(len(r) == len(HEADER) for r in rows)
print("wrote", out, len(rows), "rows")
