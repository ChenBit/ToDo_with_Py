// 初始化加载待办事项
window.addEventListener('DOMContentLoaded', async () => {
    const res = await fetch('/todos');
    (await res.json()).forEach(todo => createTodoElement(todo));
});

async function addTodo() {
    const input = document.getElementById('todoInput');
    const content = input.value.trim();
    
    if (content) {
        const res = await fetch('/add', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ content })
        });
        createTodoElement(await res.json());
        input.value = '';
    }
}

function createTodoElement(todo) {
    const li = document.createElement('li');
    li.innerHTML = `
        <span>${todo.content}</span>
        <button class="delete-btn" onclick="deleteTodo('${todo.time}')">删除</button>
    `;
    document.getElementById('todoList').appendChild(li);
}

async function deleteTodo(time) {
    await fetch(`/delete`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ time })
    });
    document.querySelectorAll('li').forEach(li => {
        if (li.querySelector('button').onclick.toString().includes(time)) li.remove()
    });
}

function checkEnter(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        addTodo();
    }
}
