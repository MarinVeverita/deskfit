import Sortable from 'sortablejs/modular/sortable.complete.esm.js';

(function() {
function returnOptions(day) {
    let options = {
        group: {
            name: 'shared',
            put: true
        },
        animation: 150,
        ghostClass: 'blue-background-class',
        draggable: '.list-group-item',
        onAdd: function(evt) {
            let item = evt.item
            if (item.childNodes.length < 2) {
                let removeButton = document.createElement('button');

                let removeSpan = document.createElement('span');
                removeSpan.className = 'material-icons';
                removeSpan.textContent = 'delete_forever';
            
                removeButton.classList = 'remove-workout btn';
                removeButton.appendChild(removeSpan)
                removeButton.onclick = () => {
                    item.parentNode.removeChild(item);
                    updatePutOption(day);
                };
                item.appendChild(removeButton);
            };
            updatePutOption(day);
        },
        onRemove: function() {
            updatePutOption(day);
        }
    }
    return options;
}

function updatePutOption(day) {
    let list = document.getElementById(day);
    let items = list.querySelectorAll('.list-group-item');

    daysSortable[day][1].group.put = items.length > 0 ? false : true;
    
    checkForErrors()
}

function updateSortable(day) {
    daysSortable[day][0].destroy();
    daysSortable[day][0] = new Sortable(document.getElementById(day), daysSortable[day][1]);
}

function checkForErrors() {
    let entries = Object.entries(daysSortable);

    entries.forEach(day => {
        let dayName = day[0];
        let dayOptions = day[1][1]

        let list = document.getElementById(dayName);
        let items = list.querySelectorAll('.list-group-item');

        if (dayOptions.group.put == true && items.length > 0) {
            console.error(dayName);
            console.error('error 1');

            dayOptions.group.put = false
        }
        else if (dayOptions.group.put == false && items.length == 0) {
            console.error(dayName)
            console.error('error 2');

            dayOptions.group.put = true
        }
        updateSortable(dayName)
    });
    
}

let daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

let daysSortable = {};

daysOfWeek.forEach(day => {
    let options = returnOptions(day);
    let sortable = new Sortable(document.getElementById(day), options);
    daysSortable[day] = [sortable, options];
});

var workoutSortable = new Sortable(document.getElementById('example2Left'), {
    group: {
        name: 'shared',
        pull: 'clone',
        put: false
    },
    animation: 150,
    ghostClass: 'blue-background-class',
    draggable: ".list-group-item",
});
})();
