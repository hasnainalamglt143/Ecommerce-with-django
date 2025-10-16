document.addEventListener("DOMContentLoaded", function() {
const slider = document.getElementById("slider");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  let index = 0;
  const totalSlides = slider.children.length;

  function updateSlide() {
    slider.style.transform = `translateX(-${index * 100}%)`;
  }

  nextBtn.addEventListener("click", () => {
    // clearInterval(id)
    index = (index + 1) % totalSlides; // loop back to 0
    updateSlide();
  });

  prevBtn.addEventListener("click", () => {
        // clearInterval(id)

    index = (index - 1 + totalSlides) % totalSlides; // go backwards and loop
    updateSlide();
  });

  // Optional: Auto-slide every 4s
  let id=setInterval(() => {
    index = (index + 1) % totalSlides;
    updateSlide();
  }, 4000);

})