document.addEventListener('DOMContentLoaded', () => {
    // Same products, prices and page names as data/products.csv and the Nest Helper bot.
    const categoryProducts = {
        bodysuits: [
            { id: "bodysuit-nb", name: "Cotton Bodysuits NB (3 pack)", desc: "clothing; size NB; age 0-1 months", price: 18 },
            { id: "bodysuit-0-3m", name: "Cotton Bodysuits 0-3M (3 pack)", desc: "clothing; size 0-3M; age 0-3 months", price: 18 },
            { id: "bodysuit-3-6m", name: "Cotton Bodysuits 3-6M (3 pack)", desc: "clothing; size 3-6M; age 3-6 months", price: 19 },
            { id: "bodysuit-6-9m", name: "Cotton Bodysuits 6-9M (3 pack)", desc: "clothing; size 6-9M; age 6-9 months", price: 20 },
            { id: "bodysuit-9-12m", name: "Cotton Bodysuits 9-12M (3 pack)", desc: "clothing; size 9-12M; age 9-12 months", price: 20 },
            { id: "tee-set-12-18m", name: "Cotton Tee and Shorts Set 12-18M", desc: "clothing; size 12-18M; age 12-18 months", price: 22 }
        ],
        formula: [
            { id: "formula-stage-1", name: "Infant Formula Stage 1 (800g)", desc: "infant formula; stage 1; 0-6 months; fictional brand", price: 45 },
            { id: "formula-stage-2", name: "Follow-on Formula Stage 2 (800g)", desc: "follow-on formula; stage 2; 6-12 months; fictional brand", price: 43 },
            { id: "milk-stage-3", name: "Growing-up Milk Stage 3 (800g)", desc: "growing-up milk; stage 3; 1-3 years; fictional brand", price: 38 }
        ],
        bundles: [
            { id: "bundle-0-3m", name: "Stage Bundle 0-3M", desc: "bundle; size 0-3M; age 0-3 months", price: 49 },
            { id: "bundle-3-6m", name: "Stage Bundle 3-6M", desc: "bundle; size 3-6M; age 3-6 months", price: 52 },
            { id: "bundle-6-9m", name: "Stage Bundle 6-9M", desc: "bundle; size 6-9M; age 6-9 months", price: 58 },
            { id: "bundle-9-12m", name: "Stage Bundle 9-12M", desc: "bundle; size 9-12M; age 9-12 months", price: 58 },
            { id: "bundle-12-18m", name: "Stage Bundle 12-18M", desc: "bundle; size 12-18M; age 12-18 months", price: 62 }
        ],
        diapers: [
            { id: "diapers-nb", name: "Diapers Newborn (60)", desc: "diapers; size NB; up to 5 kg; age 0-1 months", price: 14 },
            { id: "diapers-1", name: "Diapers Size 1 (70)", desc: "diapers; size 1; 3-6 kg; age 0-3 months", price: 16 },
            { id: "diapers-2", name: "Diapers Size 2 (70)", desc: "diapers; size 2; 5-8 kg; age 3-6 months", price: 17 },
            { id: "diapers-3", name: "Diapers Size 3 (66)", desc: "diapers; size 3; 7-11 kg; age 6-10 months", price: 18 },
            { id: "diapers-4", name: "Diapers Size 4 (60)", desc: "diapers; size 4; 9-14 kg; age 10-18 months", price: 18 },
            { id: "wipes-80", name: "Water Wipes (80)", desc: "wipes; one size; age 0-36 months", price: 4 },
            { id: "wipes-3pk", name: "Water Wipes 3 Pack (240)", desc: "wipes; one size; age 0-36 months", price: 11 }
        ],
        toys: [
            { id: "sensory-1-rattle", name: "Sensory Set 1: Soft Rattle", desc: "toys; piece 1 of 4; from 3 months", price: 12 },
            { id: "sensory-2-crinkle-book", name: "Sensory Set 2: Crinkle Book", desc: "toys; piece 2 of 4; from 4 months", price: 14 },
            { id: "sensory-3-stacking-cups", name: "Sensory Set 3: Stacking Cups", desc: "toys; piece 3 of 4; from 6 months", price: 10 },
            { id: "sensory-4-shape-sorter", name: "Sensory Set 4: Shape Sorter", desc: "toys; piece 4 of 4; from 12 months", price: 19 },
            { id: "play-mat", name: "Padded Play Mat", desc: "toys; one size; age 3-24 months", price: 39 }
        ]
    };

    const modal = document.getElementById('product-modal');
    const closeModalBtn = document.querySelector('.close-modal-btn');
    const modalTitle = document.getElementById('modal-category-title');
    const modalNoticeBanner = document.getElementById('modal-notice-banner');
    const modalProductsList = document.getElementById('modal-products-list');

    // Small message instead of a pop-up alert
    const toastEl = document.getElementById('toast');
    let toastTimer;
    function toast(text) {
        if (!toastEl) return;
        toastEl.textContent = text;
        toastEl.classList.add('on');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toastEl.classList.remove('on'), 2600);
    }

    // Cart storage (works even if the browser blocks storage)
    let memoryCart = [];
    function readCart() {
        try { return JSON.parse(localStorage.getItem('nestling_cart')) || []; } catch (e) { return memoryCart; }
    }
    function saveCart(cart) {
        memoryCart = cart;
        try { localStorage.setItem('nestling_cart', JSON.stringify(cart)); } catch (e) { }
    }

    function openCategory(category, cardTitle) {
        modalTitle.textContent = cardTitle;
        modalProductsList.innerHTML = '';
        modalNoticeBanner.className = 'modal-notice-banner';

        if (category === 'bodysuits') {
            modalNoticeBanner.textContent = 'Free size exchange within 30 days on all baby clothing (unworn, with tags). Delivery is free both ways.';
        } else if (category === 'diapers') {
            modalNoticeBanner.textContent = 'Special Offer: Get a 10% discount automatically when you buy 3 or more of the same diaper or wet wipe pack!';
        } else if (category === 'bundles') {
            modalNoticeBanner.textContent = 'Free delivery on every Stage Bundle, plus free size exchange within 30 days.';
        } else if (category === 'formula') {
            modalNoticeBanner.textContent = 'Disclaimer: Sold at our usual price, no offers apply. Nestling cannot give advice on baby formula. Please consult a doctor for professional feeding advice.';
            modalNoticeBanner.classList.add('formula-warning');
        } else {
            modalNoticeBanner.textContent = 'Need help choosing? Ask the Nest Helper chatbot if you want assistance!';
            modalNoticeBanner.classList.add('chatbot-advice');
        }
        modalNoticeBanner.style.display = 'block';

        const items = categoryProducts[category] || [];
        items.forEach(item => {
            const productRow = document.createElement('div');
            productRow.className = 'modal-product-card';
            productRow.innerHTML = `
                <div class="modal-product-info">
                    <h4><a href="shop/${item.id}/index.html">${item.name}</a></h4>
                    <p>${item.desc}</p>
                    <span class="modal-product-price">S$${item.price.toFixed(2)}</span>
                </div>
                <div class="modal-product-actions">
                    <a class="store-btn details-btn" href="shop/${item.id}/index.html">Details</a>
                    <button class="store-btn add-to-cart-btn modal-add-btn"
                        data-id="${item.id}"
                        data-name="${item.name}"
                        data-price="${item.price}" type="button">Add to Cart</button>
                </div>
            `;
            modalProductsList.appendChild(productRow);
        });

        modal.style.display = 'flex';
        closeModalBtn.focus();
    }

    document.querySelectorAll('.view-product-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.store-card');
            openCategory(card.getAttribute('data-category'), card.querySelector('h3').textContent);
        });
    });

    // Links like store.html#diapers open that category straight away
    function openFromHash() {
        const hash = (location.hash || '').replace('#', '');
        const hashCard = hash && document.querySelector(`.store-card[data-category="${hash}"]`);
        if (hashCard && hashCard.querySelector('.view-product-btn')) {
            openCategory(hash, hashCard.querySelector('h3').textContent);
        }
    }
    openFromHash();
    window.addEventListener('hashchange', openFromHash);

    function closeModal() { modal.style.display = 'none'; }
    closeModalBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-to-cart-btn')) {
            const id = e.target.getAttribute('data-id');
            const name = e.target.getAttribute('data-name');
            const price = parseFloat(e.target.getAttribute('data-price'));

            let cart = readCart();
            const existingItem = cart.find(item => item.id === id);

            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cart.push({ id, name, price, quantity: 1 });
            }

            saveCart(cart);
            renderCart();
            toast(`Added "${name}" to your cart!`);
        }
    });

    const noOfferIds = ['formula-stage-1', 'formula-stage-2', 'milk-stage-3'];

    function renderCart() {
        const cart = readCart();
        const container = document.getElementById('cart-items-container');
        const totalPriceEl = document.getElementById('cart-total-price');
        const cartCountEl = document.getElementById('cart-count');
        const deliveryEl = document.getElementById('delivery-row');

        container.innerHTML = '';

        if (cart.length === 0) {
            container.innerHTML = '<p class="empty-cart-msg">Your cart is currently empty.</p>';
            totalPriceEl.textContent = 'S$0.00';
            if (cartCountEl) cartCountEl.textContent = '0';
            deliveryEl.textContent = 'Free delivery on Stage Bundles and on orders over S$60.';
            deliveryEl.classList.remove('unlocked');
            return;
        }

        let total = 0;
        let offerTotal = 0; // formula and milk don't count towards free delivery
        let totalCount = 0;
        let hasBundle = false;

        cart.forEach((item, index) => {
            let itemPrice = item.price;
            let hasDiscount = false;

            if ((item.id.startsWith('diapers') || item.id.startsWith('wipes')) && item.quantity >= 3) {
                itemPrice = item.price * 0.9;
                hasDiscount = true;
            }
            if (item.id.startsWith('bundle')) hasBundle = true;

            const itemSubtotal = itemPrice * item.quantity;
            total += itemSubtotal;
            if (!noOfferIds.includes(item.id)) offerTotal += itemSubtotal;
            totalCount += item.quantity;

            const itemRow = document.createElement('div');
            itemRow.className = 'cart-item-row';
            itemRow.innerHTML = `
                <div class="cart-item-details">
                    <span class="cart-item-name">${item.name}</span>
                    <span class="cart-item-price">S$${itemPrice.toFixed(2)} x ${item.quantity}</span>
                    ${hasDiscount ? '<span class="discount-tag">10% stock-up discount applied!</span>' : ''}
                </div>
                <div class="cart-item-controls">
                    <button class="qty-btn decrease-qty" data-index="${index}" aria-label="One less">-</button>
                    <span>${item.quantity}</span>
                    <button class="qty-btn increase-qty" data-index="${index}" aria-label="One more">+</button>
                    <button class="remove-item-btn" data-index="${index}" aria-label="Remove">&times;</button>
                </div>
            `;
            container.appendChild(itemRow);
        });

        totalPriceEl.textContent = `S$${total.toFixed(2)}`;
        if (cartCountEl) cartCountEl.textContent = totalCount;

        if (hasBundle || offerTotal > 60) {
            deliveryEl.textContent = 'Free delivery unlocked!';
            deliveryEl.classList.add('unlocked');
        } else {
            deliveryEl.textContent = `Free delivery on orders over S$60 (S$${Math.max(0, 60 - offerTotal).toFixed(2)} to go, formula and milk don't count), or add a Stage Bundle.`;
            deliveryEl.classList.remove('unlocked');
        }
    }

    document.getElementById('cart-items-container').addEventListener('click', (e) => {
        let cart = readCart();
        const index = e.target.getAttribute('data-index');

        if (index === null) return;

        if (e.target.classList.contains('increase-qty')) {
            cart[index].quantity += 1;
        } else if (e.target.classList.contains('decrease-qty')) {
            cart[index].quantity -= 1;
            if (cart[index].quantity <= 0) {
                cart.splice(index, 1);
            }
        } else if (e.target.classList.contains('remove-item-btn')) {
            cart.splice(index, 1);
        }

        saveCart(cart);
        renderCart();
    });

    document.getElementById('clear-cart-btn').addEventListener('click', () => {
        saveCart([]);
        renderCart();
        toast('Cart cleared.');
    });

    document.getElementById('checkout-btn').addEventListener('click', () => {
        const cart = readCart();
        if (cart.length === 0) {
            toast('Your cart is empty!');
            return;
        }
        toast('Thank you! Checkout is switched off because Nestling is a fictional shop made for AI-GNITION 2026.');
    });

    renderCart();
});
