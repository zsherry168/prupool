const carpoolBuddies = {
    "Prudential Tower": [
        { name: "Alice Johnson", distance: "0.5 miles" },
        { name: "Bob Smith", distance: "0.7 miles" },
    ],
    "Prudential Insurance Company of America - Washington Building": [
        { name: "Carol Davis", distance: "0.3 miles" },
        { name: "David Brown", distance: "0.8 miles" },
    ],
    "Prudential Headquarters - Plaza Building": [
        { name: "Eva Wilson", distance: "0.4 miles" },
        { name: "Frank Miller", distance: "0.6 miles" },
    ]
};

document.addEventListener("DOMContentLoaded", function() {
    loadDropdownItems();
    
    const searchBar = document.getElementById("search-bar");
    if (searchBar) {
        searchBar.addEventListener("focus", toggleDropdown);
    }

    document.addEventListener("click", function(event) {
        const searchBar = document.getElementById("search-bar");
        const dropdown = document.getElementById("dropdown");
        const popup = document.getElementById("popup");

        if (!event.target.matches('#search-bar') && 
            !event.target.closest('#popup') && 
            !event.target.closest('#dropdown')) {
            if (popup) popup.style.display = "none";
            if (dropdown && !searchBar.contains(event.target)) {
                dropdown.style.display = "none";
            }
        }
    });
});

function toggleDropdown(event) {
    event.preventDefault();
    const dropdown = document.getElementById("dropdown");
    if (dropdown) {
      dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    }
  }

function loadDropdownItems() {
    const buildings = Object.keys(carpoolBuddies);
    const dropdown = document.getElementById("dropdown");
    dropdown.innerHTML = buildings.map(building => `<div class="dropdown-item" onclick="selectItem('${building}')">${building}</div>`).join('');
}

function showPopup(building) {
    const popup = document.getElementById("popup");
    const buddyList = document.getElementById("buddy-list");
    
    if (!popup || !buddyList) {
        console.error("Popup or buddy-list element not found");
        return;
    }

    const buddies = carpoolBuddies[building] || [];
    const buddyHTML = buddies.map(buddy => 
        `<div class="buddy-item">
            <span class="buddy-name">${buddy.name}</span>
            <span class="buddy-distance">${buddy.distance}</span>
         </div>`
    ).join('');
    
    buddyList.innerHTML = `
        <h4>Potential buddies near ${building}:</h4>
        ${buddyHTML}
    `;
    popup.style.display = "block";
}

function selectItem(building) {
    const searchBar = document.getElementById("search-bar");
    if (searchBar) {
        searchBar.value = building;
    }
    showPopup(building);
}