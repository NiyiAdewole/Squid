// Javasctript to handle table display and function

/* let prefers = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
let html = document.querySelector('html');
html.classList.add(prefers);
html.setAttribute('data-bs-theme', prefers); */
 
$(document).ready(function(){
    console.log("hit the table.js script");
    mine = $('#myTable').DataTable();
});

// let table = new DataTable('#myTable');