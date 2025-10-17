document.addEventListener("DOMContentLoaded",()=>{


let domain = window.location.origin;

    // This is your test publishable API key.
const stripe = Stripe("pk_test_51SAEjNA3TUrmlb8qtv5idsHdB3ehfK45bzvhepINv6k2cZ2C5hJI46OARRCJC3HR4JOtHuC1QJSNy7GIBwE40MA800RJDTe3Vn");

initialize();

// Create a Checkout Session
async function initialize() {
  const fetchClientSecret = async () => {
    const response = await fetch(`${domain}/payment/create-checkout-session/`, {
      method: "POST",
       headers: {
                "X-CSRFToken": csrftoken
            },
    });
    let res=await response.json()
    let { clientSecret } = res;
    console.log("response",response)

    return clientSecret;
  };

  const checkout = await stripe.initEmbeddedCheckout({
    fetchClientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}
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

})