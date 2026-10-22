(function () {
    // Cart (shared with the Store page)
    var mem = [];
    function readCart() { try { return JSON.parse(localStorage.getItem('nestling_cart')) || []; } catch (e) { return mem; } }
    function saveCart(c) { mem = c; try { localStorage.setItem('nestling_cart', JSON.stringify(c)); } catch (e) { } }
    function showCount() {
        var n = readCart().reduce(function (s, i) { return s + i.quantity; }, 0);
        var el = document.getElementById('cart-count'); if (el) el.textContent = n;
    }
    var t, toastEl = document.getElementById('toast');
    function toast(msg) { if (!toastEl) return; toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(t); t = setTimeout(function () { toastEl.classList.remove('on'); }, 2600); }
    document.querySelectorAll('.add-btn').forEach(function (b) {
        b.addEventListener('click', function () {
            var qty = parseInt(b.dataset.qty, 10) || 1, cart = readCart(), id = b.dataset.id;
            var item = cart.filter(function (i) { return i.id === id; })[0];
            if (item) item.quantity += qty; else cart.push({ id: id, name: b.dataset.name, price: parseFloat(b.dataset.price), quantity: qty });
            saveCart(cart); showCount();
            toast((qty > 1 ? qty + ' x ' : '') + b.dataset.name + ' added to your cart!');
        });
    });
    showCount();

    // "You came from Nest Helper": shown when the page is opened from a button in the chat
    var q = new URLSearchParams(location.search), from = document.getElementById('from');
    var why = { refill: 'a refill reminder', sizeup: 'a size-up reminder', milestone: 'a milestone message', winback: 'a welcome-back message', reorder: 'your reorder' };
    if (from && q.get('utm_source') === 'livechat') {
        var m = q.get('utm_medium');
        from.textContent = 'You came from Nest Helper' + (m ? ' (' + (why[m] || m) + ')' : '') + '. Add it to your cart below.';
        from.hidden = false;
    }
})();
