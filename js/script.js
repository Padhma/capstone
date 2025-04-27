let currentPage = 1;
const productsPerPage = 12;
let allProducts = [];

fetch('../data/laptops.json')
  .then(response => response.json())
  .then(products => {
    allProducts = products;
    renderPage(currentPage);
    setupPagination();
  })
  .catch(error => console.error('Error loading JSON:', error));

function renderPage(page) {
  const container = document.getElementById('product-list');
  container.innerHTML = '';

  const start = (page - 1) * productsPerPage;
  const end = start + productsPerPage;
  const paginatedProducts = allProducts.slice(start, end);

  paginatedProducts.forEach(product => {
    const productHTML = `
      <a href="../pages/products.html?product=${encodeURIComponent(product.name)}" class="product">
        <img src="../assets/images/laptop.jpg" alt="Product Image" />
        <h3>${product.name}</h3>
        <p><strong>Price: </strong>${product.price}</p>
      </a>
    `;
    container.innerHTML += productHTML;
  });
}

function setupPagination() {
  const paginationContainer = document.getElementById('pagination');
  const totalPages = Math.ceil(allProducts.length / productsPerPage);

  paginationContainer.innerHTML = `
    <button id="prevBtn">Previous</button>
    <span id="pageIndicator">${currentPage} / ${totalPages}</span>
    <button id="nextBtn">Next</button>
  `;

  document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      renderPage(currentPage);
      updatePageIndicator(totalPages);
    }
  });

  document.getElementById('nextBtn').addEventListener('click', () => {
    if (currentPage < totalPages) {
      currentPage++;
      renderPage(currentPage);
      updatePageIndicator(totalPages);
    }
  });
}

function updatePageIndicator(totalPages) {
  document.getElementById('pageIndicator').textContent = `${currentPage} / ${totalPages}`;
}
