document.addEventListener('DOMContentLoaded', function() {
    fetch('/products')
    .then(response => response.json())
    .then(data => {
        const productList = document.getElementById('product-list');
        data.forEach(product => {
            const productElement = document.createElement('div');
            productElement.innerHTML = `
                <h2>${product.product_name}</h2>
                <p>${product.description}</p>
                <p>Price: $${product.price}</p>
                <p>Stock: ${product.stock}</p>
                <button onclick="updateProduct(${product.product_id})">Update</button>
                <button onclick="deleteProduct(${product.product_id})">Delete</button>
            `;
            productList.appendChild(productElement);
        });
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('add-product-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);

    fetch('/products', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error('Error:', error));
});

function updateProduct(productId) {
    const newProductName = prompt("Enter new product name:");
    const newDescription = prompt("Enter new description:");
    const newPrice = prompt("Enter new price:");
    const newStock = prompt("Enter new stock:");

    fetch(`/products/${productId}`, {
        method: 'PUT',
        body: JSON.stringify({
            product_name: newProductName,
            description: newDescription,
            price: newPrice,
            stock: newStock
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error('Error:', error));
}

function deleteProduct(productId) {
    fetch(`/products/${productId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error('Error:', error));
}

