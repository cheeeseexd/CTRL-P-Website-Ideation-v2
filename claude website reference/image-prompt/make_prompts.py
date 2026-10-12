"""Writes PROMPT.txt into each section folder and README.md beside this file.
Run again after changing the cast, the rules or a section idea:  python make_prompts.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CAST = """The cast, the same in every section: Postman P (the character in images 2 and 3), a lean tan Indian street dog with pointed ears and a curled tail, a cat, and a pigeon. If a fifth image is attached, it is the approved hero illustration: match its dog, cat and pigeon exactly."""

SPACE = """Space comes first. This section must feel open and uncrowded.
- Text and illustration each get their own zone. They never overlap and never touch: no paw, tail, wing, box, string or dotted line crosses into a text zone.
- Illustrations are small and simple. Leave empty background all around each one, at least a quarter of its own width on every side.
- Keep the gaps between elements even and generous. If something does not fit comfortably, make it smaller or leave it out. Never shrink the gaps to make room."""

STYLE = """Style: identical to images 2 and 3, as if the same illustrator drew it on the same day. Flat vector shapes, no outlines, chunky rounded forms with a few sharp corners, two or three flat tones per shape with hard-edged shading. No soft gradients, no airbrushed fur, no glossy highlights, no texture, no grain, no 3D, no realism. A white oval eye with a small dot pupil, a big rounded pink nose, big heavy feet. Animals are built the same way as the postman.

Colour: follow image 4. Characters use only the Postman P colours: kraft tan and brown, charcoal navy, soft pink, lilac grey, white. The six brand accents (coral, sunglow, turquoise, royal blue, fuchsia, rose) appear only on printed things and tape. The only shadow allowed is one flat, pale contact shadow under each figure. No drop shadows on cards or panels."""

FIXED = """Do not change: the wording, the fonts, the brand colours, the order of the content and the overall width of the section. Add no new text beyond what is listed above, no speech bubbles, no sparkles, no confetti, no floating icons, no extra characters. If in doubt, draw less."""

OUT = "Output: same width and framing as image 1 (it may be a little taller if the section needs the room), crisp and high resolution."

def mock(intro, pictures, components):
    return ("Edit image 1, a section of the Ctrl P website. " + intro.strip() + "\n\n" + SPACE
            + "\n\nIllustration:\n" + pictures.strip()
            + "\n\nSubtle changes to the components, to make the section more creative. Use these and nothing more:\n" + components.strip()
            + "\n\n" + CAST + "\n\n" + STYLE + "\n\n" + FIXED + "\n\n" + OUT + "\n")

def alone(what, refs="images 1 and 2", colours="image 3"):
    s = STYLE.replace("images 2 and 3", refs).replace("image 4", colours)
    c = CAST.replace("images 2 and 3", refs).replace("If a fifth image is attached", "If a fourth image is attached")
    return (what.strip() + "\n\nKeep every illustration simple and small within its space, with clear white all around it. Nothing touches the edge of the picture or a neighbouring illustration.\n\n"
            + c + "\n\n" + s + "\n\nPlain white background, nothing else in the picture, no text. High resolution.\n")

SECOND = "\n--- Second prompt: %s ---\n%s\n\n"

S = {}

S["02-promises"] = ("Promises: three stamp cards", "Liked as it is. Cards become more like real stamps.", mock(
"Give the three stamp cards an illustration each and make them feel more like real postage stamps. The heading and paragraph on the left do not change.",
"""Each card is split in two: the left 60 percent is text only, the right 40 percent is illustration only. The small label stays top-left; the headline and its paragraph sit together bottom-left, the paragraph wrapping inside the left zone. All three cards are the same size, about 15 percent taller than now, with an even margin inside on all four sides and larger gaps between them.
1. Yellow card, "Order just one": the cat standing on its hind legs, holding one single small sticker above its head like a trophy.
2. Turquoise card, "Or a hundred": the dog pulling a little trolley with three stacked kraft boxes.
3. Purple card, "Sent anywhere": the pigeon in flight carrying a small parcel on a string, one short curved dotted line trailing behind it.""",
"""- Each illustration sits in its own window, as on a real stamp: a slightly lighter panel of the card's own colour with a thin inner border. One small part may break out of the frame (the raised paw, the top box, a wing).
- The step number becomes a stamp value: a large "01", "02", "03" in the top-right corner of each card in the heavy display font, replacing the small number beside the label and the small line icon.
- Tilt the cards very slightly, alternating: one degree left, one degree right, one degree left.
- One round postmark of thin white wavy lines overlapping a corner of the third card only. Lines only, no lettering.
- One short strip of coral tape across the top-left corner of the first card."""))

S["03-what-we-print"] = ("What we print: category index", "Liked as it is. The illustration replaces the product photo beside the list.", mock(
"Replace the two photographic poster prints on the right of the list with one illustration. The list keeps its rows, names and prices.",
"""One illustration, in the same place as the photos and no larger than they are now, with nothing behind it (no card, no panel): Postman P on tiptoe pressing a strip of coral tape onto the top corner of a large poster, while the cat stretches up to hold the bottom corner flat. The poster is a simple abstract print in coral, fuchsia and sunglow. It stays clear of the list on its left and the paragraph above it.""",
"""- The small row numbers (01 to 06) become small round stickers: a filled circle in a different brand accent for each row, the number inside.
- The yellow tape over the highlighted row gets pinked, zigzag-cut ends and runs a little past the list on the left, as if stuck on by hand.
- The caption under the illustration sits on a small white paper label held by one short strip of tape at its corner, tilted one degree.
- Add a little more space between the heading and the list.""")
+ SECOND % ("one matching illustration per category", "Give it the two Postman P images and the colours image only.") + alone("""
A sheet of six separate spot illustrations in a 3 by 2 grid with wide white gaps, each the same size and each showing a different product being enjoyed:

1. Posters: Postman P on tiptoe taping a large poster to a wall, the cat holding the bottom corner.
2. Stickers: the dog sitting patiently, covered in round and die-cut stickers, while the cat presses one more onto its nose.
3. Booklets: Postman P sitting on the ground reading an open photo booklet, the pigeon perched on the top edge of the page.
4. Tees: the dog wearing a printed t-shirt several sizes too big, looking delighted.
5. Tote bags: Postman P carrying a printed tote on his shoulder with the cat's head poking out of it.
6. Packaging: Postman P sealing a kraft box with coral tape, the cat already sitting inside another open box beside it.
"""))

S["04-how-it-works"] = ("How it works: four ticket stubs", "Liked as it is. Stubs become more like real tickets.", mock(
"Replace the four small line icons with illustrations and make the white stubs feel more like a strip of real tickets. The heading stays, and the kraft mailer photo in the top-right corner stays.",
"""Each stub is split in two, top and bottom: the top half holds one small illustration, centred, and the bottom half holds the step title and its description. Make the stubs about 40 percent taller than now so both halves have room.
1. Pick: the cat sitting between a small poster and a small tote bag, one paw on its chin, deciding.
2. Upload: the pigeon tugging a photo out of the top of an upright phone, as if pulling a print from a slot.
3. Print: the dog watching, nose close, as a printed sheet rolls out of a small printer.
4. Post: Postman P on his bicycle from image 3, riding off to the right with a kraft mailer in his backpack.""",
"""- A dotted tear line separates the top half of each stub from the bottom half, with a small semicircular notch punched at each end of the line.
- The step number becomes large: "01" to "04" in the heavy display font in the top-left corner of each stub, in sunglow yellow so it is quiet against the white.
- The fourth stub is torn off: a slightly wider gap before it, and it is tilted two degrees, as if it has just been handed over.
- Remove the dotted squares that framed the old icons.""") )

S["05-occasions"] = ("Shop by occasion: four photo links", "Photos stay. They become pinned-up prints.", mock(
"The four photographs keep their content exactly. Present them as real prints pinned up by the crew. The heading and the short paragraph beside it do not change.",
"""Two small figures only, both sitting on the outside of a photo, never over its subject:
1. The pigeon perched on the top edge of the tall left-hand photo, looking down into it.
2. The cat sitting on the top edge of the bottom-right photo, its tail hanging just over the corner.""",
"""- Give every photo a thin white border, like a photographic print.
- Tilt each print slightly and differently, between one and two degrees, and widen the gaps between them so no two touch.
- Each coloured category label becomes a strip of tape that holds its print to the page: it sits half on the print and half off, at the top-left corner, with cut ends.
- Each caption sits on a small white paper label overlapping the bottom edge of its print, instead of a block inside the photo.""")
+ SECOND % ("four new photographs, so no photo is used twice on the site", "Give it image 1 of this folder only.") + """Four separate photographs in the same warm, natural, slightly moody style as the photos in the reference image. Real people and places in urban India, age 18 to 28, candid, nobody looking at the lens. Shot on a 35mm lens, soft window or evening light. Simple, uncluttered frames with one clear subject and plenty of calm background.
1. Trips: a friend seen from behind at a hill-station cafe wearing an oversized white tee with a colourful print on the back.
2. Rakhi: a laptop lid and a water bottle covered in bright die-cut stickers, a rakhi thread on a wrist at the edge of the frame.
3. Farewells: hands passing a printed cream tote bag across a college canteen table.
4. Birthdays: a large poster being unrolled on a bed, wrapping paper and ribbon pushed to one side.
The printed artwork on each product is simple flat shapes in coral, sunglow, turquoise, royal blue, fuchsia and rose. No readable text and no logos; the logo is added afterwards.
""")

S["06-promo"] = ("Promotion: Diwali band", "Replace the loose sticker cluster.", mock(
"Remove the cluster of stickers on the right of the purple band and replace it with one illustration. The headline, paragraph and white button on the left do not change.",
"""One illustration in the right 40 percent of the band, well clear of the headline, feet on a common ground line: the crew hanging a festive garland of printed photographs. Postman P reaches up to tape one end of a string of five small square photo prints, strung like a toran, that swoops across to the pigeon holding the other end in its beak. The dog sits below wearing a marigold garland. The cat bats at the lowest print. Three small lit clay diyas stand in a row on the ground. The prints are in sunglow, coral, rose and turquoise so they glow against the purple. Keep the figures small enough that there is empty purple above and beside the group.""",
"""- The top and bottom edges of the purple band are cut in a zigzag, like a strip of tape cut with pinking shears.
- The small "Diwali is coming" label becomes a paper luggage tag: one end pointed with a punched hole and a short loop of string, tilted two degrees.
- Add more space between the headline and the paragraph's button below it, and between the label and the headline.""") )

S["07-for-brands"] = ("For brands: bulk orders", "Liked as it is. The box photo stays.", mock(
"The photograph of the two kraft boxes stays exactly as it is. Add the crew at a small scale and one piece of tape. The headline, paragraph and button do not change.",
"""Two small figures beside the boxes, as if getting a big order out of the door: Postman P to the right of the lower box, leaning his shoulder into it to push, and the cat sitting upright on top of the upper box like a supervisor. They stand on the same ground as the boxes and stay entirely in the right half of the section.""",
"""- One long strip of turquoise tape with a fine white grid runs behind the boxes across the right half of the section, at a slight upward angle, its cut ends visible. The boxes sit in front of it.
- A small white shipping label, blank except for a few grey lines and a barcode, is taped at a slight tilt in the empty space above the boxes.
- Move the boxes a little to the right so the gap between the text and the picture is wider.""") )

S["08-questions"] = ("Questions", "The left column under the heading is empty.", mock(
"Add one illustration in the empty space under the \"Asked a lot.\" heading, and give the list of questions a little more character. The questions and the answer keep their wording.",
"""One illustration under the heading on the left, about the height of two question rows, with clear space between it and the heading: Postman P sitting on a small kraft box, reading a long letter that unrolls over his knees and trails along the ground, the dog looking over his shoulder. The letter is plain white with a few grey lines standing in for writing and one strip of royal blue tape at the top. It stays entirely in the left column.""",
"""- The open answer sits on a slip of white paper with a torn, uneven bottom edge, tucked under its question, tilted half a degree.
- The plus and close signs at the end of each row sit inside small round stickers, royal blue for the open row and black outline for the rest.
- Slightly more height in every row.""") )

S["09-closer-and-footer"] = ("Closing call to action and footer", "Finish the story the hero started.", mock(
"Postman P carrying the logo sign stays exactly as he is. Add his friends, and let the coral tape come off a real roll. The headline, paragraph, button and footer links do not change.",
"""1. The three friends follow Postman P at a matching, small scale, walking the same way along the top edge of the coral tape strip with even gaps between them: the dog with a rolled poster in its mouth, then the cat riding in a small open kraft box on wheels pulled by a string, and the pigeon flying just above the dog. They stay to the right of the headline and button and never overlap them.
2. In the footer, at the far right above the copyright line, the bicycle from image 3 leaning on its stand with no rider, small, as if parked for the night.""",
"""- The coral tape strip no longer runs off the right edge. It ends at a roll of coral tape standing on its side at the far right, as if the whole strip has been pulled from it.
- At the left edge the strip ends in a zigzag cut.
- In the footer, each column heading (Shop, Help, Company) sits on a short strip of tape in a different brand accent with white or black lettering, whichever reads clearly.
- A little more space above the footer columns.""") )

S["10-products-page"] = ("Products page: heading", "The right side of the heading is empty.", mock(
"Add one illustration in the empty area to the right of the \"Everything we print.\" heading. The search bar, filters, chips and product cards keep their content.",
"""A washing line of freshly printed things, no taller than the heading block and kept entirely in the right half: a string runs across at a slight sag. Pegged along it, left to right with even gaps: a poster, a printed t-shirt, a tote bag, a sheet of stickers and a greeting card, each a simple flat shape with artwork in the brand accents. The pigeon holds the right-hand end of the string in its beak; the cat stretches up from below towards the tote bag without touching the heading's paragraph.""",
"""- The pegs holding the prints are short strips of tape in different brand accents.
- The thin rule under the heading area becomes a dashed cut line with a small notch at each end.
- The product count ("12 products") sits on a small round white sticker with a thin black border.
- Slightly more space between the search row and the row of chips.""") )

S["11-product-card"] = ("Product card", "Cards are liked. The picture changes; small touches below it.", """Edit image 1, a row of three product cards from the Ctrl P website.

The picture: replace each photograph with the same product shown as a clean studio cut-out, straight on, centred, on a flat panel of that card's category colour: sunglow yellow for the poster, rose pink for the stickers, royal blue for the t-shirt. The product fills no more than 60 percent of the panel, with empty colour all around it. Soft, even light, a barely visible contact shadow, no props, no hands, no background scene. The products are real, photographed objects, not illustrations: a poster sheet, a set of die-cut stickers, a folded white t-shirt with a print on the chest. Their artwork is simple flat shapes in the Ctrl P brand colours from image 4.

Subtle changes to the card, to make it more creative. Use these and nothing more:
- One short strip of white paper tape holds each product to its panel at the top, slightly off-centre and at a slight angle, different on each card.
- A dotted tear line with a small semicircular notch at each end separates the picture from the information below, like a ticket.
- The starting price sits on a small white price tag: a rectangle with one pointed end and a punched hole.
- Slightly more space between the product name, the description and the row of three facts.

Do not change: the wording, the fonts, the heart button, the tape flag, the category pill, the three facts and the Add to cart button. No drop shadows. Add no text. No characters or mascots on the cards.

Output: same width and framing as image 1 (it may be a little taller if the cards need the room), crisp and high resolution.
""")

S["12-product-page"] = ("Product page", "Gallery image and the empty space beside The details.", mock(
"Change the gallery picture, add one small illustration beside \"The details.\", and give the page a few print-shop touches. The product name, price, options, quantity, tiers and button keep their content.",
"""1. Gallery: replace the photograph with a single poster shown straight on as a clean studio cut-out on a flat sunglow yellow panel. The poster is a real photographed object with simple flat artwork in the brand colours, filling no more than 60 percent of the panel. The three thumbnails show the same poster straight on, rolled, and in a close-up of one corner.
2. In the grey "The details." section, in the empty space under that heading and well clear of it: Postman P bending forward to inspect the corner of a poster through a round magnifying glass, the pigeon standing on the poster's edge looking at the same spot. Small, about the height of three rows of the specification list.""",
"""- The gallery panel is held by two short strips of tape at its top corners, in place of the single strip at the top centre.
- The specification list sits on a white paper receipt: the bottom edge cut in a zigzag, the whole list tilted one degree.
- The selected size and paper options look like labels stuck on with tape: a yellow strip with cut ends behind each selected option.
- A little more space between the option groups in the right column.""") )

S["13-cart"] = ("Cart", "The summary becomes a printed receipt; plus an empty state.", mock(
"Make the order summary feel like a receipt that has just been printed, and add one small figure. The items, quantities, prices and button keep their content.",
"""One small figure at the foot of the order summary, beside the barcode, about as tall as the barcode and the checkout button together: the cat sitting upright, holding the torn-off end of the receipt in its mouth. It does not overlap any line of the summary.""",
"""- The order summary is a strip of white receipt paper: the top edge straight, the bottom edge torn in a zigzag, tilted one degree, with a thin dashed line above the total.
- Each line item's thumbnail is a small print held by a short strip of tape at its top, tilted slightly.
- The "bulk saving" note on the second item is a small turquoise tape flag with cut ends.
- More space between the two line items, and between the list and the summary.""")
+ SECOND % ("empty cart illustration", "Give it the two Postman P images and the colours image only.") + alone("""
One spot illustration for an empty shopping cart: Postman P holding his black backpack upside down and shaking it, nothing falling out except one small coral sticker. The dog sits beside him looking up into the open bag, head tilted. Landscape, about 3:2.
"""))

S["14-spot-illustrations"] = ("Small moments: empty states and messages", "New pieces. No section screenshot; use the three shared images.", alone("""
A sheet of six separate spot illustrations in a 3 by 2 grid with wide white gaps, each the same size:

1. Added to cart: the pigeon dropping a small parcel into an open tote bag held by the cat.
2. No search results: Postman P looking through a drawer of an open filing cabinet, the dog holding a torch in its mouth beside him.
3. Page not found: Postman P standing beside his bicycle, studying a large unfolded map held upside down, the pigeon pointing the other way with a wing.
4. Order placed: the whole crew in a row, Postman P raising his cap, the dog mid-jump, the cat on a kraft box, the pigeon overhead.
5. Uploading your photo: the pigeon flying upward carrying a photo print by its top edge.
6. Bulk order: the dog and Postman P carrying a long plank between them with a neat row of four identical kraft boxes on it, the cat riding on the last box.
"""))

ORDER = ["02-promises", "03-what-we-print", "04-how-it-works", "05-occasions", "06-promo", "07-for-brands", "08-questions",
         "09-closer-and-footer", "10-products-page", "11-product-card", "12-product-page", "13-cart", "14-spot-illustrations"]

rows = []
for k in ORDER:
    title, note, prompt = S[k]
    os.makedirs(os.path.join(HERE, k), exist_ok=True)
    open(os.path.join(HERE, k, "PROMPT.txt"), "w", encoding="utf-8", newline="\n").write(prompt)
    rows.append("| `%s` | %s | %s |" % (k, title, note))

README = """# Image prompts for the Ctrl P website

One folder per section. Each folder holds the reference images and a `PROMPT.txt`.

## How to use a folder

1. Open the folder, select all the images, and drag them into the image model. They are numbered in the order the prompt refers to them.
2. Paste the text from `PROMPT.txt`.
3. Once the hero illustration is approved, save it into every folder as `5-hero-approved.png` and drag it in too. The prompts already tell the model to match its dog, cat and pigeon, which keeps the cast the same from section to section.

In folders 02 to 13 the images are:

| File | What it is |
| --- | --- |
| `1-current.png` | The section as it is on the site now. The model edits this. |
| `2-postman-p-walking.png` | Postman P: the style to match. |
| `3-postman-p-cycling.png` | Postman P, second pose, with the bicycle. |
| `4-colours.png` | Character colours and the six brand accents. |

`01-hero` has its own numbering and a `PROMPT.md`. `14-spot-illustrations` has no screenshot, only the three shared images.

## What every prompt contains

- **Space rules.** Text and illustration get separate zones and never overlap; illustrations stay small; gaps are never shrunk to make room. Added after the first promises result came back crowded.
- **Illustration.** What the crew is doing in that section.
- **Subtle component changes.** A short list of touches the model may make to the components themselves (a tilt, a tape strip, a postmark, a tear line, a price tag), all from the brand's world of parcels, tape, stamps, tickets and receipts.
- **Style and colour.** Flat shapes to match Postman P, with an explicit ban on soft gradients and airbrushed fur, which the first result drifted into.
- **What must not change.** Wording, fonts, brand colours, content order.

## Sections

| Folder | Section | Note |
| --- | --- | --- |
| `01-hero` | Hero | Done first. Its result is the cast reference for the rest. |
%s

## Order to work in

Hero first, because it sets the cast. Then 09 (closer), which ends the story the hero starts. Then the weaker sections: 06, 08, 10, 13. Leave the sections the owner already likes (02, 03, 04, 07) for last and judge them hardest: if the result does not clearly improve the section, keep the current version.

## Notes

- The dog, cat and pigeon are a proposal, not brand characters. To change them, edit `CAST` in `make_prompts.py` and run it again.
- Some prompts have a second prompt after a dashed line. The first gives a mock-up of the section; the second gives a clean illustration or photo set to place on the site.
- If a model rewrites the page text, use the second prompt, or ask for the illustration alone on the section's background colour, and place it by hand.
- Tilts and staggered cards are the touches most likely to be toned down when built, especially in the promises section, where the cards stack on scroll.
- The prompts have not all been run through an image model. Only the first version of 02 has, and it came back too crowded, which is what the space rules address.
""" % "\n".join(rows)
open(os.path.join(HERE, "README.md"), "w", encoding="utf-8", newline="\n").write(README)
print("wrote", len(ORDER), "prompts")
