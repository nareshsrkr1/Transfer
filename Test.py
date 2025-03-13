/* Move Business Segments section slightly to the left */
.business-segments-container {
    margin-left: -20px; /* Adjust as needed */
}

/* Add space between dropdown and search box */
.segment-row, .override-row {
    display: flex;
    align-items: center;
    gap: 10px; /* Controls space between dropdown, search box, and buttons */
}

/* Ensure both sections have uniform spacing */
.dropdown-container {
    min-width: 150px; /* Adjust dropdown width */
}

/* Adjust search box size when both Add and Remove buttons exist */
.segment-row:last-child .search-box,
.override-row:last-child .search-box {
    width: calc(100% - 75px); /* Reduce width if Add button exists */
}

/* Center the Submit and Reset buttons */
.row.justify-content-center {
    text-align: center;
}
