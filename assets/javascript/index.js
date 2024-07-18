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
            handleOnAdd(evt, day);
        },
        onRemove: function(evt) {
            const csrfToken = getCSRFToken();
            const dayOfWeek = day[0].toUpperCase() + day.substring(1);
            $.ajax({
                url: `/planned_workouts/1/`,
                type: 'DELETE',       
                headers: {'X-CSRFToken': csrfToken},
                data: { 
                    day: dayOfWeek, 
                },
                success: function(data) {
                    console.log('Workout removed successfully:', data);
                },
                error: function(error) {
                    console.error('Error removing workout:', error);
                }
            });


            updatePutOption(day);
        }
    }
    return options;
}


function handleOnAdd(evt, day, flag=false) {
    if (!flag) {
        const csrfToken = getCSRFToken();
        const dayOfWeek = day[0].toUpperCase() + day.substring(1);
        const workoutId = evt.item.getAttribute('data-id').substring(8);
        
        $.ajax({
            url: '/planned_workouts/',
            type: 'POST',
            headers: {'X-CSRFToken': csrfToken},
            contentType: "application/json",
            data: JSON.stringify({ 
                day_of_week: dayOfWeek, 
                workout: workoutId
            }),
            
            
            success: function(data) {
                console.log('Success:', data);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }
    

    let item = evt.item;
    if (item.querySelector('.remove-workout') === null) {
        let removeButton = document.createElement('button');

        let removeSpan = document.createElement('span');
        removeSpan.className = 'material-icons';
        removeSpan.textContent = 'delete_forever';
    
        removeButton.classList = 'remove-workout btn';
        removeButton.appendChild(removeSpan);
        removeButton.onclick = () => {
            item.parentNode.removeChild(item);
            updatePutOption(day);

            const csrfToken = getCSRFToken();
            const dayOfWeek = day[0].toUpperCase() + day.substring(1);
            const workoutId = evt.item.getAttribute('data-id').substring(8);
            $.ajax({
                url: `/planned_workouts/1/`,
                type: 'DELETE',       
                headers: {'X-CSRFToken': csrfToken},
                data: { 
                    day: dayOfWeek, 
                },
                success: function(data) {
                    console.log('Workout removed successfully:', data);
                },
                error: function(error) {
                    console.error('Error removing workout:', error);
                }
            });

        };
        item.appendChild(removeButton);
    };
    updatePutOption(day);
}




function updatePutOption(day) {
    console.log(day)
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
            //console.error(dayName);
            //console.error('error 1');

            dayOptions.group.put = false
        }
        else if (dayOptions.group.put == false && items.length == 0) {
            //console.error(dayName)
            //console.error('error 2');

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



let difficulty_map = {
    'beginner': 1,
    'intermediate': 2,
    'expert': 3
};

$.ajax({
url: '/planned_workouts/week-plan',
type: 'GET',

success: function(data) {
    for (let day in data) {
      let element = data[day]
      if (data[day] !== null) {
    let exercises = data[day]['exercises']

    
  let difficulty_sum = 0;

  let muscle_groups = [];

  exercises.forEach(exercise_workout => {
    difficulty_sum += difficulty_map[exercise_workout['exercise'].difficulty] 
    
    if (!muscle_groups.includes(exercise_workout['exercise'].muscle)) {
      muscle_groups.push(exercise_workout['exercise'].muscle);
    }
  });

  let difficulty_avg_number = difficulty_sum / exercises.length

  let difficulty_avg;
  if (difficulty_avg_number < 1.5) {
    difficulty_avg = 'beginner';
  } else if (difficulty_avg_number <2.5) {
    difficulty_avg = 'intermediate';
  } else {
    difficulty_avg = 'expert'
  }


  

        let workout_element = `
        <div class="list-group-item workout" data-id="workout_${element.id}">
          <h4 class="workout-name">${element.name}</h4>
          <p class="workout-muscle-groups">Muscle Groups: ${muscle_groups.join(', ')}</p>
          <p class="workout-difficulty">Difficulty: ${difficulty_avg}</p>
        </div>
      `;
        
        
      let day_element = $(`#${day[0].toLowerCase() + day.substring(1)}`).append(workout_element);
      
      handleOnAdd({ item: day_element[0].lastElementChild }, day[0].toLowerCase() + day.substring(1), true);
  
        
}
}
},
error: function(error) {
    console.error('Error:', error);
}
});
})();