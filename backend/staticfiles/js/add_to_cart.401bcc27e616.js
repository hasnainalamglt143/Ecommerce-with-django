document.addEventListener("DOMContentLoaded", function() {
    const addToCartBtn = document.getElementById("add-to-cart-btn");
    const cartQuantitySpan = document.getElementById("cart_quantity");
    const successMessageDiv = document.getElementById("success_message");
    const messageContainer = document.getElementById("message-container");
    const totalAmountSpan = document.getElementById("total_amount");
    const subtotalSpan = document.getElementById("subtotal");
    // Handle ADD to cart

        if (addToCartBtn){
        addToCartBtn.addEventListener("click", function() {
            const productId = this.value;
            const quantityInput = document.querySelector("#quantity-input");
            const quantity = quantityInput.value;

            fetch("http://127.0.0.1:8000/cart/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            })
            .then(response => response.json())
            .then(data => {
                updateCartQuantity(data.cart_quantity);
                messageContainer.style.display = 'block';
                successMessageDiv.textContent = `Product "${data.product_name}" added to cart successfully!`;
                setTimeout(() => {
                    messageContainer.style.display = 'none';
                }, 3000);
            })
            .catch(error => console.error("Error:", error));
        });
    }

    

    // Handle UPDATE cart item
    document.querySelectorAll("button.update-btn").forEach(button => {
        button.addEventListener("click", function() {
            const cartItem = this.closest(".update-delete-btns-container"); // parent container
            const productId = cartItem.dataset.productId;
            const quantity = cartItem.querySelector(".quantity-input").value;
            console.log("Updating product ID:", productId, "to quantity:", quantity);
            fetch("http://127.0.0.1:8000/cart/update/", {
                method: "POST", // or PUT, depending on your backend
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            })
            .then(response => response.json())
            .then(data => {
                updateCartQuantity(data.cart_quantity);
                updateTotalAmounts(data.total_amount);
               
                messageContainer.style.display = 'block';
                successMessageDiv.textContent = `Cart updated for product "${data.product_name}"!`;
                setTimeout(() => {
                    messageContainer.style.display = 'none';
                }, 3000);
            })
            .catch(error => console.error("Error:", error));
        });
    });

    // Handle DELETE cart item
    // Handle DELETE cart item
document.querySelectorAll("button.delete-btn").forEach(button => {
    button.addEventListener("click", function() {
        const cartItem = this.closest(".update-delete-btns-container"); // parent container
        const productId = cartItem.dataset.productId;

        fetch("http://127.0.0.1:8000/cart/delete/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => response.json())
        .then(data => {
            updateCartQuantity(data.cart_quantity);
            updateTotalAmounts(data.total_amount);
            // ✅ Remove the deleted cart item from DOM
            cartItem.remove();

            // ✅ If cart becomes empty, show empty message
            const cartContainer = document.getElementById("cart-container");
            if (cartContainer.children.length === 0) {
                cartContainer.innerHTML = `
                  <div class="text-center py-20">
                      <svg class="w-10 h-10 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2 9m5-9v9m4-9v9m4-9l2 9"/>
                      </svg>
                      <h2 class="mt-4 text-xl font-semibold text-gray-700">Your cart is empty</h2>
                      <p class="text-gray-500">Looks like you haven’t added anything yet.</p>
                      <a href="/" class="mt-6 inline-block px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700">
                          Continue Shopping
                      </a>
                  </div>
                `;
            }

            // ✅ Optional toast
            messageContainer.style.display = 'block';
            successMessageDiv.textContent = `Item removed from cart!`;
            setTimeout(() => {
                messageContainer.style.display = 'none';
            }, 2000);
        })
        .catch(error => console.error("Error:", error));
    });
});


    // CSRF Helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function updateCartQuantity(newQuantity) {
        if (cartQuantitySpan) {
            cartQuantitySpan.textContent = newQuantity;
        }
    }

    function updateTotalAmounts(newTotal) {
        if (totalAmountSpan) {
            totalAmountSpan.textContent = `$${newTotal}`;
        }
        if (subtotalSpan) {
            subtotalSpan.textContent = `$${newTotal}`;
        }
    }
});
