function createTable(element, cols, rows) {
    var table = document.createElement('table');

    for (var i = 0; i < rows; i++) {
        var tr = document.createElement('tr');

        for (j = 0; j < cols; j++) {
            var td = document.createElement('td');
            td.innerHTML
            tr.appendChild(td);
        }

        table.appendChild(tr);
    }
    element.appendChild(table);
}

var elem = document.querySelector('#table');
var cols = 
createTable(elem, cols, 6)

/*
*/