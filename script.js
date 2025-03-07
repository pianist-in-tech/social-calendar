document.addEventListener("DOMContentLoaded", () => {
    fetchPosts();
    document.getElementById('postForm').addEventListener('submit', addPost);
});

function fetchPosts(){
    fetch('http://127.0.0.1:5000/posts')
    .then(res => res.json())
    .then(data => {
        let calendar = document.getElementById('calendar');
        calendar.innerHTML = '';
        data.forEach(post => {
            let postDiv = document.createElement('div');
            postDiv.innerHTML = `${post.date} ${post.time} - ${post.content} <button onclick='deletePost(${post.id})'>X</button>`;
            calendar.appendChild(postDiv);
        });
    });
}
