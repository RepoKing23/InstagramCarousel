"""Write the daily GBP copy out as one readable document.

    python3 design/build-blog-copy.py

strategy/gbp-daily-content.json stays the single source. This renders it as
strategy/gbp-blog-copy.md, month by month, so the whole run can be read,
printed or handed to someone without opening the workbook.
"""
import json
import os
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'strategy', 'gbp-daily-content.json')
OUT = os.path.join(ROOT, 'strategy', 'gbp-blog-copy.md')


def main():
    with open(CONTENT, encoding='utf-8') as f:
        data = json.load(f)
    meta, posts = data['_meta'], data['posts']

    out = [
        '# Google Business Profile — the copy, all of it',
        '',
        f"{meta['brand']}. {meta['range'].replace(' to ', ' to ')}, "
        f"{len(posts)} posts, one a day.",
        '',
        'Generated from `strategy/gbp-daily-content.json` by',
        '`design/build-blog-copy.py`. Edit the json, not this file.',
        '',
        'Each day carries two lengths. **Short** is the quick version. **Long** is',
        'the search version, which is the one to use on the days that matter. The',
        'button is always Learn more, pointed at',
        f"[{meta['instagram']}]({meta['instagram_url']}).",
        '',
    ]

    month = None
    for p in posts:
        d = datetime.datetime.strptime(p['date'], '%Y-%m-%d')
        if d.strftime('%B %Y') != month:
            month = d.strftime('%B %Y')
            out += ['', f'## {month}', '']
        src = ('evergreen, no Instagram post this day'
               if p['source'] == 'GBP only' else p['source'])
        if p.get('no_card'):
            # logged after the fact: real copy, no artwork, nothing to show
            out += [
                f"### {d.strftime('%a %d %b')} — {p['source']}",
                '',
                f"No card · {p['service']} · {p['pillar']}",
                '',
                f"*{p['note']}*",
                '',
            ]
        else:
            out += [
                f"### {d.strftime('%a %d %b')} — {p['headline'].replace('*', '')} "
                f"{p['script']}",
                '',
                f"`{p['date']}-{p['slug']}.jpg` · {p['service']} · {p['pillar']} · "
                f"{src}",
                '',
                f"**On the card:** {p['body']} → *{p['button']}*",
                '',
            ]
        out += [
            f"**Short ({len(p['text'])} chars)**",
            '',
            p['text'],
            '',
            f"**Long ({len(p['description'])} chars)**",
            '',
        ]
        out += [para for line in p['description'].split('\n\n')
                for para in (line, '')]

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out).rstrip() + '\n')
    print(f'wrote {os.path.relpath(OUT, ROOT)}  ({len(posts)} days)')


if __name__ == '__main__':
    main()
