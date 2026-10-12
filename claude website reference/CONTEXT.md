# Ctrl P website: context for continuing the work

Read this first, then `LOG.md` (same folder) for how we got here. Everything a new session needs is in this folder and the site folder; nothing depends on the original chat.

Last updated: 11 October 2026, at version 0.8.

## What this is

A design test for the Ctrl P website: a landing page, a products page, product detail pages and a cart, built to settle the design system and visual look before the rest of the site is designed. The owner (Akash, working with Beaver Studio / Bang Design) judges it on whether it looks like senior designers made it, and on one recurring question: **does it feel like a print-on-demand shop, and does it make people want to print something?**

## The brand, in brief

- **Ctrl P** is a B2C print-on-demand brand in India (parent company Sumulas). You turn photos and art into posters, stickers, booklets, tees, totes, packaging and cards. Young businesses are the secondary audience.
- Audience: 18 to 28, urban India, gifting-led. Tone: a friend who gets you; specific, a little cheeky, never salesy.
- Mascot: **Postman P**. The current version carries the pill-shaped logo (`MASCOT.png`); `Mascot-1.png` is the old one. A cycling version exists too.
- Fonts (the only two allowed): **Integral CF Extra Bold** (caps-only display) and **Neue Regrade** (everything else).
- Palette: black, white, and six accents. Coral `#F9423A`, sunglow `#FFC72C`, turquoise `#2AD2C9`, royal `#307FE2`, fuchsia `#7D55C7`, rose `#EF426F`.
- **Confirmed claims, the only ones copy may state as fact:** no minimum order, bulk pricing, ships across India.

## Where everything is

| Path (under `D:\Beaver\Ctrl+P`) | What it is |
| --- | --- |
| `claude website test\` | The site. Plain HTML, CSS and one script. This is what gets deployed. |
| `claude website test\DESIGN.md` | Design decisions, tokens, placeholders and open questions. Keep it current. |
| `claude website reference\page-builder\` | `build.py` plus the page partials and all product data. **Edit here, then rebuild.** |
| `claude website reference\page-builder\cutouts.py`, `cutouts2.py` | How the transparent product cut-outs were made (OpenCV). |
| `claude website reference\concept-boards\` | Six ChatGPT concept boards from the Figma file. The owner's visual reference for components. |
| `claude website reference\image-prompt\` | Prompts and drag-and-drop reference images for generating illustrations, one folder per section. Start with its `README.md`. |
| `claude website reference\CONTEXT.md`, `LOG.md` | This file and the session log. |
| `.claude\launch.json` | Local preview server config, name `ctrlp-site`, port 4173. |
| Rest of `D:\Beaver\Ctrl+P` | Brand source material: logo, stickers, mascots, mockups, photos, fonts. |

Figma sources (both open view-only in a browser without signing in):
- Website file with concept boards and the discovery questionnaire: https://www.figma.com/design/JOTTO1fTwkBxefaESlpiHE/CTRL-P-Website?node-id=291-2
- Final brandbook: https://www.figma.com/design/c1HJR17MrOAwomuz98x53i/CtrlP---Clientele-Access?node-id=812-2

## How to work on it

**Edit and rebuild.** The HTML pages share a header, footer and product data, so they are generated:

```bash
python "D:/Beaver/Ctrl+P/claude website reference/page-builder/build.py" "D:/Beaver/Ctrl+P/claude website test"
```

- Page bodies: `index.body.html`, `products.body.html`, `cart.body.html`, `system.body.html`. Shared: `header.html`, `footer.html`, `promises.html`, `facts.html`.
- Product data, categories, the product page template and the product card live in `build.py`.
- Shorthand in partials: `{{I:name}}` icon, `{{Is:name}}` small icon, `{{Il:name}}` large icon, `{{P:199}}` price with the drawn rupee sign.
- CSS and JS are edited directly in the site folder: `css/tokens.css`, `css/styles.css` (shared components and landing page), `css/products.css` (product cards, products page), `css/shop.css` (search and filters, product page, cart), `css/system.css`, `js/main.js`.

**Preview.**

```bash
python -m http.server 4173 --directory "D:/Beaver/Ctrl+P/claude website test"
```

Then open http://localhost:4173. Fonts need HTTP, so do not open the files directly. Press **G** on any page for the column grid overlay.

**Deploy.** Live at **https://ctrlp-website-test.netlify.app** (Netlify site `ctrlp-website-test`, project ID `b49da173-c092-4fa5-8cf6-f9ac77bc8605`, on the account akashpai2003@gmail.com, team slug `akashpai2003`). To redeploy:

1. Copy `assets`, `css`, `js` and all `*.html` from the site folder to a temporary folder. Leave out the `.md` notes.
2. Add a file named `_headers` containing two lines: `/*` then `  X-Robots-Tag: noindex`. This keeps the test, with its placeholder prices, out of search engines. Remove it only when the owner says so.
3. From that folder: `netlify deploy --prod --dir . --site b49da173-c092-4fa5-8cf6-f9ac77bc8605 --no-build`

A different account needs its own `netlify login`, and either access to that site or a new one.

## Current state (version 0.8)

**Site structure.** Top menu: Shop (menu of categories and products), Occasions, For brands, Help. Tools: search, saved, cart, "Start creating".

| Page | File | Job |
| --- | --- | --- |
| Home | `index.html` | Sell the idea, lead into the shop |
| Shop | `products.html` | Everything, with search, filters and sort |
| Product | `product-*.html` (12) | Choose size, option and quantity. One price, one button: "Add your photo" |
| Start creating | `create.html` | Opens on a product picker when reached from a "Start creating" button (`#pick`). Then four steps: design, photos, layout and text, preview. Then "Add to cart" |
| Cart | `cart.html` | Review, change photo, quantities |
| Checkout | `checkout.html` | Who, where, how to pay. Demo only |
| Order placed | `order.html` | Order number and what happens next |
| Track | `track.html` | Look an order up by number. Demo only |
| Saved | `saved.html` | Products the heart was tapped on |
| Occasions | `occasions.html` | Eight occasions, three picks each |
| For brands | `brands.html` | Bulk pricing, what brands print, quote form |
| Help | `help.html` | Questions by topic, contact form |
| About, Policies, 404 | `about.html`, `policies.html`, `404.html` | Story; policy headings (text to be written); not found |
| Design system | `system.html` | Not updated for v0.8 |

**The ordering flow:** Shop, Product, Add your photo, Cart, Checkout, Order placed, Track. The product page only chooses; nothing goes in the cart without a photo. Choices travel between pages in the browser (`localStorage`: `ctrlp-draft`, `ctrlp-cart`, `ctrlp-orders`, `ctrlp-last-order`, `ctrlp-saved`). Nothing is sent anywhere, and the pages say so.

New files: `css/flow.css` (the flow pages and the revised sections) and `js/flow.js` (create, checkout, order, track, saved, demo forms). `js/main.js` exposes `window.CtrlP` for it.

**The idea:** the interface is made from what a Ctrl P parcel looks like, and tape is the thread through all of it.

Landing page, top to bottom:
1. **Hero** (graph paper). Exactly one screen tall on desktop, tape on the bottom edge. Full-width two-line headline "Off your phone. Into their hands." with "hands." taped over in coral. Lead, one large button and a note grouped on the left; three product cut-outs (boxes, mailer, sticker pack) on the right, kept above a clear lane. Postman P rides along the top of the tape as the page scrolls while the tape lettering slides the other way.
2. **Promises** (light grey). Sticky heading on the left; three large stamp cards on the right that stack as you scroll: "Order just one", "Or a hundred", "Sent anywhere".
3. **What we print** (white). Big-type category index with prices; a row is taped over on hover and the cut-out product beside the list changes. Six more categories as chips.
4. **How it works** (sunglow). Four perforated ticket stubs with icons.
5. **What's the occasion?** (light grey). Four colour tickets, each with a product cut-out and three picks; links to the occasions page.
6. **Promotion** (fuchsia). Example Diwali campaign.
7. **For brands** (grey), **Questions** (white), **closing call to action** (graph paper), **footer** opening with the tape strip and ending on a full-width colour bar.

Shop:
- **Products page:** search, "On offer / New / Bulk rates" toggles, sort, category chips (one cut shape), product cards with a "Customise" button, a turquoise bulk-quote tile, an empty state, an end-of-list line.
- **Product page:** gallery; name, description, one live price; rows of options (size, option, how many); "Add your photo" with "Save for later". A slim bar repeats the price at the foot of the screen only when the main one is out of sight.
- **Cart, checkout, order:** light grey background, white slips, receipt summary, a three-step tape trail.

Components worth knowing: the tape button (black, pinked ends, coral tape wipes across on hover), `.taped` headline word, `.flag` tape flag, `.chip` sticker-tag chip with four cut variants, `.cat` category pill, `.vow` stacking card, `.pcard` receipt product card, `.stubs` ticket strip, `.index` category index, 38 outline icons in `assets/img/icons.svg`.

## The owner's rules (learned the hard way)

**Likes, keep these:** the tape button and its hover; tape used across the site; the cycling Postman P and tape animation; the stacking promises section ("beautiful"); the category index; the how-it-works strip; the product cards; for-brands and closing sections.

**Do:**
- Follow the concept boards for components. Be creative and visual, not minimal. More images, less text.
- Keep it clean and on the 12-column grid. Tight heading-to-subheading spacing and clear grouping.
- Use colour where it means something (category, new, discount, promise) and in full colour sections to break up the black and white.
- Thin outline icons (1.5px), sized to fit their container.
- Product images as transparent cut-outs rather than boxed photos where possible.
- Ask clarifying questions before starting a new piece of work.

**Don't:**
- Integral CF at small sizes (keep it at 28px and up), or all-caps small text.
- Hover effects on everything, or anything that moves position on hover.
- Drop shadows, beyond a barely visible contact shadow.
- Stickers placed loosely, or on product cards.
- A black section next to white and yellow ones.
- Internal labels on the live page (the "What we print / 12 categories" running headers were removed).
- Grids of plain square containers for categories.
- An overcrowded hero: one idea, one button, few things to click.
- Reusing the same photo across sections.
- Low-contrast text: pale grey body copy, or black type on pink, blue or purple.

## Placeholders and open questions

- Categories, the twelve products, options, every price, the "New" and "% off" flags, and the bulk tiers (10% off from 10 pieces, 20% from 50) are stand-ins.
- The Diwali band is an example campaign, not a real offer.
- Photos and cut-outs come from brand mockups and are reused because there are few. Real product photography is the fix. The tote cut-out has no handles; the booklet has a thin grey edge.
- Copy to confirm with the owner: "You'll see a preview before you order", "the range is still growing".
- Not built: accounts and sign-in, real payment, real file upload to a server, a text or layout editor in the photo step.
- Placeholder in v0.8: payment methods (UPI, card, net banking), the eight occasions and their picks, order numbers and tracking stages, the quote and contact forms (they send nothing), all policy text.
- "Delivery: shown before you pay" appears in the cart and checkout because delivery cost is not confirmed.
- Check that the Integral CF licence covers web use before launch.
- Figma review comments live on the page "Correction" of the website file (node 310-38). Text notes can be read from the layers panel in a browser.

## Practical notes for an AI assistant picking this up

- **Menu bug history.** The Products menu once opened when the pointer was nowhere near it. Cause: the closed panel was `visibility: hidden` but its active child had `visibility: visible`, so it stayed hoverable. Fixed with `pointer-events: none` on the closed menu, `visibility: inherit` on the child, and opening only from the Products link. Don't reintroduce it.
- The preview server sometimes stops by itself. Check it responds before taking screenshots.
- Headless browser screenshots report a viewport about 90px shorter than the window, so anything using viewport height (the hero) looks short there. Verify viewport-fit in a real browser.
- Design skills used: the UI Skills registry entries `pbakaus/impeccable`, `pbakaus/shape`, `zeke/swiss-design`, `mengto/landing-page`, `jalaalrd/anti-ai-slop-writing`.
- Figma connectors were not available. Both files load view-only in a browser. Raster images can be pulled by reading the file's `image/batch` request; vectors cannot.
- When reporting to the owner: say plainly what changed, what is placeholder, and what was not checked.
