# Image prompts for the Ctrl P website

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
| `02-promises` | Promises: three stamp cards | Liked as it is. Cards become more like real stamps. |
| `03-what-we-print` | What we print: category index | Liked as it is. The illustration replaces the product photo beside the list. |
| `04-how-it-works` | How it works: four ticket stubs | Liked as it is. Stubs become more like real tickets. |
| `05-occasions` | Shop by occasion: four photo links | Photos stay. They become pinned-up prints. |
| `06-promo` | Promotion: Diwali band | Replace the loose sticker cluster. |
| `07-for-brands` | For brands: bulk orders | Liked as it is. The box photo stays. |
| `08-questions` | Questions | The left column under the heading is empty. |
| `09-closer-and-footer` | Closing call to action and footer | Finish the story the hero started. |
| `10-products-page` | Products page: heading | The right side of the heading is empty. |
| `11-product-card` | Product card | Cards are liked. The picture changes; small touches below it. |
| `12-product-page` | Product page | Gallery image and the empty space beside The details. |
| `13-cart` | Cart | The summary becomes a printed receipt; plus an empty state. |
| `14-spot-illustrations` | Small moments: empty states and messages | New pieces. No section screenshot; use the three shared images. |

## Order to work in

Hero first, because it sets the cast. Then 09 (closer), which ends the story the hero starts. Then the weaker sections: 06, 08, 10, 13. Leave the sections the owner already likes (02, 03, 04, 07) for last and judge them hardest: if the result does not clearly improve the section, keep the current version.

## Notes

- The dog, cat and pigeon are a proposal, not brand characters. To change them, edit `CAST` in `make_prompts.py` and run it again.
- Some prompts have a second prompt after a dashed line. The first gives a mock-up of the section; the second gives a clean illustration or photo set to place on the site.
- If a model rewrites the page text, use the second prompt, or ask for the illustration alone on the section's background colour, and place it by hand.
- Tilts and staggered cards are the touches most likely to be toned down when built, especially in the promises section, where the cards stack on scroll.
- The prompts have not all been run through an image model. Only the first version of 02 has, and it came back too crowded, which is what the space rules address.
