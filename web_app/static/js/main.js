function openNav() {
  const sidenav = document.getElementById("mySidenav");
  const overlay = document.getElementById("cartOverlay");

  if (!sidenav || !overlay) return;

  sidenav.classList.add("open");
  overlay.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeNav() {
  const sidenav = document.getElementById("mySidenav");
  const overlay = document.getElementById("cartOverlay");

  if (!sidenav || !overlay) return;

  sidenav.classList.remove("open");
  overlay.classList.remove("active");
  document.body.style.overflow = "";
}

function formSwitch() {
  const logForm = document.getElementById("logForm");
  const regForm = document.getElementById("regForm");
  const formControl = document.getElementById("formControl");

  if (!logForm || !regForm || !formControl) return;

  const loginIsVisible = logForm.style.display !== "none";

  if (loginIsVisible) {
    logForm.style.display = "none";
    regForm.style.display = "block";
    formControl.textContent = "Already have an account? Sign In";
  } else {
    logForm.style.display = "block";
    regForm.style.display = "none";
    formControl.textContent = "Need an account? Register";
  }
}

/* CHECKOUT TOTALS */
function formatMoney(amount) {
  return Number(amount || 0).toFixed(2);
}

function getMoneyFromDataset(value) {
  return parseFloat(String(value || "0").replace(/[^0-9.]/g, "")) || 0;
}

function updateCheckoutTotals(tipPercent = null) {
  const totalsBox = document.getElementById("checkoutTotals");
  if (!totalsBox) return;

  const subtotal = getMoneyFromDataset(totalsBox.dataset.subtotal);
  const backendTax = getMoneyFromDataset(totalsBox.dataset.tax);
  const serviceFee = subtotal > 0 ? 1.99 : 0;

  const customTipInput = document.getElementById("customTipInput");
  const customTip = parseFloat(customTipInput?.value || "0");

  let tipAmount = 0;

  if (customTip > 0) {
    tipAmount = customTip;
  } else if (tipPercent !== null) {
    tipAmount = subtotal * (tipPercent / 100);
  } else {
    const activeTip = document.querySelector(".tip-btn.active");
    const activePercent = parseFloat(activeTip?.dataset.tip || "0");
    tipAmount = subtotal * (activePercent / 100);
  }

  const finalTotal = subtotal + backendTax + serviceFee + tipAmount;

  const subtotalDisplay = document.getElementById("subtotalDisplay");
  const taxAmount = document.getElementById("taxAmount");
  const serviceFeeDisplay = document.getElementById("serviceFee");
  const tipAmountDisplay = document.getElementById("tipAmount");
  const finalTotalDisplay = document.getElementById("finalTotal");

  if (subtotalDisplay) subtotalDisplay.textContent = formatMoney(subtotal);
  if (taxAmount) taxAmount.textContent = formatMoney(backendTax);
  if (serviceFeeDisplay) serviceFeeDisplay.textContent = formatMoney(serviceFee);
  if (tipAmountDisplay) tipAmountDisplay.textContent = formatMoney(tipAmount);
  if (finalTotalDisplay) finalTotalDisplay.textContent = formatMoney(finalTotal);

  const tipAmountInput = document.getElementById("tipAmountInput");
  const finalTotalInput = document.getElementById("finalTotalInput");

  if (tipAmountInput) tipAmountInput.value = formatMoney(tipAmount);
  if (finalTotalInput) finalTotalInput.value = formatMoney(finalTotal);
}

function setupTipButtons() {
  const tipButtons = document.querySelectorAll(".tip-btn");
  const customTipInput = document.getElementById("customTipInput");

  if (!tipButtons.length) return;

  tipButtons.forEach((button) => {
    button.addEventListener("click", () => {
      tipButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");

      if (customTipInput) {
        customTipInput.value = "";
      }

      updateCheckoutTotals(parseFloat(button.dataset.tip || "0"));
    });
  });

  if (customTipInput) {
    customTipInput.addEventListener("input", () => {
      tipButtons.forEach((btn) => btn.classList.remove("active"));
      updateCheckoutTotals();
    });
  }
}

/* CHECKOUT VALIDATION */
function setFieldError(input, message) {
  const group = input.closest(".form-group");
  const small = group?.querySelector("small");

  if (!group) return;

  group.classList.remove("success");
  group.classList.add("error");

  if (small) small.textContent = message;
}

function setFieldSuccess(input) {
  const group = input.closest(".form-group");
  const small = group?.querySelector("small");

  if (!group) return;

  group.classList.remove("error");
  group.classList.add("success");

  if (small) small.textContent = "";
}

function validateCheckoutForm() {
  const form = document.getElementById("checkoutForm");
  const errorBox = document.getElementById("formErrorBox");

  if (!form) return true;

  let isValid = true;

  const firstName = form.querySelector('input[name="first_name"]');
  const lastName = form.querySelector('input[name="last_name"]');
  const email = form.querySelector('input[name="email"]');
  const phone = form.querySelector('input[name="phone"]');

  const fields = [firstName, lastName, email, phone].filter(Boolean);

  fields.forEach((field) => {
    const label = field.dataset.label || "This field";

    if (!field.value.trim()) {
      setFieldError(field, `${label} is required.`);
      isValid = false;
    } else {
      setFieldSuccess(field);
    }
  });

  if (email && email.value.trim()) {
    const emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());

    if (!emailIsValid) {
      setFieldError(email, "Enter a valid email address.");
      isValid = false;
    }
  }

  if (phone && phone.value.trim()) {
    const digits = phone.value.replace(/\D/g, "");

    if (digits.length < 10) {
      setFieldError(phone, "Enter a valid phone number.");
      isValid = false;
    }
  }

  if (errorBox) {
    if (!isValid) {
      errorBox.textContent =
        "Please fix the highlighted fields before placing your order.";
      errorBox.classList.add("show");
    } else {
      errorBox.textContent = "";
      errorBox.classList.remove("show");
    }
  }

  return isValid;
}

function setupCheckoutValidation() {
  const form = document.getElementById("checkoutForm");
  const phoneInput = document.getElementById("phoneInput");

  if (phoneInput) {
    phoneInput.addEventListener("input", () => {
      const digits = phoneInput.value.replace(/\D/g, "").slice(0, 10);

      if (digits.length <= 3) {
        phoneInput.value = digits;
      } else if (digits.length <= 6) {
        phoneInput.value = `${digits.slice(0, 3)}-${digits.slice(3)}`;
      } else {
        phoneInput.value = `${digits.slice(0, 3)}-${digits.slice(3, 6)}-${digits.slice(6)}`;
      }
    });
  }

  if (!form) return;

  form.addEventListener("submit", function (event) {
    const isValid = validateCheckoutForm();

    if (!isValid) {
      event.preventDefault();
    }
  });
}

/* ORDER PLACED POPUP */
function showOrderPlacedPopup() {
  const params = new URLSearchParams(window.location.search);

  if (params.get("order") !== "placed") return;

  const popup = document.createElement("div");
  popup.className = "order-popup";

  popup.innerHTML = `
    <div class="order-popup-card">
      <button type="button" class="order-popup-close">&times;</button>
      <div class="order-popup-icon">🍕</div>
      <h2>Order placed!</h2>
      <p>Your pizza order was received. We’ll start making it fresh.</p>
      <a href="/menu">Order More</a>
    </div>
  `;

  document.body.appendChild(popup);

  const closeButton = popup.querySelector(".order-popup-close");

  closeButton.addEventListener("click", () => {
    popup.remove();
    window.history.replaceState({}, document.title, window.location.pathname);
  });

  setTimeout(() => {
    if (document.body.contains(popup)) {
      popup.remove();
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, 5500);
}

/* AJAX ADD TO CART */
function showCartBanner(message = "Item added to cart!") {
  const oldBanner = document.querySelector(".cart-added-banner");
  if (oldBanner) oldBanner.remove();

  const banner = document.createElement("div");
  banner.className = "cart-added-banner";
  banner.textContent = message;

  const nav = document.querySelector(".site-nav");

  if (nav) {
    nav.insertAdjacentElement("afterend", banner);
  } else {
    document.body.prepend(banner);
  }

  setTimeout(() => banner.classList.add("show"), 20);

  setTimeout(() => {
    banner.classList.remove("show");
    setTimeout(() => banner.remove(), 250);
  }, 2500);
}

function updateCartCountFromResponse(data) {
  const cartLinks = document.querySelectorAll(".cart-link");

  cartLinks.forEach((link) => {
    link.textContent = `Cart (${data.cart_item})`;
  });
}

function setupAjaxAddToCart() {
  const forms = document.querySelectorAll('form[action^="/cart/add/"]');

  forms.forEach((form) => {
    form.addEventListener("submit", async function (event) {
      event.preventDefault();

      const button = form.querySelector("button[type='submit']");
      const originalText = button ? button.textContent : "";

      if (button) {
        button.disabled = true;
        button.textContent = "Adding...";
      }

      try {
        const response = await fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        if (!response.ok) {
          throw new Error("Cart request failed");
        }

        const data = await response.json();

        updateCartCountFromResponse(data);
        showCartBanner("Item added to cart!");
      } catch (error) {
        showCartBanner("Could not add item. Try again.");
      } finally {
        if (button) {
          button.disabled = false;
          button.textContent = originalText;
        }
      }
    });
  });
}

/* INIT */
document.addEventListener("DOMContentLoaded", function () {
  setupTipButtons();
  setupCheckoutValidation();
  updateCheckoutTotals();
  showOrderPlacedPopup();
  setupAjaxAddToCart();
});

document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeNav();
  }
});