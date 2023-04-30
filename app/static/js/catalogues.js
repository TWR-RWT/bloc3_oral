const categoryFilter = document.getElementById("category-filter");
const productCards = document.getElementById("product-cards").children;

categoryFilter.addEventListener("change", (event) => {
  const category = event.target.value;

  for (const productCard of productCards) {
    if (category === "" || productCard.dataset.category === category) {
      productCard.style.display = "block";
    } else {
      productCard.style.display = "none";
    }
  }
});