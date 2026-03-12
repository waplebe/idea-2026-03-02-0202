document.addEventListener('DOMContentLoaded', function() {
    const newTaskButton = document.getElementById('newTaskButton');
    const taskContainer = document.getElementById('taskContainer');

    // Fetch tasks from the API
    fetch('/tasks')
        .then(response => response.json())
        .then(tasks => {
            taskContainer.innerHTML = '';
            tasks.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.innerHTML = `
                    <p>${task.title} - ${task.description}</p>
                    <input type="checkbox" ${task.completed ? 'checked' : ''} data-id="${task.id}">
                    <button class="deleteButton" data-id="${task.id}">Delete</button>
                `;
                taskContainer.appendChild(taskElement);
            });
        })
        .catch(error => console.error('Error fetching tasks:', error));

    // Add new task
    newTaskButton.addEventListener('click', () => {
        const title = prompt('Enter task title:');
        const description = prompt('Enter task description:');

        if (title && description) {
            fetch('/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: title, description: description })
            })
            .then(response => response.json())
            .then(newTask => {
                alert(`Task created with ID: ${newTask.id}`);
                // Refresh the task list
                fetch('/tasks')
                    .then(response => response.json())
                    .then(tasks => {
                        taskContainer.innerHTML = '';
                        tasks.forEach(task => {
                            const taskElement = document.createElement('div');
                            taskElement.innerHTML = `
                                <p>${task.title} - ${task.description}</p>
                                <input type="checkbox" ${task.completed ? 'checked' : ''} data-id="${task.id}">
                                <button class="deleteButton" data-id="${task.id}">Delete</button>
                            `;
                            taskContainer.appendChild(taskElement);
                        });
                    });
            });
        }
    });

    // Delete task
    taskContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('deleteButton')) {
            const taskId = event.target.dataset.id;
            if (confirm('Are you sure you want to delete this task?')) {
                fetch(`/tasks/${taskId}`, {
                    method: 'DELETE'
                })
                .then(() => {
                    alert('Task deleted successfully.');
                    // Refresh the task list
                    fetch('/tasks')
                        .then(response => response.json())
                        .then(tasks => {
                            taskContainer.innerHTML = '';
                            tasks.forEach(task => {
                                const taskElement = document.createElement('div');
                                taskElement.innerHTML = `
                                    <p>${task.title} - ${task.description}</p>
                                    <input type="checkbox" ${task.completed ? 'checked' : ''} data-id="${task.id}">
                                    <button class="deleteButton" data-id="${task.id}">Delete</button>
                                `;
                                taskContainer.appendChild(taskElement);
                            });
                        });
                });
            }
        }
    });
});