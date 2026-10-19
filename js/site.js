/* Пинскдрев — общий скрипт: данные, корзина, избранное, фильтры, анимации */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var ICON = function (n) { return '<svg class="i"><use href="#i-' + n + '"/></svg>'; };

  /* ---------- данные ---------- */
  var P = [
    { id: "bed", title: "Кровать «Луи Филипп»", wood: "Дуб", meta: "Дуб, 160×200", price: 129900, old: 149900, tag: "ХИТ", cats: ["spalni"], size: "160×200", feat: ["lift", "soft"], asm: 5900, stock: true, kind: "hit", img: "p-bed", art: 20418 },
    { id: "commode", title: "Комод «Тельма»", wood: "Бук", meta: "Бук, 4 ящика", price: 68900, tag: "НОВИНКА", cats: ["spalni", "gostinye"], feat: ["drawers"], asm: 3400, stock: false, kind: "new", img: "p-commode", art: 31207 },
    { id: "table", title: "Стол обеденный", wood: "Дуб", meta: "Дуб, 180×90", price: 94500, tag: "ХИТ", cats: ["kuhni"], feat: [], asm: 2900, stock: true, kind: "hit", img: "p-table", art: 20533 },
    { id: "wardrobe", title: "Шкаф «Классик»", wood: "Ольха", meta: "Ольха, 3 створки", price: 112000, old: 134000, tag: "−16%", cats: ["spalni", "kabinety"], feat: [], asm: 4800, stock: true, kind: "sale", img: "p-wardrobe", art: 20671 },
    { id: "nightstand", title: "Тумба прикроватная", wood: "Берёза", meta: "Берёза", price: 24900, tag: "НОВИНКА", cats: ["spalni"], feat: ["drawers"], asm: 1200, stock: true, kind: "new", img: "p-nightstand", art: 20419 },
    { id: "shelf", title: "Стеллаж «Тельма»", wood: "Бук", meta: "Бук, 5 полок", price: 57900, tag: "ХИТ", cats: ["kabinety", "gostinye"], feat: [], asm: 1800, stock: true, kind: "hit", img: "p-shelf", art: 20744 },
    { id: "chair", title: "Кресло «Онда»", wood: "Дуб", meta: "Дуб, масло", price: 48900, cats: [], feat: [], asm: 0, stock: true, hidden: true, img: "chair-1", art: 20812 }
  ];
  var byId = {}; P.forEach(function (p) { byId[p.id] = p; });
  var NB = " ";
  var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, NB) + NB + "₽"; };
  var plural = function (n, a, b, c) { var m = n % 100, d = n % 10; return (m > 10 && m < 20) ? c : d === 1 ? a : (d > 1 && d < 5) ? b : c; };

  /* ---------- хранилище ---------- */
  var store = {
    get: function (k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var cart = store.get("pd_cart", []);
  var favs = store.get("pd_fav", []);
  var saveCart = function () { store.set("pd_cart", cart); badge(); };
  var qtyTotal = function () { return cart.reduce(function (s, i) { return s + i.qty; }, 0); };
  function badge() {
    var b = $("#badge"); if (!b) return;
    var n = qtyTotal(); b.textContent = n; b.classList.toggle("on", n > 0);
  }
  function favBadge() {
    var b = $("#favBadge"); if (!b) return;
    b.textContent = favs.length; b.classList.toggle("on", favs.length > 0);
  }
  function addToCart(id) {
    var it = cart.filter(function (i) { return i.id === id; })[0];
    if (it) it.qty += 1; else cart.push({ id: id, qty: 1, asm: false });
    saveCart();
  }

  /* ---------- уведомление ---------- */
  var toastT;
  function toast(t) {
    var e = $(".toast"); if (!e) { e = document.createElement("div"); e.className = "toast"; document.body.appendChild(e); }
    e.textContent = t; e.offsetWidth; e.classList.add("on");
    clearTimeout(toastT); toastT = setTimeout(function () { e.classList.remove("on"); }, 2800);
  }

  /* ---------- карточка товара ---------- */
  function card(p) {
    var inCart = cart.some(function (i) { return i.id === p.id; });
    var fav = favs.indexOf(p.id) > -1;
    return '<article class="card rv" data-id="' + p.id + '" data-kind="' + (p.kind || "") + '">' +
      '<div class="card__img"><img src="img/' + p.img + '.jpg" alt="' + p.title + '">' +
      '<button class="fav" aria-pressed="' + fav + '" aria-label="В избранное">' + ICON("heart") + '</button>' +
      (p.tag ? '<span class="tag">' + p.tag + '</span>' : '') +
      '<button class="add' + (inCart ? " on" : "") + '" data-add="' + p.id + '" aria-label="В корзину">' + ICON("plus").replace('class="i"', 'class="i i--plus"') + ICON("cart").replace('class="i"', 'class="i i--cart"') + ICON("check").replace('class="i"', 'class="i i--ok"') + '</button></div>' +
      '<div class="card__info"><div><div class="card__name">' + p.title + '</div><div class="card__meta">' + p.meta + '</div></div>' +
      '<div class="card__price">' + fmt(p.price) + (p.old ? '<s>' + fmt(p.old) + '</s>' : '') + '</div></div></article>';
  }
  function bindCards(root) {
    $$(".fav", root).forEach(function (b) {
      if (b._b) return; b._b = 1;
      b.addEventListener("click", function (e) {
        e.preventDefault(); e.stopPropagation();
        var id = b.closest(".card").dataset.id, i = favs.indexOf(id);
        if (i > -1) favs.splice(i, 1); else favs.push(id);
        store.set("pd_fav", favs); favBadge(); b.setAttribute("aria-pressed", i === -1);
        if (document.body.dataset.favOnly) catalog.render();
      });
    });
    reveal(root);
  }

  /* ---------- попап «товар добавлен» ---------- */
  function openMini(id) {
    var m = $("#mini"); if (!m) return;
    var p = byId[id];
    $("#miniItem").innerHTML = '<img src="img/' + p.img + '.jpg" alt=""><div><h4>' + p.title + '</h4><small>' + p.meta + '</small><b>' + fmt(p.price) + (p.old ? '<s>' + fmt(p.old) + '</s>' : '') + '</b></div>';
    var n = qtyTotal();
    $("#miniCount").textContent = "В корзине " + n + " " + plural(n, "товар", "товара", "товаров");
    $("#miniSum").textContent = fmt(total().sum);
    var de = document.documentElement, sw = window.innerWidth - de.clientWidth;
    de.style.paddingRight = sw + "px"; de.classList.add("lock");
    m.classList.add("open"); m.setAttribute("aria-hidden", "false");
  }
  function closeMini() {
    var m = $("#mini"); if (m) { m.classList.remove("open"); m.setAttribute("aria-hidden", "true"); }
    document.documentElement.classList.remove("lock"); document.documentElement.style.paddingRight = "";
  }
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-close]")) closeMini();
    var a = e.target.closest("[data-add]");
    if (a) {
      e.preventDefault(); var id = a.dataset.add;
      addToCart(id); $$('.add[data-add="' + id + '"]').forEach(function (x) { x.classList.add("on"); });
      openMini(id);
      if (window.cartPage) cartPage.render();
    }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMini(); });

  function total() {
    var goods = 0, asm = 0, n = 0;
    cart.forEach(function (i) { var p = byId[i.id]; if (!p) return; goods += p.price * i.qty; n += i.qty; if (i.asm) asm += p.asm * i.qty; });
    return { goods: goods, asm: asm, sum: goods + asm, n: n };
  }

  /* ---------- появление при прокрутке и счётчики ---------- */
  var io = ("IntersectionObserver" in window) ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: .12, rootMargin: "0px 0px -6% 0px" }) : null;
  function reveal(root) {
    $$(".rv:not(.in)", root).forEach(function (el) { if (io) io.observe(el); else el.classList.add("in"); });
  }
  function counters() {
    var els = $$("[data-n]"); if (!els.length || !io) return;
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; co.unobserve(e.target);
        var el = e.target, to = +el.dataset.n, t0 = performance.now();
        (function tick(t) { var k = Math.min(1, (t - t0) / 1400), v = 1 - Math.pow(1 - k, 3); el.textContent = Math.round(to * v); if (k < 1) requestAnimationFrame(tick); })(t0);
      });
    }, { threshold: .6 });
    els.forEach(function (el) { el.textContent = "0"; co.observe(el); });
  }

  /* ---------- шапка ---------- */
  function header() {
    var h = $("#hdr"); if (!h) return;
    var last = window.scrollY, ticking = false;
    var on = function () {
      var y = window.scrollY;
      h.classList.toggle("solid", y > 60);
      if (y > 60 && y < last - 4) h.classList.add("hide");          // вверх: шапка прячется
      else if (y > last + 4 || y <= 60) h.classList.remove("hide"); // вниз: показывается
      last = y; ticking = false;
    };
    on(); window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(on); } }, { passive: true });
  }

  /* ---------- неразрывные пробелы (никаких висячих предлогов) ---------- */
  function typo(root) {
    var re = /(?<=(?:^|[\s«(])(?:[авикосуя]|на|по|за|из|от|до|об|во|со|не|но|ни|же|бы|для|без|при|над|под|или|что|как|это|все|его|её|их))\s+/gi;
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), nodes = [];
    while (w.nextNode()) nodes.push(w.currentNode);
    nodes.forEach(function (n) { if (n.parentNode.closest("script,style,pre")) return; n.nodeValue = n.nodeValue.replace(re, " "); });
  }

  /* ---------- главная ---------- */
  function home() {
    var g = $("#homeGrid"); if (!g) return;
    g.innerHTML = P.filter(function (p) { return !p.hidden; }).map(card).join("");
    bindCards(g);
    $$("#homeTabs .tab").forEach(function (t) {
      t.addEventListener("click", function () {
        $$("#homeTabs .tab").forEach(function (x) { x.setAttribute("aria-selected", x === t); });
        var f = t.dataset.f;
        $$(".card", g).forEach(function (c) { c.classList.toggle("hide", f !== "all" && c.dataset.kind !== f); });
      });
    });
    var form = $("#visit");
    if (form) form.addEventListener("submit", function (e) { e.preventDefault(); form.reset(); toast("Спасибо! Мы перезвоним и подтвердим запись."); });
  }

  /* ---------- каталог ---------- */
  var catalog = { render: function () {} };
  var PMIN = 12900, PMAX = 248000;
  function catalogPage() {
    var grid = $("#cgrid"); if (!grid) return;
    var q = new URLSearchParams(location.search);
    var fresh = function () { return { cat: "all", woods: [], sizes: [], feats: [], kind: "", stock: false, min: PMIN, max: PMAX, sort: "pop", fav: false }; };
    var st = fresh();
    var tab = q.get("tab");
    if (tab === "hits") st.kind = "hit"; else if (tab === "new") st.kind = "new"; else if (tab === "sale") st.kind = "sale";
    else if (tab === "fav") { st.fav = true; document.body.dataset.favOnly = 1; }
    else if (tab && $('[data-tab="' + tab + '"]')) st.cat = tab;
    var wk = q.get("wood"), wd = { oak: "Дуб", beech: "Бук", birch: "Берёза", pine: "Сосна", alder: "Ольха" }[wk] || (["Дуб", "Бук", "Берёза", "Сосна", "Ольха"].indexOf(wk) > -1 ? wk : null);
    if (wd) { st.woods = [wd]; $$("#filters input[name=wood]").forEach(function (i) { i.checked = i.value === wd; }); }
    $$("#ctabs .tab").forEach(function (t) { t.setAttribute("aria-selected", t.dataset.tab === st.cat); });

    /* ползунок цены */
    var sl = $("#slider"), h1 = $("#sh1"), h2 = $("#sh2"), sr = $("#sr"), pmin = $("#pmin"), pmax = $("#pmax");
    var span = function () { return sl.clientWidth - h1.offsetWidth; };
    var draw = function () {
      var w = span(), hw = h1.offsetWidth;
      var a = (st.min - PMIN) / (PMAX - PMIN) * w, b = (st.max - PMIN) / (PMAX - PMIN) * w;
      h1.style.left = a + "px"; h2.style.left = b + "px"; sr.style.left = (a + hw / 2) + "px"; sr.style.width = (b - a) + "px";
    };
    var setV = function (k, v) {
      v = Math.round(v / 100) * 100;
      if (k === "min") st.min = Math.max(PMIN, Math.min(v, st.max - 1000)); else st.max = Math.min(PMAX, Math.max(v, st.min + 1000));
      pmin.value = fmt(st.min).replace(NB + "₽", ""); pmax.value = fmt(st.max).replace(NB + "₽", ""); draw(); catalog.render();
    };
    [h1, h2].forEach(function (h, idx) {
      h.addEventListener("pointerdown", function (e) {
        e.preventDefault(); h.setPointerCapture(e.pointerId);
        var rect = sl.getBoundingClientRect(), scale = rect.width / sl.offsetWidth;
        var mv = function (ev) { var x = (ev.clientX - rect.left) / scale - h.offsetWidth / 2; setV(idx ? "max" : "min", PMIN + x / span() * (PMAX - PMIN)); };
        var up = function () { h.removeEventListener("pointermove", mv); h.removeEventListener("pointerup", up); };
        h.addEventListener("pointermove", mv); h.addEventListener("pointerup", up);
      });
    });
    var num = function (v) { return +String(v).replace(/\D/g, "") || 0; };
    pmin.addEventListener("change", function () { setV("min", num(pmin.value)); });
    pmax.addEventListener("change", function () { setV("max", num(pmax.value)); });
    draw(); window.addEventListener("resize", draw);

    catalog.render = function () {
      var list = P.filter(function (p) {
        if (p.hidden) return false;
        if (st.fav && favs.indexOf(p.id) === -1) return false;
        if (st.cat !== "all" && p.cats.indexOf(st.cat) === -1) return false;
        if (st.woods.length && st.woods.indexOf(p.wood) === -1) return false;
        if (st.sizes.length && st.sizes.indexOf(p.size) === -1) return false;
        if (st.feats.length && !st.feats.every(function (f) { return p.feat.indexOf(f) > -1; })) return false;
        if (st.kind && p.kind !== st.kind) return false;
        if (st.stock && !p.stock) return false;
        if (p.price < st.min || p.price > st.max) return false;
        return true;
      });
      if (st.sort === "asc") list.sort(function (a, b) { return a.price - b.price; });
      if (st.sort === "desc") list.sort(function (a, b) { return b.price - a.price; });
      grid.innerHTML = list.map(card).join(""); bindCards(grid);
      $("#cnt").textContent = list.length + " из 42 моделей";
      $("#cpg").textContent = "Показано " + list.length + " из 42";
      $("#cempty").style.display = list.length ? "none" : "block";
      $(".cpager").style.display = list.length ? "" : "none";
    };
    $$("#ctabs .tab").forEach(function (t) {
      t.addEventListener("click", function () {
        st.cat = t.dataset.tab; st.fav = false; delete document.body.dataset.favOnly;
        $$("#ctabs .tab").forEach(function (x) { x.setAttribute("aria-selected", x === t); }); catalog.render();
      });
    });
    var coll = function (name) { return $$("#filters input[name=" + name + "]:checked").map(function (i) { return i.value; }); };
    $("#filters").addEventListener("change", function (e) {
      if (e.target.name === "wood") st.woods = coll("wood");
      if (e.target.name === "size") st.sizes = coll("size");
      if (e.target.name === "feat") st.feats = coll("feat");
      catalog.render();
    });
    $("#stock").addEventListener("click", function (e) { st.stock = e.currentTarget.getAttribute("aria-pressed") !== "true"; e.currentTarget.setAttribute("aria-pressed", st.stock); catalog.render(); });
    $("#sort").addEventListener("change", function (e) { st.sort = e.target.value; catalog.render(); });
    $("#reset").addEventListener("click", function () {
      st = fresh(); delete document.body.dataset.favOnly;
      $$("#filters input[type=checkbox]").forEach(function (i) { i.checked = false; });
      $("#stock").setAttribute("aria-pressed", "false"); $("#sort").value = "pop";
      pmin.value = "12" + NB + "900"; pmax.value = "248" + NB + "000"; draw();
      $$("#ctabs .tab").forEach(function (t) { t.setAttribute("aria-selected", t.dataset.tab === "all"); });
      catalog.render();
    });
    $("#more").addEventListener("click", function () { toast("Остальные модели появятся, когда подключим базу товаров."); });
    catalog.render();
  }

  /* ---------- корзина ---------- */
  var cartPage = null;
  var CROSS = ["commode", "table", "wardrobe", "shelf"];
  function cartPageInit() {
    var list = $("#clist"); if (!list) return;
    var q = new URLSearchParams(location.search);
    if (q.has("demo")) {
      cart = q.get("demo") === "1"
        ? [{ id: "bed", qty: 1, asm: true }]
        : [{ id: "bed", qty: 1, asm: true }, { id: "nightstand", qty: 2, asm: false }, { id: "commode", qty: 1, asm: true }];
      saveCart();
    }
    cartPage = window.cartPage = {
      render: function () {
        var t = total(), main = $("#cartPage");
        main.classList.toggle("cart--empty", !cart.length);
        $("#ccount").textContent = t.n + " " + plural(t.n, "товар", "товара", "товаров");
        $("#xtitle").textContent = cart.length ? "С этим покупают" : "Популярное сейчас";
        list.innerHTML = cart.map(function (i) {
          var p = byId[i.id]; if (!p) return "";
          return '<div class="ci" data-id="' + p.id + '"><div class="ci__img"><img src="img/' + p.img + '.jpg" alt=""></div>' +
            '<div class="ci__info"><div class="ci__txt"><a class="ci__name" href="catalog.html">' + p.title + '</a><div class="ci__meta">' + p.meta + '</div>' +
            '<div class="ci__meta">арт. ' + p.art + '</div></div>' +
            '<div class="ci__stock' + (p.stock ? '' : ' order') + '"><i></i>' + (p.stock ? 'В наличии, отправим через 3 дня' : 'Под заказ, изготовим за 14 дней') + '</div>' +
            '<label class="chk"><input type="checkbox" data-asm' + (i.asm ? ' checked' : '') + '><span class="bx">' + ICON("check") + '</span><span class="lbl">Сборка мастером, + ' + fmt(p.asm) + (i.qty > 1 ? ' за шт.' : '') + '</span></label>' +
            '<div class="ci__act"><button data-fav>' + (favs.indexOf(p.id) > -1 ? 'В избранном' : 'В избранное') + '</button><button data-del>Удалить</button></div></div>' +
            '<div class="ci__side"><div class="ci__price">' + fmt(p.price * i.qty) + (p.old ? '<small class="old">' + fmt(p.old * i.qty) + '</small>' : '') + (!p.old && i.qty > 1 ? '<small>' + fmt(p.price) + ' за шт.</small>' : '') + '</div>' +
            '<div class="step-q"><button data-q="-1" aria-label="Меньше">' + ICON("minus") + '</button><span>' + i.qty + '</span><button data-q="1" aria-label="Больше">' + ICON("plus16") + '</button></div></div></div>';
        }).join("");
        $("#sGoodsL").textContent = "Товары (" + t.n + ")";
        $("#sGoods").textContent = fmt(t.goods); $("#sAsm").textContent = t.asm ? fmt(t.asm) : "0" + NB + "₽"; $("#sTot").textContent = fmt(t.sum);
        $("#xgrid").innerHTML = CROSS.map(function (id) { return card(byId[id]); }).join(""); bindCards($("#xgrid"));
        typo(list);
      }
    };
    list.addEventListener("click", function (e) {
      var row = e.target.closest(".ci"); if (!row) return;
      var it = cart.filter(function (i) { return i.id === row.dataset.id; })[0];
      var qb = e.target.closest("[data-q]");
      if (qb) { it.qty = Math.max(1, Math.min(9, it.qty + +qb.dataset.q)); saveCart(); cartPage.render(); }
      if (e.target.closest("[data-del]")) { row.classList.add("out"); setTimeout(function () { cart = cart.filter(function (i) { return i !== it; }); saveCart(); cartPage.render(); }, 350); }
      if (e.target.closest("[data-fav]")) { var k = favs.indexOf(it.id); if (k > -1) favs.splice(k, 1); else favs.push(it.id); store.set("pd_fav", favs); favBadge(); cartPage.render(); }
    });
    list.addEventListener("change", function (e) {
      if (!e.target.matches("[data-asm]")) return;
      var row = e.target.closest(".ci"), it = cart.filter(function (i) { return i.id === row.dataset.id; })[0];
      it.asm = e.target.checked; saveCart(); var t = total();
      $("#sAsm").textContent = t.asm ? fmt(t.asm) : "0" + NB + "₽"; $("#sTot").textContent = fmt(t.sum);
    });
    $("#checkout").addEventListener("click", function () { toast("Оформление заказа подключим на следующем этапе."); });
    cartPage.render();
  }

  /* ---------- запуск ---------- */
  header(); badge(); favBadge();
  home(); catalogPage(); cartPageInit();
  reveal(document); counters();
  typo(document.body);
})();
