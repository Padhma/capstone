const products = [];
for (let i = 1; i <= 20; i++) {
  products.push({
    name: `Product ${i}`,
    description: `Feature-rich gadget designed for performance and style. Product ID: ${i}`,
    price: `$${(Math.random() * 100 + 50).toFixed(2)}`,
    image: "https://via.placeholder.com/150"
  });
}

const container = document.getElementById('product-list');
products.forEach(product => {
  const productHTML = `
    <div class="product" data-type="product" data-name="${product.name}" data-price="${product.price}">
      <img src="${product.image}" alt="${product.name}" />
      <h3>${product.name}</h3>
      <p>${product.description}</p>
      <p><strong>${product.price}</strong></p>
    </div>
  `;
  container.innerHTML += productHTML;
});
