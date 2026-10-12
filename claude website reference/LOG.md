# Ctrl P website: session log

A record of each round: what the owner asked for, what was built, and what was decided. All rounds took place on 11 October 2026. Read `CONTEXT.md` first for the current state.

## Round 1: brief and first build (v0.1)

**Asked for:** a landing page from the Figma website file, using components like the kraft mailer mockups, clean, black and white with the brand colours used creatively, a proper grid, only the brand fonts, no small all-caps, few stickers, good copy. Questions first.

**Clarified:** the brand is B2C (first described as B2B, then corrected). Format left to me, but it must save locally and host on Netlify. Products are placeholders. Confirmed claims: no minimum order, bulk pricing, ships across India.

**Built:** a static site with a tokens file. Concept: the shipping label as a product card, with a strip of coloured tape behind it; one printed tape between sections; a one-page design system.

**Outcome:** clean, but too simple.

## Round 2: follow the concept boards (v0.2)

**Feedback:** not creative enough; the components were not taken from the reference images; the hero headline looked cropped; too many hover animations and too much movement on hover; harsh shadows; stickers placed randomly; old mascot used; the "why print" section needed images, not text. Liked the black button with the tape hover. Asked for a products page, a Products dropdown with a changing preview, custom icons, category chips, some colour sections.

**Built:** pulled the six concept boards out of Figma at full size. Rebuilt the landing page (tape-and-cyclist hero, receipt info cards, photo category tiles, yellow ticket-strip steps, photo mosaic), a products page with filters, a mega menu, 38 icons with a drawn rupee sign. Switched to the current mascot.

## Round 3: five fixes (v0.3)

**Feedback:** chips not right; menu opening without hovering; no stickers on product cards; bigger icons on product cards; display font too small in places; icons instead of coloured squares in the menu.

**Built:** chips as pointed sticker tags; menu opened by script with a delay; card titles moved to Neue Regrade; category icons in the menu.

## Round 4: icons, chips, hero (v0.4)

**Feedback:** shadows still harsh; icons inconsistent and not fitting; contrast problems; chips still not like the reference; hero layout boring, needs to convert.

**Built:** found that a CSS rule was hiding all but one menu icon. Redrew icons at 2px with solid parts. Rebuilt chips as icon tile plus label on a white die-cut backing. Bigger cyclist hero with promises and a "start with a product" chip strip. White text on pink, blue, purple and red.

## Round 5: tape everywhere (v0.5)

**Feedback:** chips better, but filter chips should be white and take colour when picked; Integral too bold in chips; cards need colour for new, discount and category; hero mostly unchanged and the chip strip looked bolted on; "what we print" boring boxes; icon strokes too thick and the black fills unwelcome; tall chips on photos looked bad; wants more of the tape idea; make the promises creative.

**Built:** icons redrawn at 1.5px, outline only. Chip labels in Neue Regrade. Tape flags and category pills on product cards. Hero as four prints taped to a wall. Promises as postage stamps. "What we print" as a big-type index with a changing preview. One taped word in every heading.

## Round 6: hero simplified (v0.6)

**Feedback:** hero overcrowded, elements placed without thought, too many things to interact with.

**Built:** one idea and one button: full-width two-line headline, lead and button on the left, the same photo on a phone and as a taped print on the right. Stamps moved to their own band.

## Round 7: the big round (v0.7)

**Feedback:** hero spacing and grouping; the same image reused; the cyclist covering the tape lettering; promises should tell a story with sticky stacking cards; the index preview should be a transparent image, not a card; **fix the navbar** (still opening by itself); chips need variety and no shadow; remove the section label lines; the black "why print" section looked wrong; rethink the footer; add filters, sort and search; more spacing in cards; design the cart and the individual product page; improve poster, sticker and card icons; research other print-on-demand sites; add colourful promotional sections.

**Built:**
- **Navbar root cause found and fixed** (an invisible but hoverable child panel).
- Product cut-outs made with OpenCV. Hero with products standing on the tape and the cyclist riding on top of it.
- Sticky stacking promise cards. Cut-out index preview. Chips with four cut ends and a hairline.
- "Why print" on white as occasion links. Fuchsia Diwali promo band. FAQ. Footer with the tape strip and a full-width colour bar.
- Products page: search, toggles, sort, bulk-quote tile, empty state.
- Twelve product detail pages and a working cart.
- Looked at Vistaprint and Walmart Photo for section structure.

**Outcome:** "a very big improvement". The promises section called beautiful; the category index and how-it-works sections liked.

## Round 8: hero fit

**Feedback:** fit the hero to the screen with the tape on the bottom edge; more space under the navbar; make the tape move as well as the postman; fewer products (boxes, packaging, stickers) and keep them out of the postman's way.

**Built:** hero exactly one screen tall on desktop; three cut-outs lifted above a clear lane; tape lettering slides with the scroll.

## Round 9: deploy

**Asked for:** deploy to Netlify with the CLI.

**Done:** new site `ctrlp-website-test` on the account already signed in (akashpai2003@gmail.com). Live at https://ctrlp-website-test.netlify.app. Notes files left out; a no-index header added so the test stays out of search engines.

## Round 10: handover documents

**Asked for:** a context file and a log so the work can continue from other accounts.

**Done:** `CONTEXT.md` and this file, plus a short `CLAUDE.md` in `D:\Beaver\Ctrl+P` that points to them. Confirmed that the page builder in this folder rebuilds the site identically.

## Round 11: image prompts for illustration

**Asked for:** a prompt to generate the hero with an illustration of Postman P and friends in place of the packaging, then prompts for every other section and component, with the reference images saved ready to drag and drop. The plan is to use the generated images as references for the next round of design.

**Done:** `image-prompt\` in this folder. One folder per section (14), each with a screenshot of the section as it is, the two Postman P images, a colour card and a `PROMPT.txt`. `README.md` there explains the workflow; `make_prompts.py` regenerates the prompts. Proposed cast: Postman P, a street dog, a cat and a pigeon, each carrying something Ctrl P prints. Nothing has been generated or changed on the site yet.

## Round 12: review comments, new flow, missing pages (v0.8)

**Asked for:** fix the sections the team commented on in Figma (page "Correction", node 310-38) with subtle changes and the same look; fix the product page, where the price showed twice and the order of things was muddled; rethink the site structure, simplify the flow, and add the pages that are missing. Reference for flow only: the older build at https://brilliant-heliotrope-f8472d.netlify.app (product page, then a three-step "make your" page, then cart). Competitors checked: Zoomin, Printo, Vistaprint India.

**The comments and what was done:**
- Menu: tape now wipes in behind the category and product names; the text and button beside the picture are gone; product names are large.
- Chips: one cut shape everywhere.
- "Screens fade. Print stays.": replaced by "What's the occasion?", four colour tickets with a product cut-out and three picks each.
- "Printing for a brand?": tape strip behind the boxes, a price-ladder slip, tape labels for who prints with us.
- Product page: one price, in a buy bar beside the one button. Order is now size, option, quantity, price, "Add your photo".
- Cart: grey background, each item on its own white slip, the receipt summary kept.
- Product card: tighter spacing; the offer flag is larger. The button now reads "Customise" and opens the product page.
- Products page: the three stamps after the grid are gone; the list ends with a line; "Can't find it here?" has its button under the copy and a picture on the right.
- "The details": the three promises sit under the heading.

**New flow:** shop, product (choose), add your photo (three steps: photo, fit, check), cart, checkout, order placed, track.

**New pages:** create, checkout, order, track, saved, occasions, brands, help, about, policies, 404. Top menu is now Shop, Occasions, For brands, Help.

**Not done:** not redeployed to Netlify. The illustrations generated from the image prompts are in the Figma file but were not asked for here and are not on the site. The design-system page was not updated.

## Round 13: product page order and spacing

**Feedback:** think like the shopper and check the order; the spacing is broken (the sticky price box sat on top of the quantity control); drop the numbers on the choices; look at how the older version set out its options.

**Done:** the buying panel now follows the older version. Order: name, description, the price (it changes with every choice), size, option, "How many" as a row of common quantities (1, 5, 10, 25, 50, or another number) with the bulk saving shown on the chip, then "Add your photo" with "Save for later" beside it and one line about what happens next. Numbers removed. The price box no longer sticks; a slim bar at the foot of the screen appears only when the price and the button have both scrolled out of sight. The details section gained "Good for" occasion tags.

## Round 14: occasion icons

**Asked for:** something other than product cut-outs to show each occasion, such as illustrations or icons.

**Done:** eight line icons (cake, suitcase, paper plane, rakhi, diya, rings, shop front, smiley) drawn in the house style and shown on a white round sticker at the corner of each occasion ticket. They live in `assets/img/icons.svg` as `o-<occasion id>`. Also removed a stray empty block that left a blank band above "The details" on product pages.

## Round 15: promises section with the crew illustrations

**Asked for:** rebuild "Print without the catch" to match the illustrated reference in Figma, using the cat, dog and pigeon artwork from the file.

**Done:** the three stamps now follow the reference: label and a large 01/02/03 along the top, the promise bottom left, the illustration in a lighter tilted window on the right, alternating tilt, the middle stamp set further left, a coral tape strip on the first and a postmark on the third. The cards were first built without the scroll stacking; the owner asked for it back, so they stick and overlap again, each leaving the label and number of the one before visible. Cards were also made taller and the illustrations larger. Artwork pulled from the Figma page "Correction" (frames Cat, Dog, Pigeon); originals are in `claude website reference\illustrations`, web versions in `assets/img/crew`. Occasion icons are now written into the page, and stylesheet and script links carry a version stamp.

## Round 16: the create flow, after the older version

**Asked for:** use the four screenshots of the older version for the flow only (design, photos, layout and text, preview), reachable from the product page and from every "Start creating" button. Do not change the existing look.

**Done:** `create.html` now has four steps. Design: Plain, Instant (white frame) or Night (black frame), all placeholders. Photos: thumbnails with a remove button, "Add more", a count, a sample option; one photo for most products, three for die-cut stickers, six for the sticker pack. Layout: border, caption (22 characters, with a counter), fit, zoom, turn. Preview: a summary, "Change size or options", "Share preview" (shares the product link for now), then "Add to cart". Every "Start creating" button opens `create.html#pick`, which asks which product first; the product page button is also "Start creating" and carries the chosen options in. No existing component styles were changed; the new pieces reuse the step tabs, option buttons, inputs and summary rows.

## Open at the end of the session

- Waiting on the owner's view of the new flow and pages, and on whether the generated illustrations (now in the Figma file) should be built into the site.
- Decisions the owner needs to make: accounts and sign-in (none designed), payment methods, delivery cost and times, returns policy.
- Replace placeholder products and prices with real ones; real product photography.
- Three copy claims and the Integral CF web licence still need confirming. See `CONTEXT.md`.
