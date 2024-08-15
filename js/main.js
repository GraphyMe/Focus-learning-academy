document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'Shimaa Robaa' && password === 'controlpanel') {
        window.location.href = 'controlpanel.html';
    } else if (password === 'Focus2024') {
        window.location.href = `dashboard.html?student=${username}`;
    } else {
        document.getElementById('loginMessage').textContent = 'Invalid credentials, please try again.';
    }
});

function addStudent(name, password) {
    const students = JSON.parse(localStorage.getItem('students')) || {};
    students[name] = { password: password, assignments: [], feedback: "" };
    localStorage.setItem('students', JSON.stringify(students));
}

function getStudent(name) {
    const students = JSON.parse(localStorage.getItem('students')) || {};
    return students[name];
}

function deleteStudent(name) {
    const students = JSON.parse(localStorage.getItem('students')) || {};
    delete students[name];
    localStorage.setItem('students', JSON.stringify(students));
}

function editStudent(name, newInfo) {
    const students = JSON.parse(localStorage.getItem('students')) || {};
    students[name] = { ...students[name], ...newInfo };
    localStorage.setItem('students', JSON.stringify(students));
}

function addAssignment(name, assignment) {
    const students = JSON.parse(localStorage.getItem('students')) || {};
    if (students[name]) {
        students[name].assignments.push(assignment);
        localStorage.setItem('students', JSON.stringify(students));
    }
}

function addFeedback(name, feedback) {
    const students = JSON.parse(localStorage.getItem('students')) || {};
    if (students[name]) {
        students[name].feedback = feedback;
        localStorage.setItem('students', JSON.stringify(students));
    }
}
