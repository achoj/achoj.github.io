

document.addEventListener("DOMContentLoaded", function() {
    const posts = document.querySelectorAll(".post");
    posts.forEach(post => {
        post.addEventListener("click", function() {
            const path = this.getAttribute("data-path");
            window.location.href = "post.html?path=" + encodeURIComponent(path);
        });
    });
});