# Ctrl P website test

A static site: plain HTML, CSS and a small script. No build step.

## View it locally

Fonts load over HTTP, so open it through a local server rather than double-clicking the file:

```bash
python -m http.server 4173
```

Then visit http://localhost:4173 for the landing page. The products page, product pages and cart are linked from it; the design system is at http://localhost:4173/system.html.

## Put it on Netlify

Drag this whole folder onto https://app.netlify.com/drop, or connect it as a site with no build command and this folder as the publish directory.

## What is where

- `index.html`: landing page
- `products.html`: all products, with search, filters and sorting
- `product-*.html`: one page per product
- `cart.html`: cart
- `system.html`: design system page
- `css/tokens.css`: colours, type scale, spacing, grid
- `css/styles.css`: shared components and the landing page
- `css/products.css`: product cards and the products page
- `css/shop.css`: search and filters, product page, cart
- `css/system.css`: styles used only by the design system page
- `js/main.js`: Products menu, filters, product options, cart, scroll effects, grid overlay (press G)
- `assets/`: fonts, logo, icon set, stickers, photos, product cut-outs
- `DESIGN.md`: the design decisions and open questions
