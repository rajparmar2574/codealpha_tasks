// ── CSRF helper ──────────────────────────────────────────────────────────────
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ── TOAST ─────────────────────────────────────────────────────────────────────
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = 'toast';
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  toast.innerHTML = `<span>${icons[type] || '📢'}</span> ${message}`;
  container.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(20px)'; toast.style.transition = 'all 0.3s'; setTimeout(() => toast.remove(), 300); }, 3000);
}

// ── ADD TO CART (AJAX) ────────────────────────────────────────────────────────
document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    const productId = btn.dataset.productId;
    const quantity = document.getElementById('qty-input') ? parseInt(document.getElementById('qty-input').value) : 1;
    btn.textContent = '⏳';
    try {
      const res = await fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `quantity=${quantity}`
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        document.querySelectorAll('.cart-badge').forEach(b => b.textContent = data.cart_count);
        btn.textContent = '✅ Added';
        setTimeout(() => btn.textContent = '🛒 Add to Cart', 2000);
      }
    } catch (err) {
      showToast('Please login to add to cart', 'error');
      btn.textContent = '🛒 Add to Cart';
    }
  });
});

// ── QUANTITY CONTROLS ─────────────────────────────────────────────────────────
const qtyInput = document.getElementById('qty-input');
document.querySelectorAll('.qty-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (!qtyInput) return;
    let val = parseInt(qtyInput.value);
    if (btn.dataset.action === 'inc') val = Math.min(val + 1, 99);
    if (btn.dataset.action === 'dec') val = Math.max(val - 1, 1);
    qtyInput.value = val;
  });
});

// ── CART QUANTITY UPDATE (AJAX) ───────────────────────────────────────────────
document.querySelectorAll('.cart-qty-update').forEach(btn => {
  btn.addEventListener('click', async () => {
    const itemId = btn.dataset.itemId;
    const action = btn.dataset.action;
    const qtyEl = document.getElementById(`qty-${itemId}`);
    let qty = parseInt(qtyEl?.textContent || 1);
    if (action === 'inc') qty += 1;
    if (action === 'dec') qty = Math.max(qty - 1, 0);

    try {
      const res = await fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `quantity=${qty}`
      });
      const data = await res.json();
      if (data.success) {
        if (qty === 0) {
          document.getElementById(`cart-row-${itemId}`)?.remove();
        } else {
          if (qtyEl) qtyEl.textContent = qty;
          const subtotalEl = document.getElementById(`subtotal-${itemId}`);
          // update cart total
        }
        document.querySelectorAll('.cart-badge').forEach(b => b.textContent = data.cart_count);
        document.querySelectorAll('.cart-total-display').forEach(el => el.textContent = `₹${data.cart_total.toFixed(2)}`);
      }
    } catch (err) { console.error(err); }
  });
});

// ── REMOVE FROM CART ─────────────────────────────────────────────────────────
document.querySelectorAll('.cart-remove-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const itemId = btn.dataset.itemId;
    if (!confirm('Remove this item?')) return;
    try {
      const res = await fetch(`/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded' },
        body: ''
      });
      const data = await res.json();
      if (data.success) {
        document.getElementById(`cart-row-${itemId}`)?.remove();
        document.querySelectorAll('.cart-badge').forEach(b => b.textContent = data.cart_count);
        document.querySelectorAll('.cart-total-display').forEach(el => el.textContent = `₹${data.cart_total.toFixed(2)}`);
        showToast('Item removed from cart', 'info');
      }
    } catch (err) { console.error(err); }
  });
});

// ── PASSWORD STRENGTH ────────────────────────────────────────────────────────
const pwdInput = document.getElementById('id_password');
const pwdStrength = document.getElementById('pwd-strength');
if (pwdInput && pwdStrength) {
  pwdInput.addEventListener('input', () => {
    const val = pwdInput.value;
    let strength = 0;
    if (val.length >= 6) strength++;
    if (/[A-Z]/.test(val)) strength++;
    if (/[0-9]/.test(val)) strength++;
    if (/[^A-Za-z0-9]/.test(val)) strength++;
    const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
    const colors = ['', '#ff5c5c', '#f0a853', '#60a5fa', '#4ecb71'];
    pwdStrength.textContent = labels[strength] || '';
    pwdStrength.style.color = colors[strength] || '';
  });
}

// ── PAYMENT OPTION HIGHLIGHT ─────────────────────────────────────────────────
document.querySelectorAll('.payment-option input[type=radio]').forEach(radio => {
  radio.addEventListener('change', () => {
    document.querySelectorAll('.payment-option').forEach(opt => opt.classList.remove('selected'));
    radio.closest('.payment-option').classList.add('selected');
  });
});

// ── AUTO-DISMISS MESSAGES ────────────────────────────────────────────────────
setTimeout(() => {
  document.querySelectorAll('.message').forEach(m => {
    m.style.transition = 'all 0.4s';
    m.style.opacity = '0';
    m.style.maxHeight = '0';
    setTimeout(() => m.remove(), 400);
  });
}, 4000);
