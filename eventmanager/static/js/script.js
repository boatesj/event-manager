document.addEventListener('DOMContentLoaded', function() {
    // sidenav initialization
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

   
    // Initialize select elements and datepicker
document.addEventListener('DOMContentLoaded', function() {
    // Initialize select elements
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);

    // Initialize datepicker
    var dateElems = document.querySelectorAll('.datepicker');
    var dateInstances = M.Datepicker.init(dateElems, {
        format: 'dd-mm-yyyy',  // Set your desired format
    });
});


    // select initialization
    let selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);

    // collapsible initialization
    let collapsibles = document.querySelectorAll('.collapsible');
    M.Collapsible.init(collapsibles);
});


    document.querySelector('form').addEventListener('submit', function(event) {
        const dateInput = document.getElementById('date');
        let dateValue = dateInput.value;

        // Perform client-side validation here if needed

        // Optionally: Modify the input value to fit the desired format before submission
        // Example: If users enter in ISO format, convert it to dd-mm-yyyy HH:MM format
    });

