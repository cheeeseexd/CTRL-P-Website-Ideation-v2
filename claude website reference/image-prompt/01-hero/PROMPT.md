# Hero illustration prompt

Drag all five images in this folder into the image model, in order, then paste the prompt.

| File | What it is for |
| --- | --- |
| `1-hero-current.png` | The hero as it is now. Layout reference. |
| `2-hero-canvas-empty.png` | The same hero with the packaging and the small cyclist removed. This is the image to edit. |
| `3-postman-p-walking.png` | Postman P. The style and the character to match. |
| `4-postman-p-cycling.png` | Postman P again, second pose. Shows how props and printed sheets are drawn. |
| `5-colours.png` | Character colours and the six brand accents. |

## Prompt: full hero mock-up

```text
Edit image 2 (the empty website hero). Keep everything in it exactly as it is: the navbar, the logo, the headline "OFF YOUR PHONE. INTO THEIR HANDS." with the coral tape over "HANDS.", the paragraph, the black "Start creating" button, the note under it, the pale graph-paper background and the coral tape strip along the bottom edge. Do not redraw, move, restyle or re-letter any of it, except for the three small component changes listed further down. Image 1 shows the old version of this hero for layout only; the photographic boxes, mailer and sticker pack in it must not appear.

Add one illustration in the empty area on the right, below the headline. It sits in the right half of the frame, its feet standing directly on the top edge of the coral tape strip as if the tape were the road. It must not overlap the headline, the paragraph or the button, and the left half of the tape stays empty.

The illustration: Postman P (the character in images 3 and 4) leading a small delivery parade, walking left to right in a single file.

1. Postman P at the front, in the same striding pose as image 3, but instead of the logo sign he carries a huge printed photograph under his arm, tilted the same way. The print is a white-bordered photo, taller than he is wide, showing two friends laughing together, drawn in flat shapes in turquoise, sunglow yellow and rose. A short strip of coral tape is stuck on one corner. This print is the centre of the picture and the brightest thing in it.
2. Behind him, an Indian street dog (lean, tan, pointed ears, curled tail) trotting proudly with a rolled poster in its mouth, the roll held by a royal blue band.
3. Behind the dog, a cat sitting inside a small open kraft shipping box on four little wheels, pulled along by a string tied to the dog's tail, looking pleased with itself. The box has a strip of coral tape across it.
4. Above Postman P's cap, a pigeon flying ahead with a small fuchsia envelope in its beak.

Nothing else. No extra characters, no scenery, no buildings, no speech bubbles, no floating icons, no sparkles, no confetti.

Space comes first. The parade is small: no taller than a third of the frame, with empty graph paper above it, to its left and to its right. The figures have even gaps between them and do not overlap one another, apart from the string. If it does not fit comfortably, make every figure smaller; never let it touch the headline, the paragraph or the button.

Subtle changes to the components, to make the hero more creative. Use these and nothing more:
- The coral tape strip no longer runs off the right edge. It ends at a roll of coral tape standing on its side at the far right, as if the strip has just been pulled from it.
- At the left edge the strip ends in a zigzag cut.
- The note under the button ("No minimum order. Ships across India.") sits on a small white paper label held by one short strip of sunglow tape, tilted one degree.

Style: identical to images 3 and 4, as if the same illustrator drew the friends on the same day. Flat vector illustration, no outlines, chunky rounded shapes with a few sharp corners, two or three flat tones per shape with hard-edged shading. No soft gradients, no airbrushed fur, no glossy highlights, no texture, no grain, no 3D, no realism. Faces as in the reference: a white oval eye with a small dot pupil, a big rounded pink nose, simple shapes. Big heavy feet, small details like the bow-tied laces. The animals follow the same construction: big simple silhouettes, the same dot eyes, the same hard two-tone shading.

Colour: follow image 5. The characters use only the Postman P colours: kraft tan and brown, charcoal navy, soft pink, lilac grey, white. The six brand accents appear only on printed things: the photo print, the poster band, the envelope, the tape. One flat pale lilac-grey contact shadow under each character, no other shadows.

No new text anywhere. The only lettering the illustration may contain is the small "P" mark on Postman P's cap, as in the reference. The Ctrl P logo is not repeated in the illustration.

Output: 16:10 landscape, same framing as image 2, crisp and high resolution.
```

## Prompt: the illustration alone

Use this one to get an asset that can go on the site. Give it images 3, 4 and 5 only.

```text
A single illustration on a plain white background, in exactly the style of the two reference characters (images 1 and 2), as if the same illustrator drew it.

Postman P (the character in the references) leads a small delivery parade, walking left to right in single file along a flat ground line.

1. Postman P at the front, in the same striding pose as image 1, but instead of the logo sign he carries a huge printed photograph under his arm, tilted the same way. The print is a white-bordered photo showing two friends laughing together, drawn in flat shapes in turquoise, sunglow yellow and rose, with a short strip of coral tape on one corner. It is the brightest thing in the picture.
2. Behind him, an Indian street dog (lean, tan, pointed ears, curled tail) trotting proudly with a rolled poster in its mouth, the roll held by a royal blue band.
3. Behind the dog, a cat sitting in a small open kraft shipping box on four little wheels, pulled by a string tied to the dog's tail. A strip of coral tape across the box.
4. Above Postman P's cap, a pigeon flying ahead with a small fuchsia envelope in its beak.

Nothing else: no scenery, no extra characters, no speech bubbles, no sparkles, no text except the small "P" mark on the cap.

Keep it open: even gaps between the figures, none overlapping another apart from the string, and clear white space all round.

Style: flat vector illustration, no outlines, chunky rounded shapes with a few sharp corners, two or three flat tones per shape with hard-edged shading. No soft gradients, no airbrushed fur, no glossy highlights, no texture, no 3D. White oval eyes with a dot pupil, big rounded pink nose, big heavy feet. The animals are built the same way as the postman.

Colour: follow image 3. Characters in kraft tan and brown, charcoal navy, soft pink, lilac grey and white only. The brand accents (coral, sunglow, turquoise, royal blue, fuchsia, rose) only on the printed things. One flat pale lilac-grey contact shadow under each character.

Wide landscape composition, about 2:1, everything fully inside the frame with clear white space around it, feet all on the same ground line. High resolution.
```

## Notes

- Postman P appears once. The small cyclist on the tape is left out of the mock-up because he is now in the illustration. To keep him instead, edit `1-hero-current.png` and change the parade leader to another friend.
- If the model changes the headline or the button, generate with the second prompt and place the result over `2-hero-canvas-empty.png` by hand.
- The friends are a proposal, not brand characters. Swap them in the numbered list if the brand has others in mind.
