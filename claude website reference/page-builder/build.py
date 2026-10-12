"""Assembles the static pages from partials. Run: python build.py <site_dir>
The output is plain HTML; nothing in the published folder depends on this script.
All product data below is placeholder: names, options, prices, offers and bulk tiers."""
import sys, os, html, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
NL = chr(10)

def read(name):
    return open(os.path.join(HERE, name), encoding='utf-8').read()

def icon(name, cls='icon'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="assets/img/icons.svg#i-{name}"/></svg>'

def price(n, cls='price'):
    return f'<span class="{cls}"><svg aria-hidden="true"><use href="assets/img/icons.svg#i-rupee"/></svg><span class="visually-hidden">Rs </span>{n}</span>'

def expand(t):
    t = re.sub(r'[{][{]I:([a-z-]+)[}][}]', lambda m: icon(m.group(1)), t)
    t = re.sub(r'[{][{]Is:([a-z-]+)[}][}]', lambda m: icon(m.group(1), 'icon icon--sm'), t)
    t = re.sub(r'[{][{]Il:([a-z-]+)[}][}]', lambda m: icon(m.group(1), 'icon icon--lg'), t)
    t = re.sub(r'[{][{]P:([0-9]+)[}][}]', lambda m: price(m.group(1)), t)
    return t

# ---- categories ----
CATS = [
    # id, name, colour, text-on-colour, icon, menu line, menu text, menu image
    ('posters', 'Posters', 'sunglow', 'ink', 'poster', 'For the photo that deserves a wall.', 'Three sizes, matte or glossy.', 'photos/posters-shelf.webp'),
    ('stickers', 'Stickers', 'rose', 'paper', 'sticker', 'Inside jokes, cut to shape.', 'Singles, sheets and bagged packs.', 'photos/sticker-pack.webp'),
    ('booklets', 'Booklets', 'fuchsia', 'paper', 'booklet', 'The trip, edited down and bound.', 'Photo booklets and newsprint zines.', 'photos/booklet.webp'),
    ('merch', 'Merch', 'royal', 'paper', 'tee', 'Wear the group chat.', 'Tees and totes with your art on them.', 'photos/tote.webp'),
    ('packaging', 'Packaging', 'coral', 'paper', 'box', 'Make the unboxing look deliberate.', 'Boxes, mailers and tape by the roll.', 'photos/box-label.webp'),
    ('cards', 'Cards', 'turquoise', 'ink', 'card', 'For the cafe, the label, the club.', 'Business cards and thank-you notes.', 'photos/cards-white.webp'),
]
CAT = {c[0]: c for c in CATS}

# Occasions: id, name, colour, text-on-colour, line, three products, cut-out. All placeholder picks.
OCCASIONS = [
    ('birthdays', 'Birthdays', 'sunglow', 'ink', 'The worst photo you have of them, as big as it goes.', ['poster-print', 'sticker-pack', 'printed-tee'], 'posters.webp'),
    ('trips', 'Trips', 'royal', 'paper', 'Six hundred photos, edited down to the ones worth keeping.', ['photo-booklet', 'printed-tee', 'poster-print'], 'booklet.webp'),
    ('farewells', 'Farewells', 'turquoise', 'ink', 'The whole team on one thing they will carry around.', ['tote-bag', 'printed-tee', 'newsprint-zine'], 'tote.webp'),
    ('rakhi', 'Rakhi', 'rose', 'paper', 'Every nickname you have given him, cut to shape.', ['die-cut-stickers', 'sticker-pack', 'thank-you-cards'], 'sticker-pack.webp'),
    ('diwali', 'Diwali', 'fuchsia', 'paper', 'Something to send that is not a forwarded greeting.', ['thank-you-cards', 'art-print', 'sticker-pack'], 'stickers.webp'),
    ('weddings', 'Weddings', 'coral', 'paper', 'The photo everyone asked for, finally off the phone.', ['art-print', 'photo-booklet', 'poster-print'], 'posters.webp'),
    ('new-shop', 'Opening a shop', 'sunglow', 'ink', 'Boxes, tape and cards that make it look like a real brand.', ['mailer-box', 'packing-tape', 'business-cards'], 'box-tape.webp'),
    ('no-reason', 'Just because', 'turquoise', 'ink', 'Sometimes a sticker is just funny.', ['die-cut-stickers', 'tote-bag', 'art-print'], 'tee.webp'),
]

def o(label, *values):
    """An option group. Each value is 'Name' or ('Name', price multiplier)."""
    return (label, [(v, 1) if isinstance(v, str) else v for v in values])

P = [
    dict(slug='poster-print', cat='posters', name='Poster print', text='Your photo or art on heavyweight paper.', price=199,
         long='The photo that has been your lock screen for three years, at a size people can actually see. Printed edge to edge on heavyweight paper.',
         imgs=['photos/posters-shelf.webp', 'photos/poster-wall.webp', 'photos/poster-folded.webp'], alt='Three posters leaning on a white shelf',
         specs=[('size', 'Sizes', 'A3, A2, A1'), ('paper', 'Paper', 'Matte or glossy'), ('drop', 'Ink', 'Archival')],
         opts=[o('Size', 'A3', ('A2', 1.6), ('A1', 2.4)), o('Paper', 'Matte', 'Glossy')]),
    dict(slug='die-cut-stickers', cat='stickers', name='Die-cut stickers', text='Cut to the outline of whatever you send.', price=99, flag='New',
         long='Inside jokes, pet portraits, your friend&rsquo;s worst nickname. Cut to the outline of your art and built to outlive the laptop.',
         imgs=['photos/stickers-laptop.webp', 'photos/stickers-table.webp', 'photos/sticker-pack-hand.webp'], alt='A laptop lid with stickers on it, beside printed colour swatches',
         specs=[('size', 'Sizes', '5 to 10cm'), ('paper', 'Material', 'Vinyl'), ('drop', 'Finish', 'Matte or gloss')],
         opts=[o('Size', '5cm', ('7.5cm', 1.3), ('10cm', 1.6)), o('Finish', 'Matte', 'Gloss')]),
    dict(slug='printed-tee', cat='merch', name='Printed tee', text='Your art on the front, the back or both.', price=349, pos='50% 38%',
         long='Wear the group chat. Your art on the front, the back or both, for the trip, the farewell or no reason at all.',
         imgs=['photos/tee-cafe.webp', 'photos/tee-road.webp', 'photos/neck-label.webp'], alt='A white tee with a colourful print on the back',
         specs=[('size', 'Sizes', 'XS to XXL'), ('paper', 'Fabric', 'Cotton'), ('drop', 'Print', 'Front or back')],
         opts=[o('Size', 'XS', 'S', 'M', 'L', 'XL', 'XXL'), o('Print', 'Front', 'Back', ('Both', 1.3))]),
    dict(slug='photo-booklet', cat='booklets', name='Photo booklet', text='The trip, edited down and bound.', price=249,
         long='Six hundred trip photos edited down to the forty worth keeping, bound so they stay in order.',
         imgs=['photos/booklet.webp', 'photos/book-cover.webp', 'photos/newsprint.webp'], alt='An open booklet with colourful pages',
         specs=[('size', 'Sizes', 'A5, A4'), ('paper', 'Pages', '20 to 60'), ('drop', 'Binding', 'Stapled')],
         opts=[o('Size', 'A5', ('A4', 1.5)), o('Pages', '20', ('40', 1.5), ('60', 2))]),
    dict(slug='mailer-box', cat='packaging', name='Mailer box', text='Kraft boxes with your label on the lid.', price=299, tag='Bulk rates',
         long='For people who sell things and want the unboxing to look deliberate. Kraft mailer boxes with your label printed on the lid.',
         imgs=['photos/box-label.webp', 'boxes.webp', 'box-tape.webp'], alt='A kraft mailer box with a turquoise label',
         specs=[('size', 'Sizes', 'S, M, L'), ('paper', 'Board', 'Kraft'), ('drop', 'Print', 'Full colour')],
         opts=[o('Size', 'S', ('M', 1.3), ('L', 1.6)), o('Print', 'One colour', 'Full colour')]),
    dict(slug='sticker-pack', cat='stickers', name='Sticker pack', text='A bagged set of your own designs.', price=149, sale=15,
         long='A bagged set of your own designs, ready to hand over. Good for birthdays, better for inside jokes.',
         imgs=['photos/sticker-pack.webp', 'photos/sticker-pack-hand.webp', 'photos/stickers-table.webp'], alt='A bagged pack of stickers on a blue background',
         specs=[('size', 'Count', '6 or 12'), ('paper', 'Material', 'Vinyl'), ('drop', 'Finish', 'Gloss')],
         opts=[o('Count', '6 stickers', ('12 stickers', 1.7)), o('Finish', 'Gloss', 'Matte')]),
    dict(slug='business-cards', cat='cards', name='Business cards', text='For the cafe, the label, the club.', price=149, tag='Bulk rates',
         long='For the cafe, the label, or the college club that finally has a logo.',
         imgs=['photos/cards-white.webp', 'photos/cards-colour.webp', 'photos/cards-teal.webp'], alt='A stack of white cards printed with a logo',
         specs=[('size', 'Size', '90 x 55mm'), ('paper', 'Paper', 'Matte or textured'), ('drop', 'Sides', 'One or two')],
         opts=[o('Paper', 'Matte', 'Textured'), o('Sides', 'One side', ('Two sides', 1.2))]),
    dict(slug='tote-bag', cat='merch', name='Tote bag', text='A canvas bag that carries the joke.', price=299, sale=10,
         long='A canvas bag that carries the joke everywhere. The whole team on one tote works too.',
         imgs=['photos/tote.webp', 'photos/tote-chair.webp'], alt='A cream canvas tote bag with a printed logo',
         specs=[('size', 'Size', 'One size'), ('paper', 'Fabric', 'Canvas'), ('drop', 'Print', 'One side')],
         opts=[o('Print', 'One side', ('Both sides', 1.25))]),
    dict(slug='art-print', cat='posters', name='Art print', text='Wall-ready, with a clean white border.', price=249,
         long='Your illustration or photo with a clean white border, ready for a frame or a strip of tape.',
         imgs=['photos/poster-wall.webp', 'photos/poster-folded.webp', 'photos/posters-shelf.webp'], alt='A white poster pasted on a wall over yellow and green sheets',
         specs=[('size', 'Sizes', 'A4, A3'), ('paper', 'Paper', 'Textured'), ('drop', 'Finish', 'Matte')],
         opts=[o('Size', 'A4', ('A3', 1.5)), o('Paper', 'Textured', 'Matte')]),
    dict(slug='newsprint-zine', cat='booklets', name='Newsprint zine', text='Big pages, loose folds, properly inky.', price=299, flag='New',
         long='Big pages, loose folds, properly inky. For the trip, the band, or the year in review.',
         imgs=['photos/newsprint.webp', 'photos/booklet.webp'], alt='A folded newspaper with a bold printed headline',
         specs=[('size', 'Size', 'Tabloid'), ('paper', 'Pages', '8 to 24'), ('drop', 'Paper', 'Newsprint')],
         opts=[o('Pages', '8', ('16', 1.6), ('24', 2.2))]),
    dict(slug='packing-tape', cat='packaging', name='Packing tape', text='Your pattern, by the roll.', price=199, tag='Bulk rates',
         long='Your logo or pattern on packing tape, by the roll. It makes a plain box look like yours.',
         imgs=['box-tape.webp', 'boxes.webp'], alt='A kraft box sealed with printed Ctrl P tape, the roll beside it',
         specs=[('size', 'Width', '48mm'), ('paper', 'Length', '50m roll'), ('drop', 'Print', 'Full colour')],
         opts=[o('Print', 'One colour', ('Full colour', 1.25))]),
    dict(slug='thank-you-cards', cat='cards', name='Thank-you cards', text='Slip one into every order.', price=129,
         long='A small card to slip into every order. People keep these longer than you would think.',
         imgs=['photos/cards-teal.webp', 'photos/cards-colour.webp', 'photos/cards-white.webp'], alt='A stack of turquoise cards on a wooden table',
         specs=[('size', 'Size', 'A6'), ('paper', 'Paper', 'Matte'), ('drop', 'Sides', 'One or two')],
         opts=[o('Paper', 'Matte', 'Textured'), o('Sides', 'One side', ('Two sides', 1.2))]),
]
# How the artwork is shown on the create page: (shape, width / height, what the area is called)
PREVIEW = {
    'poster-print': ('sheet', 0.707, 'Poster'), 'art-print': ('sheet', 0.707, 'Art print'),
    'die-cut-stickers': ('diecut', 1, 'Sticker'), 'sticker-pack': ('diecut', 1, 'Sticker'),
    'printed-tee': ('sheet', 0.8, 'Print area on the tee'), 'tote-bag': ('sheet', 0.85, 'Print area on the tote'),
    'photo-booklet': ('sheet', 0.707, 'Front cover'), 'newsprint-zine': ('sheet', 0.75, 'Front page'),
    'mailer-box': ('sheet', 1.5, 'Lid label'), 'packing-tape': ('sheet', 3, 'Tape pattern'),
    'business-cards': ('sheet', 1.636, 'Card front'), 'thank-you-cards': ('sheet', 1.414, 'Card front'),
}
PIECE = {'sticker-pack': 'pack', 'printed-tee': 'tee', 'tote-bag': 'tote', 'mailer-box': 'box', 'packing-tape': 'roll', 'art-print': 'print', 'newsprint-zine': 'zine'}
UNIT = {'posters': 'poster', 'stickers': 'sticker', 'booklets': 'booklet', 'merch': 'piece', 'packaging': 'piece', 'cards': 'card'}

for i, p in enumerate(P):
    p['order'] = i
    p['url'] = 'product-' + p['slug'] + '.html'
    p['was'] = round(p['price'] * 100 / (100 - p['sale'])) if p.get('sale') else None

BY = {p['slug']: p for p in P}

def flags_of(p):
    f = []
    if p.get('flag'): f.append(('new', f'<span class="flag" style="--c:var(--sunglow)">{p["flag"]}</span>'))
    if p.get('sale'): f.append(('sale', f'<span class="flag flag--offer" style="--c:var(--coral); --on:var(--paper)"><b>{p["sale"]}%</b> off</span>'))
    if p.get('tag'): f.append(('bulk', f'<span class="flag" style="--c:var(--turquoise)">{p["tag"]}</span>'))
    return f

def default_opts(p):
    return ', '.join(vals[0][0] for _, vals in p['opts'])

# How many photos a product takes in the create flow (one unless listed)
PHOTOS = {'sticker-pack': 6, 'die-cut-stickers': 3}

def add_attrs(p):
    shape, ratio, area = PREVIEW[p['slug']]
    return (f'data-id="{p["slug"]}" data-name="{p["name"]}" data-price="{p["price"]}" data-img="assets/img/{p["imgs"][0]}" data-url="{p["url"]}" '
            f'data-cat="{p["cat"]}" data-shape="{shape}" data-ratio="{ratio}" data-area="{area}" data-max="{PHOTOS.get(p["slug"], 1)}" data-colour="{CAT[p["cat"]][2]}" data-unit="{PIECE.get(p["slug"], UNIT[p["cat"]])}"')

def cat_pill(p):
    cid, cname, col, on, ic, *_ = CAT[p['cat']]
    return f'<span class="cat" style="--c:var(--{col}); --on:var(--{on})">{icon(ic)}{cname}</span>'

def product_card(p, i=0, reveal=True):
    specs = ''.join(f'<li>{icon(sic)}<span><b>{k}</b>{v}</span></li>' for sic, k, v in p['specs'])
    fl = flags_of(p)
    flags_html = (NL + '              <div class="pcard__flags">' + ''.join(h for _, h in fl) + '</div>') if fl else ''
    was = price(p['was'], 'price price--was') if p['was'] else ''
    pos = f' style="object-position:{p["pos"]}"' if p.get('pos') else ''
    rv = ' data-reveal' if reveal else ''
    search = html.escape((p['name'] + ' ' + CAT[p['cat']][1] + ' ' + p['text']).lower())
    return f'''          <article class="pcard" data-slug="{p['slug']}" data-cat="{p['cat']}" data-price="{p['price']}" data-order="{p['order']}" data-name="{p['name']}" data-flags="{' '.join(k for k, _ in fl)}" data-search="{search}" style="--d:{i % 3}"{rv}>
            <div class="pcard__media">
              <a href="{p['url']}" tabindex="-1" aria-hidden="true"><img src="assets/img/{p['imgs'][0]}" loading="lazy" alt=""{pos}></a>
              <button class="pcard__wish" type="button" aria-pressed="false" aria-label="Save {p['name']}" data-wish="{p['slug']}">{icon('heart')}</button>{flags_html}
            </div>
            <div class="pcard__body">
              <p class="pcard__meta">{cat_pill(p)}</p>
              <h2 class="h3 pcard__title"><a href="{p['url']}">{p['name']}</a></h2>
              <p class="pcard__text">{p['text']}</p>
              <ul class="pcard__specs">{specs}</ul>
              <div class="pcard__buy">
                <p class="pcard__price"><span>Starting from</span>{price(p['price'])}{was}<small>/ piece</small></p>
                <a class="btn btn--small" href="{p['url']}"><span>Customise</span>{icon('arrow-right', 'icon icon--sm')}</a>
              </div>
            </div>
          </article>'''

PROMO_TILE = f'''          <aside class="pcard-promo" data-promo>
            {icon('stack', 'icon icon--lg')}
            <p class="h2">Printing 25 or more?</p>
            <p>Prices drop as the quantity climbs. Tell us what you need and we&rsquo;ll send a quote.</p>
            <a class="btn" href="brands.html#quote"><span>Ask for a bulk quote</span>{icon('arrow-up-right', 'icon icon--sm')}</a>
          </aside>'''

def product_cards():
    cards = [product_card(p, i) for i, p in enumerate(P)]
    cards.insert(5, PROMO_TILE)
    return (NL * 2).join(cards)

def chip(tag, attrs, col, on, ic, name):
    cls = 'chip chip--filter' if tag == 'button' else 'chip'
    return f'<{tag} class="{cls}" {attrs} style="--c:var(--{col}); --on:var(--{on})"><span class="chip__icon">{icon(ic)}</span><span class="chip__label">{name}</span></{tag}>'

def filter_chips():
    out = ['            ' + chip('button', 'type="button" aria-pressed="true" data-filter="all"', 'ink', 'paper', 'all', 'All')]
    for cid, name, col, on, ic, *_ in CATS:
        out.append('            ' + chip('button', f'type="button" aria-pressed="false" data-filter="{cid}"', col, on, ic, name))
    return NL.join(out)

def mega_cats():
    rows = []
    for i, (cid, name, col, on, ic, *_r) in enumerate(CATS):
        active = ' is-active' if i == 0 else ''
        rows.append(f'                  <li><a class="mega__cat{active}" href="products.html#{cid}" data-panel="{cid}" style="--c:var(--{col}); --on:var(--{on})"><span class="mega__icon">{icon(ic)}</span><span class="mega__name">{name}</span>{icon("chevron-right", "icon icon--sm")}</a></li>')
    return NL.join(rows)

def mega_panels():
    out = []
    for i, (cid, name, col, on, ic, line, text, img) in enumerate(CATS):
        active = ' is-active' if i == 0 else ''
        links = ''.join(f'<a href="{p["url"]}"><span>{p["name"]}</span></a>' for p in P if p['cat'] == cid)
        out.append(f'''                  <div class="mega__panel{active}" data-panel="{cid}" style="--c:var(--{col}); --on:var(--{on})">
                    <div class="mega__products">{links}<a class="mega__all" href="products.html#{cid}"><span>All {name.lower()}</span>{icon("arrow-right", "icon icon--sm")}</a></div>
                    <div class="mega__media"><img src="assets/img/{img}" width="1376" height="768" loading="lazy" alt=""></div>
                  </div>''')
    return NL.join(out)

# ---- product detail page ----
def extra(p, mult):
    """What an option adds to the price of one piece, shown on the option itself."""
    add = round(p['price'] * mult) - p['price']
    return f'<small>+<svg aria-hidden="true"><use href="assets/img/icons.svg#i-rupee"/></svg>{add}</small>' if add > 0 else ''

def product_page(p):
    cid, cname, col, on, ic, *_ = CAT[p['cat']]
    fl = flags_of(p)
    flags_html = '<div class="pcard__flags">' + ''.join(h for _, h in fl) + '</div>' if fl else ''
    thumbs = ''.join(f'<button class="pdp__thumb{" is-active" if i == 0 else ""}" type="button" data-thumb="assets/img/{im}" aria-label="Photo {i + 1}"><img src="assets/img/{im}" loading="lazy" alt=""></button>' for i, im in enumerate(p['imgs']))
    groups = []
    for label, vals in p['opts']:
        key = label.lower()
        radios = ''.join(f'<label class="opt"><input type="radio" name="{key}" value="{v}" data-mult="{m}"{" checked" if i == 0 else ""}><span>{v}{extra(p, m)}</span></label>' for i, (v, m) in enumerate(vals))
        groups.append(f'''              <fieldset class="field">
                <legend class="field__label">{label}</legend>
                <div class="opts">{radios}</div>
              </fieldset>''')
    specs = ''.join(f'<div><dt>{icon(sic)}{k}</dt><dd>{v}</dd></div>' for sic, k, v in p['specs'])
    related = [q for q in P if q['cat'] == p['cat'] and q is not p] + [q for q in P if q['cat'] != p['cat']]
    related_html = (NL * 2).join(product_card(q, i, reveal=False) for i, q in enumerate(related[:3]))
    offer = f'<span class="flag flag--offer" style="--c:var(--coral); --on:var(--paper)"><b>{p["sale"]}%</b> off</span>' if p.get('sale') else ''
    good = ''.join(f'<a class="flag" href="occasions.html#{o[0]}" style="--c:var(--{o[2]}); --on:var(--{o[3]})">{o[1]}</a>' for o in OCCASIONS if p['slug'] in o[5])
    good_html = f'<div class="goodfor"><p>Good for</p><div class="tapes">{good}</div></div>' if good else ''
    unit = PIECE.get(p['slug'], UNIT[p['cat']])
    return f'''  <main id="main">

    <section class="pdp" style="--c:var(--{col}); --on:var(--{on})">
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb">
          <a href="products.html">Shop</a>{icon('chevron-right', 'icon icon--sm')}<a href="products.html#{cid}">{cname}</a>{icon('chevron-right', 'icon icon--sm')}<span aria-current="page">{p['name']}</span>
        </nav>

        <div class="grid pdp__grid">
          <div class="pdp__gallery">
            <figure class="pdp__main">
              <img src="assets/img/{p['imgs'][0]}" alt="{html.escape(p['alt'])}" data-main>
              {flags_html}
            </figure>
            <div class="pdp__thumbs">{thumbs}</div>
          </div>

          <div class="pdp__panel">
            {cat_pill(p)}
            <h1 class="h2 pdp__title">{p['name']}</h1>
            <p class="pdp__text">{p['long']}</p>

            <!-- The one price on the page. It moves with every choice below. -->
            <div class="pdp__price" aria-live="polite" data-price-block>
              <strong data-total>{price(p['price'])}</strong>{offer}
              <p><span data-each>for 1 {unit}</span><small data-saving hidden></small></p>
            </div>

            <form class="pdp__form" id="buy" data-product {add_attrs(p)}>
{NL.join(groups)}
              <fieldset class="field">
                <legend class="field__label">How many</legend>
                <div class="opts">
                  <label class="opt"><input type="radio" name="qty" value="1" checked><span>1</span></label>
                  <label class="opt"><input type="radio" name="qty" value="5"><span>5</span></label>
                  <label class="opt"><input type="radio" name="qty" value="10"><span>10<small>10% off</small></span></label>
                  <label class="opt"><input type="radio" name="qty" value="25"><span>25<small>10% off</small></span></label>
                  <label class="opt"><input type="radio" name="qty" value="50"><span>50<small>20% off</small></span></label>
                  <label class="opt"><input type="radio" name="qty" value="other"><span>Another number</span></label>
                </div>
                <div class="stepper" data-qty-custom hidden>
                  <button type="button" data-step="-1" aria-label="One fewer">{icon('minus')}</button>
                  <input type="number" inputmode="numeric" value="1" min="1" max="999" aria-label="Quantity" data-qty>
                  <button type="button" data-step="1" aria-label="One more">{icon('plus')}</button>
                </div>
              </fieldset>

              <div class="pdp__actions">
                <button class="btn btn--large" type="submit" data-buy><span>Start creating</span>{icon('arrow-right')}</button>
                <button class="pdp__save" type="button" aria-pressed="false" data-wish="{p['slug']}">{icon('heart')}<span>Save for later</span></button>
              </div>
              <p class="pdp__note">Next, you pick a design, add your photo and see it on the {unit}. Nothing goes in the cart until you&rsquo;re happy with it.</p>
            </form>
          </div>
        </div>
      </div>

      <!-- Slides up only when the price above has scrolled out of sight, so there is never more than one price on screen -->
      <div class="buybar" data-buybar hidden>
        <div class="wrap">
          <p class="buybar__price"><strong data-bar-total>{price(p['price'])}</strong><span><b>{p['name']}</b><i data-bar-each>for 1 {unit}</i></span></p>
          <button class="btn" type="submit" form="buy"><span>Start creating</span>{icon('arrow-right', 'icon icon--sm')}</button>
        </div>
      </div>
    </section>

    <section class="pdp-details">
      <div class="wrap grid">
        <div class="pdp-details__copy">
          <h2 class="h2">The <span class="taped" style="--c:var(--{col}); --on:var(--{on})">details.</span></h2>
          <ul class="ticks">
            <li>{icon('check')}No minimum order</li>
            <li>{icon('check')}Bulk pricing from 10 pieces</li>
            <li>{icon('check')}Ships across India</li>
          </ul>
          {good_html}
        </div>
        <dl class="specs">{specs}<div><dt>{icon('one')}Minimum</dt><dd>1 piece</dd></div><div><dt>{icon('truck')}Delivery</dt><dd>Across India</dd></div></dl>
      </div>
    </section>

    <section class="shop shop--related">
      <div class="wrap">
        <h2 class="h2">Goes well <span class="taped">with.</span></h2>
        <div class="grid shop__grid">

{related_html}

        </div>
      </div>
    </section>

  </main>
'''

import time
STAMP = time.strftime('%y%m%d%H%M')

def head(title, desc, extra_css='', robots=''):
    extra_css = extra_css.replace('.css"', '.css?v=' + STAMP + '"')
    return f'''<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{robots}
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="assets/fonts/IntegralCF-ExtraBold.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/NeueRegrade-Variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/tokens.css?v={STAMP}">
  <link rel="stylesheet" href="css/styles.css?v={STAMP}">{extra_css}
  <link rel="stylesheet" href="css/flow.css?v={STAMP}">
  <script>document.documentElement.classList.add("js");</script>
</head>
<body>
'''

SHOP_CSS = NL + '  <link rel="stylesheet" href="css/products.css">' + NL + '  <link rel="stylesheet" href="css/shop.css">'
promises = expand(read('promises.html'))
facts = expand(read('facts.html'))
header = expand(read('header.html').replace('{{MEGA_CATS}}', mega_cats()).replace('{{MEGA_PANELS}}', mega_panels()))
footer = expand(read('footer.html')).replace('.js" defer', '.js?v=' + STAMP + '" defer')

def picks():
    out = []
    for i, p in enumerate(P):
        cid, cname, col, on, *_ = CAT[p['cat']]
        out.append(f'''          <li class="kit__item" style="--c:var(--{col}); --on:var(--{on})">
            <button type="button" data-pick {add_attrs(p)} data-opts="{default_opts(p)}">
              <img src="assets/img/{p['imgs'][0]}" loading="lazy" alt="">
              <span class="kit__name">{p['name']}</span>
              <span class="kit__text">{p['text']}</span>
              <span class="kit__from">from {price(p['price'])}{icon('arrow-right', 'icon icon--sm')}</span>
            </button>
          </li>''')
    return NL.join(out)

def all_cards():
    return (NL * 2).join(product_card(p, i, reveal=False) for i, p in enumerate(P))

# Occasion drawings are written straight into the page, so they never depend on a cached copy of the icon file
def occasion_icon(oid):
    sprite = open(os.path.join(OUT, 'assets/img/icons.svg'), encoding='utf-8').read()
    m = re.search(r'<symbol id="o-' + oid + r'" ([^>]*)>(.*?)</symbol>', sprite)
    return f'<svg {m.group(1)}>{m.group(2)}</svg>'

def occasion_cards(limit=None):
    out = []
    for i, (oid, name, col, on, line, picks, img) in enumerate(OCCASIONS[:limit]):
        links = ''.join(f'<li><a href="{BY[sl]["url"]}"><span>{BY[sl]["name"]}</span><em>from {price(BY[sl]["price"])}</em>{icon("arrow-right", "icon icon--sm")}</a></li>' for sl in picks)
        out.append(f'''          <article class="occ" id="{oid}" style="--c:var(--{col}); --on:var(--{on}); --d:{i % 4}" data-reveal>
            <div class="occ__top">
              <h3 class="occ__name">{name}</h3>
              <span class="occ__badge" aria-hidden="true">{occasion_icon(oid)}</span>
            </div>
            <p class="occ__line">{line}</p>
            <ul class="occ__picks">{links}</ul>
          </article>''')
    return NL.join(out)

def fill(t):
    t = t.replace('{{PICKS}}', picks()) if '{{PICKS}}' in t else t
    t = t.replace('{{ALL_CARDS}}', all_cards()).replace('{{OCCASIONS}}', occasion_cards()).replace('{{OCCASIONS_4}}', occasion_cards(4))
    return expand(t.replace('{{PROMISES}}', promises).replace('{{FACTS}}', facts).replace('{{CHIPS}}', filter_chips()).replace('{{CARDS}}', product_cards()).replace('{{COUNT}}', str(len(P))))

pages = {
    'index.html': head('Ctrl P | Prints of your photos and art, delivered across India',
                       'Turn the photos and art on your phone into posters, stickers, booklets and merch. No minimum order, bulk pricing and delivery across India.')
                  + header + NL + fill(read('index.body.html')) + NL + footer,
    'products.html': head('Ctrl P | Everything we print',
                          'Posters, stickers, booklets, tees, totes, packaging and cards, printed with your photos and art. Order as few as one.', SHOP_CSS)
                     + header + NL + fill(read('products.body.html')) + NL + footer,
    'cart.html': head('Ctrl P | Your cart', 'Your Ctrl P cart.', SHOP_CSS, NL + '  <meta name="robots" content="noindex">')
                 + header + NL + fill(read('cart.body.html')) + NL + footer,
}
for p in P:
    pages[p['url']] = head(f'Ctrl P | {p["name"]}', html.escape(html.unescape(p['long'])), SHOP_CSS) + header + NL + product_page(p) + NL + footer

NOINDEX = NL + '  <meta name="robots" content="noindex">'
EXTRA = [
    # file, title, description, shop css?, keep out of search?
    ('create', 'Start creating', 'Pick a design, add your photo and see it on the product.', True, True),
    ('checkout', 'Checkout', 'Delivery details for your Ctrl P order.', True, True),
    ('order', 'Order placed', 'Your Ctrl P order.', True, True),
    ('track', 'Track an order', 'See where your Ctrl P order has got to.', True, False),
    ('saved', 'Saved', 'Products you have saved on Ctrl P.', True, True),
    ('occasions', 'Print for the occasion', 'Birthdays, trips, farewells, Rakhi, Diwali: what to print for each.', False, False),
    ('brands', 'Printing for brands', 'Packaging, cards, stickers and merch for small brands. Prices drop as the quantity climbs, with no minimum order.', True, False),
    ('help', 'Help', 'How ordering, artwork, bulk pricing and delivery work at Ctrl P.', False, False),
    ('about', 'About', 'Ctrl P turns the photos and art on your phone into things you can hold.', False, False),
    ('policies', 'Policies', 'Delivery, returns, privacy and terms for Ctrl P.', False, False),
    ('404', 'Page not found', 'That page is not here.', False, True),
]
for name, title, desc, shop, hidden in EXTRA:
    pages[name + '.html'] = (head('Ctrl P | ' + title, desc, SHOP_CSS if shop else '', NOINDEX if hidden else '')
                             + header + NL + fill(read(name + '.body.html')) + NL + footer)

ICON_IDS = re.findall(r'<symbol id="i-([a-z-]+)"', open(os.path.join(OUT, 'assets/img/icons.svg'), encoding='utf-8').read())
def icon_list():
    rows = []
    for name in ICON_IDS:
        cls = 'icon icon--lg iconset__rupee' if name == 'rupee' else 'icon icon--lg'
        rows.append(f'              <li><svg class="{cls}" aria-hidden="true"><use href="assets/img/icons.svg#i-{name}"/></svg>{name.replace("-", " ")}</li>')
    return NL.join(rows)

if os.path.exists(os.path.join(HERE, 'system.body.html')):
    body = fill(read('system.body.html').replace('{{CARD}}', product_card(P[0], 0, reveal=False)).replace('{{ICONS}}', icon_list()).replace('{{ICON_COUNT}}', str(len(ICON_IDS))))
    pages['system.html'] = (head('Ctrl P | Design system', 'The Ctrl P website design system: colour, type, grid, components, motion and voice.',
                                 SHOP_CSS + NL + '  <link rel="stylesheet" href="css/system.css">', NL + '  <meta name="robots" content="noindex">')
                            + header + NL + body + NL + footer)

for old in glob.glob(os.path.join(OUT, 'product-*.html')):
    os.remove(old)
for name, content in pages.items():
    assert '{{' not in content, (name, content[content.index('{{'):content.index('{{') + 40])
    open(os.path.join(OUT, name), 'w', encoding='utf-8', newline=NL).write(content)
print('wrote', len(pages), 'pages:', ', '.join(sorted(pages)))
