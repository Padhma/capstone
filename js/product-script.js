const urlParams = new URLSearchParams(window.location.search);
const productName = urlParams.get('product');

if (productName) {
  fetch('../data/laptops.json')  // Correct path to JSON
    .then(response => response.json())
    .then(products => {
      const product = products.find(p => p.name === productName);
      if (product) {
        document.getElementById('product-name').textContent = product.name;
        document.getElementById('product-price').textContent = product.price;
        document.getElementById('product-brand').textContent = product.metadata.brand;
        document.getElementById('product-screen').textContent = product.metadata.screen;
        document.getElementById('product-ram').textContent = product.metadata.ram;
        document.getElementById('product-ssd').textContent = product.metadata.ssd;
        document.getElementById('product-cpu').textContent = product.metadata.cpu;
        document.getElementById('product-gpu').textContent = product.metadata.gpu;
        document.getElementById('product-battery').textContent = product.metadata.battery;
        document.getElementById('product-weight').textContent = product.metadata.weight;
      } else {
        document.querySelector('.product-detail-container').innerHTML = '<p>Product not found.</p>';
      }
    })
    .catch(error => console.error('Error loading JSON:', error));
}