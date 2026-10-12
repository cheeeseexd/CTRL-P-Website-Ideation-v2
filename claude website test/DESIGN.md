# Ctrl P website: design notes

Version 0.7. A design test built to settle the design system and visual look before the rest of the site is designed.

## Pages

- `index.html`: landing page.
- `products.html`: all products, with search, filters and sorting.
- `product-*.html`: one page per product (twelve), with options, quantity, bulk tiers and add to cart.
- `cart.html`: the cart. It reads what was added in this browser.
- `system.html`: the design system in the browser.

Press **G** on any page to lay the column grid over the design.

## Sources

| Source | What was taken from it |
| --- | --- |
| Brandbook (Figma, "CtrlP - Clientele Access", Final) | Positioning, personality, palette, type hierarchy, mascot, sticker and pattern usage |
| Concept boards (Figma, "CTRL P Website") | Tape and cyclist, sticker-tag chips, product card anatomy, line icons, Products menu with a changing preview. Saved in `../claude website reference/concept-boards` |
| Local `Ctrl+P` folder | Logo, stickers, Postman P, mockups, brand photos, fonts |
| Vistaprint and Walmart Photo (looked at for structure only) | Which sections a print shop needs: shop by category, shop by occasion, how it works, bulk, FAQ, upload-first product page with quantity pricing |

## The idea

The interface is made from what a Ctrl P parcel looks like, and tape is the thread through all of it.

- **Tape.** One word in each heading is taped over. Buttons, category rows, photo captions, filters and options are taped across on hover or when picked. A strip of Ctrl P tape closes the hero and opens the footer.
- **Hero.** Exactly one screen tall on a desktop, with the tape on the bottom edge. Headline, then the lead, button and note as one group beside three products (boxes, mailer, sticker pack). Below them a clear lane is kept for Postman P, who rides along the top of the tape as the page scrolls while the tape's lettering slides the other way.
- **Promises.** Three large stamp cards that stack on top of each other as you scroll, telling one story: order just one, or a hundred, sent anywhere.
- **Category index.** A list of big names with prices. Pointing at a row tapes it over and swaps the cut-out product beside the list.
- **Sticker tags.** Category chips: an icon tile and a label on one white die-cut backing, the right end cut four different ways. A hairline marks the edge; there is no shadow.
- **Receipts and tickets.** Product cards and the cart summary are till receipts. The steps and the bulk tiers are perforated ticket stubs.
- **Stickers.** Only as products or on something physical. Never loose on the page, never on product cards.

## Landing page, top to bottom

1. Hero (graph paper)
2. Promises that stack (light grey)
3. What we print: category index (white)
4. How it works: four ticket stubs (sunglow)
5. Shop by occasion: four photo links (white)
6. Seasonal promotion (fuchsia). Placeholder campaign.
7. For brands (grey)
8. Questions (white)
9. Closing call to action (graph paper), footer

## Colour

Black and white carry most of the page. Colour is used where it tells you something: a category, something new, a discount, a promise, plus one or two full colour sections per page. There is no black section.

| Token | Value | Use |
| --- | --- | --- |
| `--ink` / `--paper` | `#000000` / `#FFFFFF` | Type, rules, buttons; page and paper components |
| `--tint-1` / `--tint-2` | `#F4F4F4` / `#E7E7E7` | Quiet bands; `--tint-2` matches the studio grey of the mockups |
| `--coral` | `#F9423A` | The tape, discounts, Packaging |
| `--sunglow` | `#FFC72C` | How it works, "New", Posters |
| `--turquoise` | `#2AD2C9` | Bulk, Cards |
| `--royal` | `#307FE2` | Merch |
| `--fuchsia` | `#7D55C7` | Promotion band, Booklets |
| `--rose` | `#EF426F` | Stickers |

On sunglow and turquoise, type is black. On fuchsia it is white at any size (5.3:1). On rose, royal and coral, white is used only for bold labels and large type.

## Type

| Role | Face | Size |
| --- | --- | --- |
| Display, headings, category index, prices | Integral CF Extra Bold | 28px and up |
| Card titles, questions | Neue Regrade 700 | 22 to 30px |
| Lead / body | Neue Regrade 400 to 450 | 18 to 22px / 17px |
| Chips, flags, labels | Neue Regrade 600 to 700 | 13 to 16px, sentence case |

## Icons

38 icons drawn for Ctrl P in `assets/img/icons.svg`: a 24px grid, a 1.5px line with rounded joins, outline only. A rupee sign is drawn to sit beside Integral CF, which has none.

## Motion and hover

- Tape wipes in from the left: over a headline word, across a button, row, caption, filter or option.
- The hero headline rises line by line and the products step onto the tape, once, on load.
- Content fades up 16px as it enters the screen. Postman P rides with the scroll. Nothing loops.
- The promise cards stack with plain sticky positioning; no scroll hijacking.
- Nothing changes position on hover. No drop shadows beyond a faint contact shadow under cut-outs.
- **Products menu:** only the Products link can open it, with a mouse resting on it or the down arrow key. While closed it takes no pointer events. Scrolling, leaving, clicking a link or Escape closes it.

All motion switches off under `prefers-reduced-motion`.

## Placeholders and open questions

- **Range and prices.** The categories, twelve products, their options, every price, the "New" and "% off" flags, and the bulk tiers (10% off from 10 pieces, 20% off from 50) are stand-ins.
- **Promotion.** The Diwali band is an example campaign, not a real offer.
- **Photos.** Product photos and cut-outs come from the brand mockups in the folder. They are reused across pages because there are only so many; real product photography will fix that. The poster and sticker cut-outs are composed from brand artwork.
- **Copy to confirm.** "You'll see a preview before you order" (product page and FAQ), "the range is still growing".
- **Not built.** Checkout, account, the customiser and real file upload. The cart is stored in the browser only; the upload field shows the chosen file name and does nothing else.
- **Font licences.** Check that the Integral CF licence covers web use before launch.

## How the pages are put together

The pages share a header, footer and product data, so they are assembled by a small script kept outside this folder, in `../claude website reference/page-builder` (`python build.py "<this folder>"`). The published folder is plain HTML, CSS and one script, and needs no build step to host.

## v0.8: flow and structure

- **One price per page.** On the product page the price sits under the description and changes with every choice. A slim bar at the foot of the screen repeats it only while the price and the button are both out of sight.
- **Choices are plain rows of options,** in the order size, option, how many. "How many" offers 1, 5, 10, 25, 50 or another number; bulk savings are written on the chips. No step numbers.
- **Choose, then make.** The product page chooses; `create.html` adds the photo in three steps (photo, fit, check); only then does it go in the cart. Product cards say "Customise", not "Add to cart".
- **Flow pages are grey with white paper.** Cart, checkout and order use `--tint-1` with white slips and the receipt summary. A three-piece tape trail shows where you are.
- **Chips use one cut.** The four variants are gone.
- **Menu.** Tape wipes in behind category and product names; product names are set large; one picture, no caption.
- **Occasion ticket (`.occ`).** Colour top with a torn edge and a cut-out leaning out of it, one line, three picks.
- **Price ladder (`.ladder`).** A slip of paper with three bars that shorten as the run gets longer.
- New files: `css/flow.css`, `js/flow.js`. The design-system page has not been updated for these.
