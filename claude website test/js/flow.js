/* Ctrl P: the pages after the product page.
   Add your photo, checkout, order placed, tracking, saved, and the two demo forms.
   Everything is kept in this browser; nothing is sent anywhere. */
(() => {
  const api = window.CtrlP;
  if (!api) return;
  const { $, $$, rupees, discountFor, read, write } = api;

  const plain = (amount) => rupees(amount).replace('class="price"', 'class="price price--plain"');
  const escapeHtml = (text) => String(text).replace(/[&<>"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[char]));

  const totals = (lines) =>
    lines.reduce(
      (sum, line) => {
        const full = line.unit * line.qty;
        const off = full * discountFor(line.qty);
        return { pieces: sum.pieces + line.qty, subtotal: sum.subtotal + full, saving: sum.saving + off, total: sum.total + full - off };
      },
      { pieces: 0, subtotal: 0, saving: 0, total: 0 }
    );

  const itemRows = (lines) =>
    lines
      .map(
        (line) =>
          '<li><img src="' + escapeHtml(line.art || line.img) + '" alt=""><p><b>' + escapeHtml(line.name) + "</b><span>" +
          line.qty + " × " + escapeHtml(line.opts) + "</span></p>" + rupees(line.unit * line.qty * (1 - discountFor(line.qty))) + "</li>"
      )
      .join("");

  // Marks the empty or malformed boxes and says whether the form can go
  const valid = (form) => {
    let ok = true;
    $$("input, select, textarea", form).forEach((field) => {
      const label = field.closest(".input");
      if (!label) return;
      const bad = !field.checkValidity();
      label.classList.toggle("is-bad", bad);
      if (bad && ok) field.focus();
      if (bad) ok = false;
    });
    return ok;
  };

  /* ---------- Start creating: pick a product if there is none, then design, photos, layout and text, preview ---------- */
  const create = $("[data-create]");
  if (create) {
    const picker = $("[data-create-pick]");
    const DESIGNS = { plain: "Plain", white: "Instant", black: "Night" };

    // A drawn stand-in, so the flow can be tried without a photo
    const sample =
      "data:image/svg+xml," +
      encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800"><rect width="600" height="800" fill="#2ad2c9"/><circle cx="470" cy="150" r="70" fill="#ffc72c"/>' +
          '<circle cx="150" cy="470" r="90" fill="#b17d50"/><path d="M20 800v-90a130 130 0 0 1 260 0v90z" fill="#f9423a"/>' +
          '<circle cx="450" cy="490" r="80" fill="#e4b2a1"/><path d="M330 800v-80a120 120 0 0 1 240 0v80z" fill="#7d55c7"/>' +
          '<circle cx="300" cy="400" r="120" fill="#7a4a2b"/><path d="M250 420q50 40 100 0" fill="none" stroke="#000" stroke-width="12" stroke-linecap="round"/>' +
          '<path d="M120 800V690a180 180 0 0 1 360 0v110z" fill="#ffc72c"/></svg>'
      );

    const showPicker = (draft) => {
      create.hidden = true;
      picker.hidden = false;
      if (draft) {
        $("[data-create-resume]").hidden = false;
        $("[data-resume-name]").textContent = draft.name.toLowerCase();
      }
    };

    const start = (draft) => {
      picker.hidden = true;
      create.hidden = false;
      const board = $("[data-artboard]");
      const art = $("[data-art]");
      const img = $("[data-art-img]");
      const captionOn = $("[data-art-caption]");
      const captionInput = $("[data-caption]");
      const next = $("[data-next]");
      const prev = $("[data-prev]");
      const steps = $$("[data-steps] li");
      const panels = $$("[data-step-panel]");
      const shots = $("[data-shots]");
      const addTile = $("[data-shots-add]");
      const max = draft.max || 1;
      const state = { design: draft.design || "plain", caption: draft.caption || "", photos: [], current: 0, fit: "cover", zoom: 1, turn: 0, x: 50, y: 50, step: 1 };

      board.dataset.shape = draft.shape;
      board.style.setProperty("--ratio", draft.ratio);
      board.style.setProperty("--c", "var(--" + draft.colour + ")");
      $("[data-create-name]").textContent = draft.name.toLowerCase() + ".";
      $("[data-create-area]").textContent = draft.area;
      $("[data-create-opts]").textContent = draft.opts;
      $("[data-create-backname]").textContent = "Back to " + draft.name;
      $("[data-create-back]").href = draft.url;
      $("[data-create-change]").href = draft.url;
      $("[data-photo-word]").textContent = max > 1 ? "photos" : "photo";
      if (max > 1) $("[data-photo-hint]").textContent = "Up to " + max + " photos or pieces of art. Tap one to see it on the preview.";
      captionInput.value = state.caption;

      const remember = () => write("ctrlp-draft", { ...draft, design: state.design, caption: state.caption });

      const paint = () => {
        const photo = state.photos[state.current];
        const framed = state.design !== "plain";
        board.classList.toggle("has-art", Boolean(photo));
        board.classList.toggle("is-turned", state.turn % 180 !== 0);
        board.dataset.frame = state.design;
        board.style.setProperty("--fit", state.fit);
        board.style.setProperty("--zoom", state.zoom);
        board.style.setProperty("--turn", state.turn + "deg");
        board.style.setProperty("--x", state.x + "%");
        board.style.setProperty("--y", state.y + "%");
        img.hidden = !photo;
        if (photo && img.getAttribute("src") !== photo.src) img.src = photo.src;
        $("[data-art-empty]").hidden = Boolean(photo);
        captionOn.hidden = !framed;
        captionOn.textContent = state.caption;
        $("[data-caption-field]").hidden = !framed;
        $("[data-caption-count]").textContent = state.caption.length + "/22";
        $$("[data-design]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.design === state.design)));
        $$("input[name=border]").forEach((input) => (input.checked = input.value === state.design));
      };

      const paintShots = () => {
        $$(".shots__item", shots).forEach((item) => item.remove());
        state.photos.forEach((photo, i) => {
          const item = document.createElement("div");
          item.className = "shots__item" + (i === state.current ? " is-current" : "");
          item.innerHTML =
            '<button type="button" aria-label="Show photo ' + (i + 1) + ' on the preview"><img src="' + photo.src + '" alt=""></button>' +
            '<button class="shots__remove" type="button" aria-label="Remove photo ' + (i + 1) + '"><svg class="icon" aria-hidden="true"><use href="assets/img/icons.svg#i-close"/></svg></button>';
          item.firstChild.addEventListener("click", () => {
            state.current = i;
            paintShots();
            paint();
          });
          item.lastChild.addEventListener("click", () => {
            state.photos.splice(i, 1);
            state.current = Math.max(0, Math.min(state.current, state.photos.length - 1));
            paintShots();
            paint();
            go(state.step);
          });
          shots.insertBefore(item, addTile);
        });
        addTile.hidden = state.photos.length >= max;
        $("[data-add-label]").textContent = state.photos.length ? "Add more" : "Add a photo";
        $("[data-photo-count]").textContent = state.photos.length + " of " + max + " added.";
        $("[data-sample]").hidden = state.photos.length >= max;
      };

      const labels = ["Next: photos", "Next: layout and text", "Next: preview", "Add to cart"];
      const go = (step) => {
        const ready = state.photos.length > 0;
        if (step > 2 && !ready) step = 2;
        state.step = step;
        steps.forEach((item, i) => {
          item.classList.toggle("is-active", i + 1 === step);
          item.classList.toggle("is-done", i + 1 < step);
          $("button", item).disabled = !ready && i > 1;
        });
        panels.forEach((panel) => (panel.hidden = Number(panel.dataset.stepPanel) !== step));
        prev.hidden = step === 1;
        next.disabled = step >= 2 && !ready;
        $("[data-next-label]").textContent = labels[step - 1];
        if (step === 4) {
          const off = discountFor(draft.qty);
          $("[data-check-name]").textContent = draft.name + (state.design !== "plain" ? ", " + DESIGNS[state.design] + " design" : "") + (state.caption && state.design !== "plain" ? ": “" + state.caption + "”" : "");
          $("[data-check-opts]").textContent = draft.opts;
          $("[data-check-qty]").textContent = draft.qty + (off ? ", " + Math.round(off * 100) + "% off each" : "");
          $("[data-check-each]").innerHTML = plain(draft.unit * (1 - off));
          $("[data-check-total]").innerHTML = rupees(draft.unit * draft.qty * (1 - off));
        }
      };

      const addPhoto = (src, name) => {
        if (state.photos.length >= max) return;
        state.photos.push({ src, name });
        state.current = state.photos.length - 1;
        Object.assign(state, { fit: "cover", zoom: 1, turn: 0, x: 50, y: 50 });
        $("[data-zoom]").value = 1;
        $("input[name=fit][value=cover]").checked = true;
        paintShots();
        paint();
        go(state.step);
      };

      $$("[data-design]").forEach((button) =>
        button.addEventListener("click", () => {
          state.design = button.dataset.design;
          remember();
          paint();
        })
      );
      $$("input[name=border]").forEach((input) =>
        input.addEventListener("change", () => {
          state.design = input.value;
          remember();
          paint();
        })
      );
      captionInput.addEventListener("input", () => {
        state.caption = captionInput.value.slice(0, 22);
        remember();
        paint();
      });

      $("[data-file]").addEventListener("change", (event) => {
        [...event.target.files].slice(0, max - state.photos.length).forEach((file) => {
          const reader = new FileReader();
          reader.addEventListener("load", () => addPhoto(reader.result, file.name));
          reader.readAsDataURL(file);
        });
        event.target.value = "";
      });
      $("[data-sample]").addEventListener("click", () => addPhoto(sample, "Sample photo"));

      $$("input[name=fit]").forEach((input) =>
        input.addEventListener("change", () => {
          state.fit = input.value;
          paint();
        })
      );
      $("[data-zoom]").addEventListener("input", (event) => {
        state.zoom = Number(event.target.value);
        paint();
      });
      $("[data-rotate]").addEventListener("click", () => {
        state.turn = (state.turn + 90) % 360;
        paint();
      });
      $("[data-reset]").addEventListener("click", () => {
        Object.assign(state, { fit: "cover", zoom: 1, turn: 0, x: 50, y: 50 });
        $("[data-zoom]").value = 1;
        $("input[name=fit][value=cover]").checked = true;
        paint();
      });

      // Drag the photo around inside the print
      let grab = null;
      art.addEventListener("pointerdown", (event) => {
        if (!state.photos.length) return;
        grab = { x: event.clientX, y: event.clientY, startX: state.x, startY: state.y };
        art.setPointerCapture(event.pointerId);
      });
      art.addEventListener("pointermove", (event) => {
        if (!grab) return;
        const box = art.getBoundingClientRect();
        state.x = Math.max(0, Math.min(100, grab.startX - ((event.clientX - grab.x) / box.width) * 100));
        state.y = Math.max(0, Math.min(100, grab.startY - ((event.clientY - grab.y) / box.height) * 100));
        paint();
      });
      ["pointerup", "pointercancel"].forEach((type) => art.addEventListener(type, () => (grab = null)));

      // A small square of the artwork, so the cart can show what was made
      const thumbnail = () => {
        try {
          const size = 200;
          const canvas = document.createElement("canvas");
          canvas.width = canvas.height = size;
          const context = canvas.getContext("2d");
          const scale = Math.max(size / img.naturalWidth, size / img.naturalHeight);
          const width = img.naturalWidth * scale;
          const height = img.naturalHeight * scale;
          context.fillStyle = "#fff";
          context.fillRect(0, 0, size, size);
          context.translate(size / 2, size / 2);
          context.rotate((state.turn * Math.PI) / 180);
          context.drawImage(img, -width / 2, -height / 2, width, height);
          return canvas.toDataURL("image/jpeg", 0.82);
        } catch (error) {
          return "";
        }
      };

      // Sharing the picture itself needs a server; for now this passes on the product link
      $("[data-share]").addEventListener("click", async () => {
        const link = new URL(draft.url, window.location.href).href;
        const note = $("[data-share-note]");
        try {
          if (navigator.share) await navigator.share({ title: "Ctrl P: " + draft.name, url: link });
          else {
            await navigator.clipboard.writeText(link);
            note.textContent = "Link copied. Paste it wherever you like.";
          }
        } catch (error) {
          note.textContent = "That didn’t go through. Copy the address of the product page to share it.";
        }
      });

      $$("[data-goto]").forEach((button) => button.addEventListener("click", () => go(Number(button.dataset.goto))));
      prev.addEventListener("click", () => go(state.step - 1));
      next.addEventListener("click", () => {
        if (state.step < 4) return go(state.step + 1);
        state.current = 0;
        paint();
        const { replaces, key, max: unused, ...item } = draft;
        const framed = state.design !== "plain";
        if (replaces) api.setCart(api.cart().filter((line) => line.key !== replaces));
        api.addToCart({
          ...item,
          opts: draft.opts + (framed ? ", " + DESIGNS[state.design] + " design" : ""),
          design: state.design,
          caption: framed ? state.caption : "",
          art: thumbnail(),
          stamp: Date.now(),
        });
        localStorage.removeItem("ctrlp-draft");
        window.location.href = "cart.html";
      });

      paintShots();
      paint();
      go(1);
    };

    // Choosing a product here starts the flow with that product's first options and a quantity of one
    $$("[data-pick]").forEach((button) =>
      button.addEventListener("click", () => {
        const data = button.dataset;
        const draft = {
          id: data.id, name: data.name, img: data.img, url: data.url, opts: data.opts, unit: Number(data.price), qty: 1,
          cat: data.cat, shape: data.shape, ratio: data.ratio, area: data.area, colour: data.colour, piece: data.unit, max: Number(data.max) || 1,
        };
        write("ctrlp-draft", draft);
        history.replaceState(null, "", "create.html");
        window.scrollTo(0, 0);
        start(draft);
      })
    );

    const draft = read("ctrlp-draft");
    if (!draft || window.location.hash === "#pick") showPicker(draft);
    else start(draft);
  }

  /* ---------- Checkout ---------- */
  const fillSums = (sum) => {
    $("[data-sum-subtotal]").innerHTML = plain(sum.subtotal);
    $("[data-sum-saving-row]").hidden = sum.saving === 0;
    $("[data-sum-saving]").innerHTML = "&minus; " + plain(sum.saving);
    $("[data-sum-total]").innerHTML = rupees(sum.total);
  };

  const checkout = $("[data-checkout]");
  if (checkout) {
    const lines = api.cart();
    checkout.hidden = lines.length === 0;
    $("[data-checkout-empty]").hidden = lines.length > 0;
    if (lines.length) {
      const sum = totals(lines);
      $("[data-checkout-items]").innerHTML = itemRows(lines);
      fillSums(sum);
      const form = $("[data-checkout-form]");
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        const ok = valid(form);
        $("[data-checkout-error]").hidden = ok;
        if (!ok) return;
        const data = new FormData(form);
        const order = {
          no: "CP-" + String(Math.floor(100000 + Math.random() * 900000)),
          date: new Date().toISOString(),
          name: String(data.get("name")).trim().split(" ")[0],
          to: String(data.get("city")).trim() + " " + String(data.get("pin")).trim(),
          pay: data.get("pay"),
          lines,
          total: sum.total,
        };
        write("ctrlp-orders", [...(read("ctrlp-orders") || []), order]);
        write("ctrlp-last-order", order.no);
        api.setCart([]);
        window.location.href = "order.html";
      });
    }
  }

  /* ---------- Order placed ---------- */
  const orders = () => read("ctrlp-orders") || [];
  const placed = $("[data-placed]");
  if (placed) {
    const order = orders().find((other) => other.no === read("ctrlp-last-order"));
    placed.hidden = !order;
    $("[data-order-none]").hidden = Boolean(order);
    if (order) {
      $("[data-order-name]").textContent = order.name || "friend";
      $("[data-order-no]").textContent = order.no;
      $("[data-order-items]").innerHTML = itemRows(order.lines);
      $("[data-order-to]").textContent = order.to;
      $("[data-order-pay]").textContent = order.pay;
      $("[data-order-total]").innerHTML = rupees(order.total);
      $("[data-order-track]").href = "track.html#" + order.no;
    }
  }

  /* ---------- Tracking: looks the number up among orders placed in this browser ---------- */
  const trackForm = $("[data-track-form]");
  if (trackForm) {
    const input = $("[data-track-input]");
    const find = () => {
      const no = input.value.trim().toUpperCase();
      const order = orders().find((other) => other.no === no);
      $("[data-track-result]").hidden = !order;
      $("[data-track-miss]").hidden = Boolean(order) || !no;
      if (!order) return;
      $("[data-track-no]").textContent = order.no;
      $("[data-track-meta]").textContent = order.lines.reduce((sum, line) => sum + line.qty, 0) + " pieces, going to " + order.to;
      $("[data-track-date]").textContent = new Date(order.date).toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
    };
    trackForm.addEventListener("submit", (event) => {
      event.preventDefault();
      find();
    });
    if (window.location.hash.length > 1) {
      input.value = decodeURIComponent(window.location.hash.slice(1));
      find();
    }
  }

  /* ---------- Saved: every card is on the page, only the saved ones show ---------- */
  const savedGrid = $("[data-saved-grid]");
  if (savedGrid) {
    const show = () => {
      const list = api.saved();
      $$(".pcard", savedGrid).forEach((card) => card.classList.toggle("is-unsaved", !list.includes(card.dataset.slug)));
      savedGrid.hidden = list.length === 0;
      $("[data-saved-empty]").hidden = list.length > 0;
    };
    document.addEventListener("ctrlp:saved", show);
    show();
  }

  /* ---------- Quote and contact forms: they check themselves, then show the reply. Nothing is sent. ---------- */
  $$("[data-demo-form]").forEach((form) =>
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const ok = valid(form);
      $("[data-form-error]", form).hidden = ok;
      if (ok) $("[data-form-sent]", form).hidden = false;
    })
  );
})();
