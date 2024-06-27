const carpoolBuddies = {
    "Prudential Tower": [
        { name: "Lata N. Reddy", distance: "0.5 miles away" },
        { name: "Ann Kappler", distance: "0.7 miles away" },
    ],
    "Washington Building": [
        { name: "Darshana Rao", distance: "0.3 miles away" },
        { name: "RJ Sala", distance: "0.8 miles away" },
    ],
    "Plaza Building": [
        { name: "Stacy Goodman", distance: "0.4 miles away" },
        { name: "Frank Miller", distance: "0.6 miles away" },
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

    const dropdown = document.querySelector('.custom-dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');
    const input = document.getElementById('days_going_to_work');
    const options = dropdownContent.querySelectorAll('div');

    dropdown.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    options.forEach(option => {
        option.addEventListener('click', function() {
            if (option.classList.contains('selected')) {
                option.classList.remove('selected');
            } else {
                option.classList.add('selected');
            }
            updateInputValue();
            dropdownContent.style.display = 'none';
        });
    });

    document.addEventListener('click', function() {
        dropdownContent.style.display = 'none';
    });

    function updateInputValue() {
        const selectedOptions = dropdownContent.querySelectorAll('.selected');
        const values = Array.from(selectedOptions).map(option => option.getAttribute('data-value'));
        input.value = values.join(', ');
    }

    // Initialize the dropdown with the current preferences
    const currentPreferences = input.value.split(', ').map(item => item.trim());
    options.forEach(option => {
        if (currentPreferences.includes(option.getAttribute('data-value'))) {
            option.classList.add('selected');
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