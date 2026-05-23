/* This updates the name of the dropdown button */

var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-menu .dropdown-item'))
dropdownElementList.map(function(dropdownItem) {
    dropdownItem.addEventListener('click', function(event) {
        var dropdownButton = event.target.closest('.dropdown').querySelector('.dropdown-toggle');
        dropdownButton.textContent = this.textContent;
    })
})


/* Upload profile picture */
