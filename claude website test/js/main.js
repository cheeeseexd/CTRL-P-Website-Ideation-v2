(() => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  const rupees = (amount) =>
    '<span class="price"><svg aria-hidden="true"><use href="assets/img/icons.svg#i-rupee"/></svg><span class="visually-hidden">Rs </span>' +
    Math.round(amount).toLocaleString("en-IN") +
    "</span>";

  // Placeholder bulk tiers: 10 or more pieces 10% off each, 50 or more 20% off each
  const discountFor = (qty) => (qty >= 50 ? 0.2 : qty >= 10 ? 0.1 : 0);

  /* ---------- Reveal on scroll ---------- */
  const revealables = $$("[data-reveal]");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -6% 0px", threshold: 0.08 }
    );
    revealables.forEach((el) => observer.observe(el));
  } else {
    revealables.forEach((el) => el.classList.add("is-in"));
  }

  /* ---------- Hero: Postman P cycles along the tape as the page scrolls ---------- */
  const rider = $("[data-rider]");
  if (rider && !reduceMotion) {
    let ticking = false;
    const ride = () => {
      const progress = Math.min(window.scrollY / (window.innerHeight * 0.9), 1);
      rider.style.setProperty("--ride", (progress * 82).toFixed(2));
      ticking = false;
    };
    window.addEventListener(
      "scroll",
      () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(ride);
      },
      { passive: true }
    );
  }

  // The tape's lettering slides the other way as the page scrolls. It repeats every two words, so it never runs out.
  const tapes = $$("[data-tape]");
  if (tapes.length && !reduceMotion) {
    let ticking = false;
    const measure = (run) => run.children[2].offsetLeft - run.children[0].offsetLeft;
    const pull = () => {
      tapes.forEach((run) => {
        const unit = measure(run);
        if (unit > 0) run.style.setProperty("--pull", -((window.scrollY * 0.35) % unit).toFixed(1) + "px");
      });
      ticking = false;
    };
    window.addEventListener(
      "scroll",
      () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(pull);
      },
      { passive: true }
    );
  }

  /* ---------- Nav ---------- */
  const nav = $("[data-nav]");
  const toggle = $("[data-nav-toggle]");
  const menu = document.getElementById("menu");
  if (nav) {
    const setStuck = () => nav.classList.toggle("is-stuck", window.scrollY > 8);
    window.addEventListener("scroll", setStuck, { passive: true });
    setStuck();
  }
  const setMenu = (open) => {
    if (!toggle || !menu) return;
    menu.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Menu");
  };
  if (toggle && menu) {
    toggle.addEventListener("click", () => setMenu(!menu.classList.contains("is-open")));
    menu.addEventListener("click", (event) => {
      if (event.target.closest("a")) setMenu(false);
    });
  }

  // Products menu. Only the Products link itself can open it, and only with a real mouse resting on it:
  // the closed panel takes no pointer events, scrolling closes it, and touch never opens it.
  const mega = $("[data-mega]");
  const megaLink = $("[data-mega-link]");
  const wide = window.matchMedia("(min-width: 64rem)");
  let openTimer;
  let closeTimer;
  const closeMega = () => {
    if (!mega) return;
    window.clearTimeout(openTimer);
    mega.classList.remove("is-open");
  };
  if (mega && megaLink) {
    const cats = $$(".mega__cat[data-panel]", mega);
    const panels = $$(".mega__panel", mega);
    const show = (id) => {
      cats.forEach((cat) => cat.classList.toggle("is-active", cat.dataset.panel === id));
      panels.forEach((panel) => panel.classList.toggle("is-active", panel.dataset.panel === id));
    };
    const openMega = () => {
      window.clearTimeout(closeTimer);
      mega.classList.add("is-open");
    };
    cats.forEach((cat) => {
      cat.addEventListener("pointerenter", () => show(cat.dataset.panel));
      cat.addEventListener("focus", () => show(cat.dataset.panel));
    });

    megaLink.addEventListener("pointerenter", (event) => {
      if (event.pointerType !== "mouse" || !wide.matches) return;
      window.clearTimeout(closeTimer);
      openTimer = window.setTimeout(() => {
        if (megaLink.matches(":hover")) openMega();
      }, 140);
    });
    megaLink.addEventListener("pointerleave", () => window.clearTimeout(openTimer));
    mega.addEventListener("pointerenter", () => window.clearTimeout(closeTimer));
    mega.addEventListener("pointerleave", () => {
      window.clearTimeout(openTimer);
      closeTimer = window.setTimeout(closeMega, 160);
    });
    megaLink.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowDown" || !wide.matches) return;
      event.preventDefault();
      openMega();
      cats[0].focus();
    });
    mega.addEventListener("focusout", (event) => {
      if (!mega.contains(event.relatedTarget)) closeMega();
    });
    mega.addEventListener("click", (event) => {
      if (event.target.closest(".mega a")) closeMega();
    });
    window.addEventListener("scroll", closeMega, { passive: true });
    window.addEventListener("blur", closeMega);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    setMenu(false);
    if (mega && mega.classList.contains("is-open")) {
      closeMega();
      megaLink.focus();
    }
  });

  /* ---------- Category index: a row tapes over and the product beside the list changes ---------- */
  const index = $("[data-index]");
  if (index) {
    const rows = $$(".index__row", index);
    const shots = $$(".index__shot");
    const showRow = (row) => {
      rows.forEach((other) => other.classList.toggle("is-active", other === row));
      shots.forEach((shot) => shot.classList.toggle("is-active", shot.dataset.show === row.dataset.show));
    };
    rows.forEach((row) => {
      row.addEventListener("pointerenter", () => showRow(row));
      row.addEventListener("focus", () => showRow(row));
    });
  }

  /* ---------- Cart, kept in this browser ---------- */
  const CART_KEY = "ctrlp-cart";
  const readCart = () => {
    try {
      return JSON.parse(localStorage.getItem(CART_KEY)) || [];
    } catch (error) {
      return [];
    }
  };
  let cart = readCart();
  const cartCount = $("[data-cart-count]");
  const saveCart = () => {
    try {
      localStorage.setItem(CART_KEY, JSON.stringify(cart));
    } catch (error) {
      /* private mode: the cart lasts for this page only */
    }
    const pieces = cart.reduce((sum, item) => sum + item.qty, 0);
    if (cartCount) {
      cartCount.textContent = pieces;
      cartCount.hidden = pieces === 0;
      cartCount.parentElement.setAttribute("aria-label", "Cart, " + pieces + (pieces === 1 ? " item" : " items"));
    }
  };
  // Two lines with the same product and options stay separate when the artwork differs
  const addToCart = (item) => {
    const key = item.id + "|" + item.opts + "|" + (item.stamp || "");
    const existing = cart.find((line) => line.key === key);
    if (existing) existing.qty = Math.min(999, existing.qty + item.qty);
    else cart.push({ ...item, key });
    saveCart();
  };
  saveCart();

  const read = (key) => {
    try {
      return JSON.parse(localStorage.getItem(key));
    } catch (error) {
      return null;
    }
  };
  const write = (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      /* private mode: nothing is kept between pages */
    }
  };

  const itemFrom = (el, opts, unit, qty) => ({
    id: el.dataset.id,
    name: el.dataset.name,
    img: el.dataset.img,
    url: el.dataset.url,
    opts,
    unit,
    qty,
  });

  const toast = $("[data-toast]");
  let toastTimer;
  const showToast = (text) => {
    if (!toast) return;
    $("[data-toast-text]", toast).textContent = text;
    toast.hidden = false;
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => {
      toast.hidden = true;
    }, 4000);
  };

  /* ---------- Saved products, kept in this browser ---------- */
  const SAVED_KEY = "ctrlp-saved";
  let saved = read(SAVED_KEY) || [];
  const savedCount = $("[data-saved-count]");
  const paintSaved = () => {
    $$("[data-wish]").forEach((button) => button.setAttribute("aria-pressed", String(saved.includes(button.dataset.wish))));
    if (savedCount) {
      savedCount.textContent = saved.length;
      savedCount.hidden = saved.length === 0;
    }
    document.dispatchEvent(new CustomEvent("ctrlp:saved", { detail: saved }));
  };
  $$("[data-wish]").forEach((button) => {
    button.addEventListener("click", () => {
      const slug = button.dataset.wish;
      const adding = !saved.includes(slug);
      saved = adding ? [...saved, slug] : saved.filter((other) => other !== slug);
      write(SAVED_KEY, saved);
      paintSaved();
      if (adding && !$("[data-saved]")) showToast("Saved for later.");
    });
  });

  // Shared with js/flow.js, which runs the pages after the product page
  window.CtrlP = {
    $,
    $$,
    rupees,
    discountFor,
    read,
    write,
    addToCart,
    cart: () => cart,
    saved: () => saved,
    setCart: (next) => {
      cart = next;
      saveCart();
    },
  };
  paintSaved();

  /* ---------- Products page: search, filters, sorting ---------- */
  const grid = $("[data-products]");
  if (grid) {
    const cards = $$("[data-cat]", grid);
    const promo = $("[data-promo]", grid);
    const chips = $$("[data-filter]");
    const flagToggles = $$("[data-flag]");
    const searchInput = $("[data-search-input]");
    const sortSelect = $("[data-sort]");
    const count = $("[data-count]");
    const countLabel = $("[data-count-label]");
    const empty = $("[data-empty]");
    const clearButtons = $$("[data-clear]");
    const state = { cat: "all", flags: new Set(), query: "", sort: "featured" };

    const sorters = {
      featured: (a, b) => a.dataset.order - b.dataset.order,
      low: (a, b) => a.dataset.price - b.dataset.price,
      high: (a, b) => b.dataset.price - a.dataset.price,
      new: (a, b) => b.dataset.flags.includes("new") - a.dataset.flags.includes("new") || b.dataset.order - a.dataset.order,
      name: (a, b) => a.dataset.name.localeCompare(b.dataset.name),
    };

    const apply = () => {
      const words = state.query.toLowerCase().split(/\s+/).filter(Boolean);
      let shown = 0;
      cards.forEach((card) => {
        const flags = card.dataset.flags.split(" ");
        const match =
          (state.cat === "all" || card.dataset.cat === state.cat) &&
          [...state.flags].every((flag) => flags.includes(flag)) &&
          words.every((word) => card.dataset.search.includes(word));
        card.hidden = !match;
        if (match) {
          shown += 1;
          card.classList.add("is-in");
        }
      });
      [...cards].sort(sorters[state.sort]).forEach((card) => grid.append(card));

      const untouched = state.cat === "all" && state.flags.size === 0 && !words.length && state.sort === "featured";
      if (promo) {
        promo.hidden = !untouched;
        if (untouched) grid.insertBefore(promo, grid.children[5] || null);
      }
      chips.forEach((chip) => chip.setAttribute("aria-pressed", String(chip.dataset.filter === state.cat)));
      flagToggles.forEach((button) => button.setAttribute("aria-pressed", String(state.flags.has(button.dataset.flag))));
      count.textContent = shown;
      countLabel.textContent = shown === 1 ? "product" : "products";
      empty.hidden = shown > 0;
      grid.hidden = shown === 0;
      clearButtons.forEach((button) => {
        if (!button.closest("[data-empty]")) button.hidden = state.cat === "all" && state.flags.size === 0 && !words.length;
      });
    };

    const fromHash = () => {
      const id = window.location.hash.slice(1);
      if (id === "search" && searchInput) {
        searchInput.focus();
        return;
      }
      state.cat = chips.some((chip) => chip.dataset.filter === id) ? id : "all";
      apply();
    };

    chips.forEach((chip) =>
      chip.addEventListener("click", () => {
        state.cat = chip.dataset.filter;
        history.replaceState(null, "", state.cat === "all" ? window.location.pathname : "#" + state.cat);
        apply();
      })
    );
    flagToggles.forEach((button) =>
      button.addEventListener("click", () => {
        const flag = button.dataset.flag;
        if (state.flags.has(flag)) state.flags.delete(flag);
        else state.flags.add(flag);
        apply();
      })
    );
    if (searchInput) {
      searchInput.addEventListener("input", () => {
        state.query = searchInput.value;
        apply();
      });
    }
    if (sortSelect) {
      sortSelect.addEventListener("change", () => {
        state.sort = sortSelect.value;
        apply();
      });
    }
    clearButtons.forEach((button) =>
      button.addEventListener("click", () => {
        state.cat = "all";
        state.flags.clear();
        state.query = "";
        if (searchInput) searchInput.value = "";
        history.replaceState(null, "", window.location.pathname);
        apply();
      })
    );
    window.addEventListener("hashchange", fromHash);
    if (window.location.hash) fromHash();
  }

  /* ---------- Product page: options, quantity, running total ---------- */
  const form = $("[data-product]");
  if (form) {
    const base = Number(form.dataset.price);
    const qtyInput = $("[data-qty]", form);
    const total = $("[data-total]");
    const saving = $("[data-saving]");
    const picked = () => $$("input[type=radio][data-mult]:checked", form);
    const counts = $$("input[name=qty]", form);
    const custom = $("[data-qty-custom]", form);
    const barTotal = $("[data-bar-total]");
    const barEach = $("[data-bar-each]");
    const quantity = () => Math.max(1, Math.min(999, Math.round(Number(qtyInput.value) || 1)));
    const unitPrice = () => Math.round(picked().reduce((value, input) => value * Number(input.dataset.mult), base));

    const each = $("[data-each]");
    const update = () => {
      const qty = quantity();
      const unit = unitPrice();
      const discount = discountFor(qty);
      const now = unit * (1 - discount);
      total.innerHTML = rupees(now * qty);
      each.innerHTML = qty === 1 ? "for 1 " + form.dataset.unit : "for " + qty + ", " + rupees(now) + " each";
      barTotal.innerHTML = total.innerHTML;
      barEach.innerHTML = each.innerHTML;
      saving.hidden = !discount;
      saving.innerHTML = discount ? "You save " + rupees(unit * qty * discount).replace('class="price"', 'class="price price--plain"') : "";
    };

    // "How many" is a short row of common numbers; the last one opens a box for any other number
    const syncCount = () => {
      const chosen = counts.find((input) => input.checked);
      custom.hidden = chosen.value !== "other";
      if (chosen.value !== "other") qtyInput.value = chosen.value;
    };
    form.addEventListener("change", () => {
      syncCount();
      update();
    });
    qtyInput.addEventListener("input", update);
    qtyInput.addEventListener("blur", () => {
      qtyInput.value = quantity();
    });
    $$("[data-step]", form).forEach((button) =>
      button.addEventListener("click", () => {
        qtyInput.value = Math.max(1, Math.min(999, quantity() + Number(button.dataset.step)));
        update();
      })
    );

    // The bar at the foot of the screen appears only while the price and the button are both out of sight
    const bar = $("[data-buybar]");
    if (bar && "IntersectionObserver" in window) {
      const seen = new Map();
      const watcher = new IntersectionObserver((entries) => {
        entries.forEach((entry) => seen.set(entry.target, entry.isIntersecting));
        const section = seen.get(form.closest(".pdp"));
        bar.hidden = !section || seen.get($("[data-price-block]")) || seen.get($("[data-buy]", form));
      });
      [form.closest(".pdp"), $("[data-price-block]"), $("[data-buy]", form)].forEach((el) => watcher.observe(el));
    }

    // Coming back from the photo step to change something: put the earlier choices back
    const earlier = read("ctrlp-draft");
    if (earlier && earlier.id === form.dataset.id) {
      earlier.opts.split(", ").forEach((value) => {
        const input = $$("input[type=radio]", form).find((radio) => radio.value === value);
        if (input) input.checked = true;
      });
      qtyInput.value = earlier.qty;
      (counts.find((input) => input.value === String(earlier.qty)) || counts[counts.length - 1]).checked = true;
      syncCount();
      qtyInput.value = earlier.qty;
    }

    // The product page only chooses. The photo is added on the next page, and the cart comes after that.
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      write("ctrlp-draft", {
        ...itemFrom(form, picked().map((input) => input.value).join(", "), unitPrice(), quantity()),
        cat: form.dataset.cat,
        shape: form.dataset.shape,
        ratio: form.dataset.ratio,
        area: form.dataset.area,
        colour: form.dataset.colour,
        piece: form.dataset.unit,
        max: Number(form.dataset.max) || 1,
      });
      window.location.href = "create.html";
    });

    const main = $("[data-main]");
    $$("[data-thumb]").forEach((thumb) =>
      thumb.addEventListener("click", () => {
        main.src = thumb.dataset.thumb;
        $$("[data-thumb]").forEach((other) => other.classList.toggle("is-active", other === thumb));
      })
    );
    update();
  }

  /* ---------- Cart page ---------- */
  const cartView = $("[data-cart]");
  if (cartView) {
    const list = $("[data-cart-items]");
    const emptyView = $("[data-cart-empty]");
    const escapeHtml = (text) => String(text).replace(/[&<>"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[char]));

    const render = () => {
      cartView.hidden = cart.length === 0;
      emptyView.hidden = cart.length > 0;
      let subtotal = 0;
      let savingTotal = 0;
      list.innerHTML = cart
        .map((line, i) => {
          const discount = discountFor(line.qty);
          const full = line.unit * line.qty;
          const lineTotal = full * (1 - discount);
          subtotal += full;
          savingTotal += full - lineTotal;
          return (
            '<li class="line" data-line="' + i + '" style="--c:var(--' + escapeHtml(line.colour || "coral") + ')">' +
            '<a class="line__img" href="' + escapeHtml(line.url) + '"><img src="' + escapeHtml(line.art || line.img) + '" alt=""></a>' +
            '<div class="line__info"><a class="line__name" href="' + escapeHtml(line.url) + '">' + escapeHtml(line.name) + "</a>" +
            '<p class="line__opts">' + escapeHtml(line.opts) + "</p>" +
            '<p class="line__unit">' + rupees(line.unit) + " each" + (discount ? ' <span class="flag" style="--c:var(--turquoise)">' + Math.round(discount * 100) + "% bulk saving</span>" : "") + "</p>" +
            '<p class="line__actions"><a href="create.html" data-edit>Change photo</a><button type="button" data-remove>Remove</button></p></div>' +
            '<div class="stepper"><button type="button" data-step="-1" aria-label="One fewer"><svg class="icon" aria-hidden="true"><use href="assets/img/icons.svg#i-minus"/></svg></button>' +
            '<input type="number" inputmode="numeric" min="1" max="999" value="' + line.qty + '" aria-label="Quantity of ' + escapeHtml(line.name) + '" data-qty>' +
            '<button type="button" data-step="1" aria-label="One more"><svg class="icon" aria-hidden="true"><use href="assets/img/icons.svg#i-plus"/></svg></button></div>' +
            '<p class="line__total">' + rupees(lineTotal) + "</p></li>"
          );
        })
        .join("");
      $("[data-sum-count]").textContent = cart.reduce((sum, line) => sum + line.qty, 0);
      $("[data-sum-subtotal]").innerHTML = rupees(subtotal);
      $("[data-sum-saving-row]").hidden = savingTotal === 0;
      $("[data-sum-saving]").innerHTML = "&minus; " + rupees(savingTotal);
      $("[data-sum-total]").innerHTML = rupees(subtotal - savingTotal);
    };

    const setQty = (i, qty) => {
      cart[i].qty = Math.max(1, Math.min(999, Math.round(qty) || 1));
      saveCart();
      render();
    };
    list.addEventListener("click", (event) => {
      const row = event.target.closest("[data-line]");
      if (!row) return;
      const i = Number(row.dataset.line);
      const step = event.target.closest("[data-step]");
      if (step) setQty(i, cart[i].qty + Number(step.dataset.step));
      if (event.target.closest("[data-edit]")) write("ctrlp-draft", { ...cart[i], replaces: cart[i].key });
      if (event.target.closest("[data-remove]")) {
        cart.splice(i, 1);
        saveCart();
        render();
      }
    });
    list.addEventListener("change", (event) => {
      const row = event.target.closest("[data-line]");
      if (row && event.target.matches("[data-qty]")) setQty(Number(row.dataset.line), Number(event.target.value));
    });
    render();
  }

  /* ---------- Press G to show the column grid ---------- */
  const gridlines = $("[data-gridlines]");
  if (gridlines) {
    document.addEventListener("keydown", (event) => {
      if (event.key.toLowerCase() !== "g" || event.metaKey || event.ctrlKey || event.altKey) return;
      if (event.target.closest("input, textarea, select")) return;
      gridlines.hidden = !gridlines.hidden;
    });
  }
})();
