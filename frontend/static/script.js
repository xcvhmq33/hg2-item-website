let currentPage = 0;
const itemsPerPage = 96;

function changePage(direction) {
    currentPage += direction;
    loadItems(currentPage);
}

async function loadItems(page) {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/items?skip=${page * itemsPerPage}&limit=${itemsPerPage}`);
    const items = await response.json();
    renderItems(items);
}

function renderItems(items) {
    const container = document.getElementById('items-container');
    container.innerHTML = '';

    if (items.length === 0) {
        container.innerHTML = '<p>No items found.</p>';
        return;
    }

    items.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('item');
        itemDiv.innerHTML = `
            <img src="${item.image_url}" alt="${item.title}" style="width: 100%; height: auto;">
            <h3>${item.title}</h3>
        `;
        container.appendChild(itemDiv);
    });

    updatePagination();
}

function updatePagination() {
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');

    prevButton.disabled = currentPage === 0;
    nextButton.disabled = false;
}

document.addEventListener('DOMContentLoaded', () => {
    loadItems(currentPage);
});
