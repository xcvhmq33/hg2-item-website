const API_BASE = "http://127.0.0.1:8000/api/v1/items";
let currentPage = 1;
const itemsPerPage = 96;

function changePage(direction) {
    currentPage += direction;
    if (currentPage < 1) {
        currentPage = 1;
        updatePagination()
    } else {
        loadItems(currentPage);
    }
    const inputer = document.getElementById('page-input');
    inputer.value = currentPage;
}

function jumpToPage(event) {
    const pageNumber = parseInt(event.target.value, 10);
    if (!isNaN(pageNumber) && pageNumber > 0) {
        currentPage = pageNumber - 1;
        loadItems(currentPage);
    } else {
        event.target.value = currentPage + 1;
    }
}

async function loadItems(page) {
    const response = await fetch(`${API_BASE}/?skip=${(page-1) * itemsPerPage}&limit=${itemsPerPage}`);
    const items = await response.json();
    renderItems(items.data);
}

function renderItems(items) {
    const container = document.getElementById('items-container');
    container.innerHTML = '';

    if (items.length === 0) {
        container.innerHTML = '<p>No items found.</p>';
        updatePagination();
        return;
    }

    items.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('item');
        itemDiv.innerHTML = `
        <img src="${item.image_url}" alt="${item.title}" style="width: 100%; height: auto;">
        <h3>${item.title}</h3>
        `;
        itemDiv.addEventListener('click', () => showItemDetails(item.ingame_id));
        container.appendChild(itemDiv);
    });

    updatePagination();
}

async function showItemDetails(itemId) {
    const response = await fetch(`${API_BASE}/${itemId}`);
    const item = await response.json();
    alert(`
        Title: ${item.title}
        Rarity: ${item.rarity}
        Damage Type: ${item.damage_type || 'None'}
    `);
}

function updatePagination() {
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');

    prevButton.disabled = (currentPage === 1);
    nextButton.disabled = false;
}

document.addEventListener('DOMContentLoaded', () => {
    loadItems(currentPage);
});
