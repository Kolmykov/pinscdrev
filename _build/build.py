#!/usr/bin/env python3
"""Собирает index.html, catalog.html, cart.html из общих кусков. Запуск: python3 _build/build.py (из папки prototype)."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent

SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></symbol>
<symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 20.5 4.2 12.8a4.9 4.9 0 0 1 6.9-7L12 6.7l.9-.9a4.9 4.9 0 0 1 6.9 7z"/></symbol>
<symbol id="i-cart" viewBox="0 0 24 24"><path d="M2.5 3.5h3l2.3 11.2h10.4l2.3-8.2H6.2"/><circle cx="9.3" cy="19.2" r="1.5"/><circle cx="17" cy="19.2" r="1.5"/></symbol>
<symbol id="i-arrow" viewBox="0 0 10 10"><path d="M0 5h9M5 1l4 4-4 4"/></symbol>
<symbol id="i-plus" viewBox="0 0 14 14"><path d="M7 1v12M1 7h12"/></symbol>
<symbol id="i-minus" viewBox="0 0 16 16"><path d="M3 8h10"/></symbol>
<symbol id="i-plus16" viewBox="0 0 16 16"><path d="M8 3v10M3 8h10"/></symbol>
<symbol id="i-check" viewBox="0 0 14 14"><path d="M2 7.5 5.5 11 12 3.5"/></symbol>
<symbol id="i-chev" viewBox="0 0 16 16"><path d="M3 6l5 5 5-5"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M5 5l14 14M19 5 5 19"/></symbol>
<symbol id="i-x14" viewBox="0 0 14 14"><path d="M0 0 14 14M14 0 0 14"/></symbol>
<symbol id="i-ne" viewBox="0 0 24 24"><path d="M6 18 18 6M8 6h10v10"/></symbol>
</defs></svg>'''

def ic(name, cls='', size=None):
    c = 'i' + (' ' + cls if cls else '')
    return f'<svg class="{c}"><use href="#i-{name}"/></svg>'

def header(hero):
    cls = 'hdr hdr--hero' if hero else 'hdr'
    base = '' if hero else ''
    home = 'index.html'
    return f'''<header class="{cls}" id="hdr"><div class="w hdr__row">
  <div class="hdr__l"><a class="hdr__logo" href="{home}">Пинскдрев</a>
    <nav class="hdr__nav"><a href="catalog.html">Каталог</a><a href="{home}#rooms">Комнаты</a><a href="{home}#kits">Коллекции</a><a href="catalog.html?tab=sale">Акции</a><a href="{home}#shop">Где купить</a></nav></div>
  <div class="hdr__r"><a class="btn btn--line" href="{home}#shop">Заказать звонок</a>
    <div class="hdr__icons"><a href="#" aria-label="Профиль">{ic('user')}</a><a href="catalog.html?tab=fav" aria-label="Избранное">{ic('heart')}<span class="badge" id="favBadge">0</span></a><a href="cart.html" aria-label="Корзина">{ic('cart')}<span class="badge" id="badge">0</span></a></div></div>
</div></header>'''

FOOTER = '''<footer class="ftr" id="footer"><div class="w">
  <div class="ftr__cols">
    <div class="ftr__about"><p>Мебель из массива дерева. Беларусь и Европа.</p><b>Пинскдрев</b>
      <form class="ftr__form" onsubmit="return false"><input type="email" placeholder="Почта для новостей и акций" aria-label="Почта"><button aria-label="Подписаться"><svg class="i"><use href="#i-arrow"/></svg></button></form></div>
    <div><h4>Покупателям</h4><ul><li><a href="#">Доставка</a></li><li><a href="#">Оплата</a></li><li><a href="#">Рассрочка</a></li><li><a href="#">Сборка</a></li><li><a href="#">Опт и дизайнерам</a></li></ul></div>
    <div><h4>О компании</h4><ul><li><a href="#">Контакты</a></li><li><a href="#">Блог</a></li><li><a href="#">Отзывы</a></li><li><a href="#">Производители</a></li><li><a href="index.html#about">О нас</a></li></ul></div>
    <div><h4>Контакты</h4><ul><li><a href="#">Написать директору</a></li><li><a href="#">Telegram · WhatsApp</a></li><li><a href="mailto:mebel@pandrev.ru">mebel@pandrev.ru</a></li><li><a href="tel:88005501420">8 800 550-14-20</a></li></ul></div>
  </div>
  <div class="ftr__legal"><p>Информация на сайте носит ознакомительный характер и не является публичной офертой. Цвета на фото могут отличаться от натуральных.</p><p>© 2012–2026 Пинскдрев · Политика конфиденциальности</p></div>
</div><div class="bigword" aria-hidden="true">Пинскдрев</div></footer>'''

MINI = '''<div class="mini" id="mini" aria-hidden="true"><div class="mini__scrim" data-close></div>
<aside class="mini__panel" role="dialog" aria-label="Товар добавлен в корзину">
  <button class="mini__x" data-close aria-label="Закрыть"><svg class="i"><use href="#i-x14"/></svg></button>
  <h3>Товар добавлен в корзину</h3>
  <div class="mini__item" id="miniItem"></div>
  <div class="mini__tot"><span id="miniCount">В корзине 1 товар</span><b id="miniSum">0 ₽</b></div>
  <div class="mini__btns"><a class="btn btn--fill btn--full" href="cart.html">Перейти в корзину</a><button class="btn btn--line btn--full" data-close>Продолжить покупки</button></div>
  <p class="mini__note">Сборку и доставку можно выбрать в корзине.</p>
</aside></div>'''

def ic(name, cls='', size=None):
    c = 'i' + (' ' + cls if cls else '')
    return f'<svg class="{c}"><use href="#i-{name}"/></svg>'

def header(hero):
    cls = 'hdr hdr--hero' if hero else 'hdr'
    base = '' if hero else ''
    home = 'index.html'
    return f'''<header class="{cls}" id="hdr"><div class="w hdr__row">
  <div class="hdr__l"><a class="hdr__logo" href="{home}">Пинскдрев</a>
    <nav class="hdr__nav"><a href="catalog.html">Каталог</a><a href="{home}#rooms">Комнаты</a><a href="{home}#kits">Коллекции</a><a href="catalog.html?tab=sale">Акции</a><a href="{home}#shop">Где купить</a></nav></div>
  <div class="hdr__r"><a class="btn btn--line" href="{home}#shop">Заказать звонок</a>
    <div class="hdr__icons"><a href="#" aria-label="Профиль">{ic('user')}</a><a href="catalog.html?tab=fav" aria-label="Избранное">{ic('heart')}<span class="badge" id="favBadge">0</span></a><a href="cart.html" aria-label="Корзина">{ic('cart')}<span class="badge" id="badge">0</span></a></div></div>
</div></header>'''

FOOTER = '''<footer class="ftr" id="footer"><div class="w">
  <div class="ftr__cols">
    <div class="ftr__about"><p>Мебель из массива дерева. Беларусь и Европа.</p><b>Пинскдрев</b>
      <form class="ftr__form" onsubmit="return false"><input type="email" placeholder="Почта для новостей и акций" aria-label="Почта"><button aria-label="Подписаться"><svg class="i"><use href="#i-arrow"/></svg></button></form></div>
    <div><h4>Покупателям</h4><ul><li><a href="#">Доставка</a></li><li><a href="#">Оплата</a></li><li><a href="#">Рассрочка</a></li><li><a href="#">Сборка</a></li><li><a href="#">Опт и дизайнерам</a></li></ul></div>
    <div><h4>О компании</h4><ul><li><a href="#">Контакты</a></li><li><a href="#">Блог</a></li><li><a href="#">Отзывы</a></li><li><a href="#">Производители</a></li><li><a href="index.html#about">О нас</a></li></ul></div>
    <div><h4>Контакты</h4><ul><li><a href="#">Написать директору</a></li><li><a href="#">Telegram · WhatsApp</a></li><li><a href="mailto:mebel@pandrev.ru">mebel@pandrev.ru</a></li><li><a href="tel:88005501420">8 800 550-14-20</a></li></ul></div>
  </div>
  <div class="ftr__legal"><p>Информация на сайте носит ознакомительный характер и не является публичной офертой. Цвета на фото могут отличаться от натуральных.</p><p>© 2012–2026 Пинскдрев · Политика конфиденциальности</p></div>
</div><div class="bigword" aria-hidden="true">Пинскдрев</div></footer>'''



ZOOM = """<script>document.documentElement.classList.add('js');
/* макет рассчитан на 1440: на более узком окне все размеры масштабируются через --u */
(function(){var d=document.documentElement;function f(){var w=d.clientWidth;d.style.setProperty('--u',(w<1440?w/1440:1)+'px')}f();addEventListener('resize',f)})();</script>"""
ZOOM_BODY = ""

def head(title, cls=''):
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.ico" sizes="48x48"><link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="stylesheet" href="css/site.css?v=20261019b">
{ZOOM}
</head><body class="{cls}">
{ZOOM_BODY}
{SPRITE}'''

TAIL = '''{mini}
<script src="js/site.js"></script>
</body></html>'''

def row(a, b):
    return f'<div class="sec-row rv"><span>{a}</span><span>{b}</span></div>'

def room(name, tab, pill, left_pill=False):
    p = f'<img class="pill" src="img/pill-{pill}.jpg" alt="">' if pill else ''
    txt = f'<span>{name}</span>'
    inner = (p + txt) if left_pill else (txt + p)
    cls = ' class="has-pill"' if pill else ''
    return f'<a{cls} href="catalog.html?tab={tab}">{inner}</a>'

# ---------------- главная ----------------
def index():
    rooms = '\n'.join([
        '<div class="rlist__row">' + room('Спальни','spalni','spalni') + room('Гостиные','gostinye','gostinye',True) + '</div>',
        '<div class="rlist__row">' + room('Кабинеты','kabinety','kabinety',True) + room('Детские','detskie','detskie',True) + '</div>',
        '<div class="rlist__row">' + room('Прихожие','prihozhie',None) + '</div>',
        '<div class="rlist__row">' + room('Кухни и столовые','kuhni','kuhni') + '</div>',
        '<div class="rlist__row">' + room('Дача','dacha','dacha',True) + '</div>',
        '<div class="rlist__row">' + room('Мягкая мебель','myagkaya',None) + '</div>',
        '<div class="rlist__row">' + room('Для бизнеса','biznes',None) + '</div>'])
    mats = [('oak','Дуб','Самый прочный. Выразительный рисунок, служит поколениями.'),
            ('beech','Бук','Плотный и ровный, с тёплым розоватым оттенком.'),
            ('birch','Берёза','Светлая, с мягким узором. Подходит для детской.'),
            ('pine','Сосна','Тёплая и доступная. Хороша для дачи и спальни.'),
            ('alder','Ольха','Медовый цвет, мягкая древесина. Красиво темнеет.')]
    mrows = '\n'.join(f'<a class="mrow rv" href="catalog.html?wood={k}"><div class="mrow__l"><img src="img/mat-{k}.jpg" alt=""><h3>{n}</h3></div><p>{t}</p>{ic("ne")}</a>' for k,n,t in mats)
    fabs = ['Вилейская мебельная фабрика','Гомельдрев','Молодечномебель','Пинскдрев','Фёнэча-Арт','Минский мебельный центр','Szynaka Meble','Пандрев']
    marq = ''.join(f'<span>{f}</span>' for f in fabs)
    steps = [('01','Вы выбираете мебель','В каталоге или в шоу-руме на ВДНХ. Подскажем по размерам, породе и отделке.'),
             ('02','Оплачиваете удобно','Картой, по счёту или наличными в шоу-руме. Есть рассрочка без переплаты.'),
             ('03','Мы доставляем','По всей России. Привозим с фабрики и бережно упаковываем.'),
             ('04','Собираем у вас дома','В Москве и области сборка и установка входят в услугу.')]
    st = '\n'.join(f'<div class="step rv"><i>{a}</i><div><h3>{b}</h3><p>{c}</p></div></div>' for a,b,c in steps)
    body = head('Пинскдрев — мебель из массива дерева', 'home') + header(True) + f'''
<div id="top"></div>
<main>
<section class="hero" id="hero"><div class="hero__bg"></div>
  <div class="w hero__in">
    <a class="hero__card" href="catalog.html?tab=hits"><div><h2>Хит: кровать «Луи Филипп»</h2><p>Массив дуба, от 129 900 ₽</p></div><span class="go">Смотреть {ic('arrow')}</span><img src="img/herocard.jpg" alt="Кровать «Луи Филипп»"></a>
    <div class="hero__bot"><div><h1 class="hero__title">Пинскдрев</h1><p class="hero__sub">Мы не делаем мебель на один сезон.<br>Мы делаем мебель, которую передают детям.</p></div>
      <a class="btn btn--white" href="index.html#kits">Создать комплект {ic('arrow')}</a></div>
  </div></section>

<section class="band rooms" id="rooms"><div class="w">{row('Комнаты','02')}
  <p class="rooms__lead rv">Мы подберём для вас</p>
  <div class="rlist rv">{rooms}</div></div></section>

<section class="cat" id="catalog"><div class="w">{row('Каталог','03')}
  <div class="cat__head rv"><h2 class="h64">Не просто мебель, а <em>тактильная архитектура</em> вашего дома</h2>
    <div class="tabs" role="tablist" id="homeTabs"><button class="tab" role="tab" aria-selected="true" data-f="all">Все</button><button class="tab" role="tab" aria-selected="false" data-f="new">Новинки</button><button class="tab" role="tab" aria-selected="false" data-f="hit">Хиты</button><button class="tab" role="tab" aria-selected="false" data-f="sale">Акции</button></div></div>
  <div class="grid3 home-grid" id="homeGrid"></div>
  <div class="cat__foot rv"><p>Только модели с ценой и в наличии</p><a class="btn btn--line btn--brown" href="catalog.html">Весь каталог {ic('arrow')}</a></div>
</div></section>

<section class="fsec fsec--week" id="week"><div class="fsec__band" style="background-image:url(img/band-week.jpg)"></div>
  <div class="w">{row('Новинка','04')}
    <h2 class="fsec__title rv">Выбор недели</h2>
    <div class="week__l rv"><h3>Кресло «Онда»</h3>
      <p>Обеденное кресло из массива европейского дуба. Мягкие линии и ручная отделка маслом подчёркивают характер дерева. Спокойно вписывается в гостиную, кухню и кабинет.</p>
      <div class="spec"><div class="spec__r"><b>Размеры</b><span>В 76 × Ш 52 × Г 49 см</span></div><div class="spec__r"><b>Вес</b><span>4,2 кг</span></div><div class="spec__r"><b>Материал</b><span>Массив дуба</span></div><div class="spec__r"><b>Отделка</b><span>Натуральное матовое масло</span></div><div class="spec__r"><b>Цвет</b><div class="dots"><i style="background:#c9b08e"></i><i style="background:#7a6654"></i><i style="background:#3b2e25"></i></div></div></div>
      <div class="buy"><strong>48 900 ₽</strong><button class="btn btn--fill" data-add="chair">Добавить в корзину</button></div></div>
    <div class="week__r"><div class="ph-img rv"><img src="img/chair-1.jpg" alt="Кресло «Онда»"></div><div class="ph-img rv d1"><img src="img/chair-2.jpg" alt="Кресло «Онда», деталь"></div></div>
  </div></section>

<section class="fsec fsec--kits" id="kits"><div class="fsec__band" style="background-image:url(img/band-kits.jpg)"></div>
  <div class="w">{row('Комплекты','05')}
    <div class="kits__title rv"><h2>Готовые комнаты</h2><p>Каждая коллекция собрана в комнату, и вам остаётся выбрать цвет.</p></div>
    <div class="kits__l rv"><small>Коллекция «Луи Филипп»</small><h3>Спальня из массива дуба</h3>
      <dl><div><dt>Состав</dt><dd>Кровать 160×200, две тумбы, комод, шкаф трёхстворчатый.</dd></div><div><dt>Материал</dt><dd>Массив дуба, натуральное матовое масло.</dd></div></dl>
      <div class="kits__price"><small class="kits__cap">Цена комплекта</small><b>от 389 000 ₽ <s>445 000 ₽</s></b></div>
      <a class="btn btn--fill" href="catalog.html?tab=spalni">Смотреть комплект</a></div>
    <div class="kits__photo ph-img rv d1"><img src="img/kits-big.jpg" alt="Спальня «Луи Филипп»">
      <div class="review"><div class="review__h"><i></i>Анна, Москва</div><p>Привезли в срок, собрали за день. Через год выглядит так же, как в шоу-руме.</p><span class="st">★★★★★</span></div></div>
    <div class="kits__row rv"><a class="kit" href="catalog.html?tab=gostinye"><div class="kit__img"><img src="img/kit-telma.jpg" alt=""></div><div><h4>Тельма</h4><p>Гостиная: диван, стол, стеллаж, тумба под ТВ. Бук.</p><b>от 276 000 ₽</b></div></a>
      <a class="kit" href="catalog.html?tab=kabinety"><div class="kit__img"><img src="img/kit-classic.jpg" alt=""></div><div><h4>Классик</h4><p>Кабинет: стол, кресло, книжный шкаф. Ольха.</p><b>от 198 000 ₽</b></div></a></div>
  </div></section>

<section class="band mat" id="materials"><div class="w">{row('Материалы','06')}
  <h2 class="mat__title rv"><span>Пять </span><span class="pill pill--stripes" aria-hidden="true" style="display:flex;overflow:hidden;flex:none;width:calc(110*var(--u));height:calc(70*var(--u))"><i style="flex:1;background:url(img/mat-oak.jpg) center/cover"></i><i style="flex:1;background:url(img/mat-beech.jpg) center/cover"></i><i style="flex:1;background:url(img/mat-birch.jpg) center/cover"></i><i style="flex:1;background:url(img/mat-pine.jpg) center/cover"></i><i style="flex:1;background:url(img/mat-alder.jpg) center/cover"></i></span><span>пород дерева, пять характеров</span></h2>
  <div class="mlist">{mrows}</div>
  <p class="mat__note rv">Цвет дерева лучше увидеть вживую: образцы всех пород лежат <a href="#shop">в шоу-руме на ВДНХ {ic('arrow')}</a></p>
</div></section>

<section class="about" id="about"><div class="w">{row('О нас','07')}
  <div class="about__top rv"><h2>Мы знаем каждую <em>фабрику</em><br>и отвечаем за каждый шкаф,<br>который привозим</h2>
    <div class="stats"><div class="stat"><div class="stat__n"><span data-n="15">15</span><sup>+</sup></div><p>фабрик Беларуси<br>и России</p></div><div class="stat"><div class="stat__n"><span data-n="50">50</span><sup>+</sup></div><p>коллекций<br>из массива</p></div><div class="stat"><div class="stat__n"><span data-n="14">14</span><sup>+</sup></div><p>лет на рынке</p></div></div></div>
</div>
<div class="marq"><div class="marq__row">{marq}{marq}</div></div></section>

<section class="band proc" id="how"><div class="w">{row('Условия','08')}
  <h2 class="h64 rv">Как мы работаем</h2>
  <div class="proc__body"><div class="proc__photo ph-img rv"><img src="img/process.jpg" alt=""></div><div class="steps">{st}</div></div></div></section>

<section class="shop" id="shop"><div class="w">{row('Где купить','09')}
  <div class="shop__body"><div class="shop__l rv"><h2>Приезжайте <em>в шоу-рум</em></h2>
    <div><dl class="shop__info"><div><dt>Адрес</dt><dd>г. Москва, ул. Ярославская, д. 8, к. 4, БЦ «Авантаж»</dd></div><div><dt>График</dt><dd>Пн–Пт 10:00–18:00, Сб–Вс 10:00–15:00</dd></div><div><dt>Телефон</dt><dd>+7 495 920-16-50</dd></div></dl>
      <form class="form" id="visit"><input placeholder="Имя" aria-label="Имя"><input type="tel" placeholder="Телефон" aria-label="Телефон"><button class="btn btn--fill btn--full" type="submit">Записаться в шоу-рум</button><small>Нажимая кнопку, вы соглашаетесь с политикой конфиденциальности.</small></form></div></div>
    <div class="shop__map ph-img rv d1"><img src="img/showroom.jpg" alt="Шоу-рум на ВДНХ"></div></div></div></section>

<section class="band pro" id="pro"><div class="w"><div class="pro__l rv"><small>Дизайнерам и оптом</small><h2>Мебель для проектов под ключ</h2></div>
  <div class="pro__r rv"><p>Особые цены, подбор по спецификации и доставка на объект.</p><a class="btn btn--line" href="#">Запросить предложение</a></div></div></section>
</main>
{FOOTER}
''' + TAIL.format(mini=MINI)
    return body

# ---------------- каталог ----------------
def catalog():
    tabs = [('all','Все'),('spalni','Спальни'),('gostinye','Гостиные'),('kabinety','Кабинеты'),('detskie','Детские'),('prihozhie','Прихожие'),('kuhni','Кухни и столовые'),('dacha','Дача')]
    tb = ''.join(f'<button class="tab" role="tab" aria-selected="{"true" if k=="all" else "false"}" data-tab="{k}">{n}</button>' for k,n in tabs)
    def chk(name, val, label, cnt):
        return f'<li><label class="fi"><input type="checkbox" name="{name}" value="{val}"><span class="bx">{ic("check")}</span><span class="lbl">{label}</span><small>{cnt}</small></label></li>'
    woods = ''.join(chk('wood', n, n, c) for n,c in [('Дуб',18),('Бук',9),('Берёза',7),('Ольха',5),('Сосна',3)])
    sizes = ''.join(chk('size', v, l, c) for v,l,c in [('90×200','90 × 200',5),('140×200','140 × 200',12),('160×200','160 × 200',16),('180×200','180 × 200',9)])
    feats = ''.join(chk('feat', k, n, c) for k,n,c in [('lift','С подъёмным механизмом',11),('drawers','С ящиками',8),('soft','Мягкое изголовье',7)])
    return head('Каталог — Пинскдрев', 'inner') + header(False) + f"""
<main>
<section><div class="w"><div class="sec-row"><span>Каталог</span><span class="crumbs"><a href="index.html">Главная</a>  /  Каталог</span></div>
  <div class="page-head"><h1 class="h64">Мебель из массива <em>дерева</em></h1><div class="tabs" role="tablist" id="ctabs">{tb}</div></div>
  <div class="cbody">
    <aside class="cf" id="filters">
      <div class="fg"><h4>Порода дерева</h4><ul>{woods}</ul></div>
      <div class="fg"><h4>Цена, ₽</h4><div class="prange"><input id="pmin" inputmode="numeric" value="12 900" aria-label="Цена от"><span>—</span><input id="pmax" inputmode="numeric" value="248 000" aria-label="Цена до"></div>
        <div class="slider" id="slider"><i class="slider__t"></i><i class="slider__r" id="sr"></i><button class="slider__h" id="sh1" aria-label="Минимальная цена"></button><button class="slider__h" id="sh2" aria-label="Максимальная цена"></button></div></div>
      <div class="fg"><h4>Размер спального места</h4><ul>{sizes}</ul></div>
      <div class="fg"><h4>Особенности</h4><ul>{feats}</ul></div>
      <div class="fg fg--sw"><span>Только в наличии</span><button class="sw" id="stock" aria-pressed="false" aria-label="Только в наличии"></button></div>
      <button class="btn btn--line btn--full" id="reset">Сбросить фильтры</button>
    </aside>
    <div class="cmain"><div class="cbar"><span id="cnt">6 из 42 моделей</span><label class="sort"><small>Сортировка:</small><select id="sort"><option value="pop">Сначала популярные</option><option value="asc">Сначала дешевле</option><option value="desc">Сначала дороже</option></select>{ic('chev')}</label></div>
      <div class="grid3 grid3--c" id="cgrid"></div><div class="empty-f" id="cempty">По этим условиям моделей нет. Попробуйте сбросить фильтры.</div>
      <div class="cpager"><span id="cpg">Показано 6 из 42</span><button class="btn btn--line" id="more">Показать ещё</button></div></div>
  </div></div></section>
<section class="band cbanner"><div class="w"><div class="cbanner__t"><h2>Нужен другой размер или отделка?</h2><p>Изготовим мебель по вашим размерам из выбранной породы дерева. Срок от 14 дней, замер и доставка включены.</p><a class="btn btn--fill" href="index.html#shop">Рассчитать на заказ</a></div><div class="cbanner__img ph-img"><img src="img/hero.jpg" alt=""></div></div></section>
</main>
{FOOTER}
""" + TAIL.format(mini=MINI)

# ---------------- корзина ----------------
def cart():
    return head('Корзина — Пинскдрев', 'inner cart-page') + header(False) + f"""
<main id="cartPage">
<section><div class="w"><div class="sec-row"><span>Корзина</span><span class="crumbs"><a href="index.html">Главная</a>  /  Корзина</span></div>
  <div class="cart__title"><h1 class="h64">Корзина</h1><span class="cart__count" id="ccount">0 товаров</span></div>
  <div class="cempty" id="cempty"><div class="cempty__ic">{ic('cart')}</div><h2>В корзине пока ничего нет</h2><p>Выберите мебель в каталоге или начните с готовых комнат.</p><div class="cempty__b"><a class="btn btn--fill" href="catalog.html">Перейти в каталог</a><a class="btn btn--line" href="index.html#kits">Готовые комнаты</a></div></div>
  <div class="cart__body"><div class="clist" id="clist"></div>
    <aside class="cright"><div class="sum"><h3>Ваш заказ</h3>
      <div class="sum__rows"><div class="sum__r"><span class="mut" id="sGoodsL">Товары</span><b id="sGoods">0 ₽</b></div><div class="sum__r"><span class="mut">Сборка</span><b id="sAsm">0 ₽</b></div><div class="sum__r"><span class="mut">Доставка</span><span class="mut">рассчитаем по адресу</span></div></div><hr>
      <div class="sum__t"><small>Итого</small><b id="sTot">0 ₽</b></div>
      <div class="promo"><input placeholder="Промокод" aria-label="Промокод"><button>Применить</button></div>
      <button class="btn btn--fill btn--full" id="checkout">Оформить заказ</button>
      <p class="sum__n">Оплата картой на сайте или при получении. Рассрочка 0% на 12 месяцев на заказы от 30 000 ₽.</p></div>
      <ul class="info"><li><b>Доставка по России</b><small>От 3 дней. Подъём на этаж и вынос упаковки по договорённости.</small></li><li><b>Сборка мастером</b><small>1–2 дня после доставки. Гарантия на сборку 1 год.</small></li><li><b>Гарантия 5 лет</b><small>На каркас и фурнитуру, замена деталей без споров.</small></li></ul></aside></div>
</div></section>
<section class="cross"><div class="w"><div class="cross__h"><h2 class="h48" id="xtitle">С этим покупают</h2><a class="btn btn--line" href="catalog.html">Весь каталог</a></div>
  <div class="grid4" id="xgrid"></div></div></section>
</main>
{FOOTER}
""" + TAIL.format(mini=MINI)

(root/'index.html').write_text(index(), encoding='utf-8')
(root/'catalog.html').write_text(catalog(), encoding='utf-8')
(root/'cart.html').write_text(cart(), encoding='utf-8')
print('ok')

# CSS: каждый px (кроме 0 и 1px) → calc(N * var(--u))
def px(m):
    v = float(m.group(1))
    if v in (0.0, 1.0, -1.0): return m.group(0)
    n = m.group(1)
    return f'calc({n}*var(--u))'
src = (root/'css'/'site.src.css').read_text(encoding='utf-8')
out = re.sub(r'(?<![\w.\-])(-?\d*\.?\d+)px', px, src)
(root/'css'/'site.css').write_text(out, encoding='utf-8')
print('css ok')
