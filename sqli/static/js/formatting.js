function displayUserInfo(userData) {
    document.getElementById('user-info').textContent = userData;
}

function escapeHTML(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function displaySearchResults(query, results) {
    var searchDiv = document.getElementById('search-results');
    searchDiv.innerHTML = '<h3>Search results for: ' + escapeHTML(query) + '</h3>';
    
    results.forEach(function(result) {
        searchDiv.innerHTML += '<div class="result-item">' + escapeHTML(result.name) + '</div>';
    });
}

function updateCourseDescription(courseId, description) {
    var descElement = document.querySelector('[data-course-id="' + courseId + '"] .description');
    if (descElement) {
        descElement.textContent = description;
    }
}

function formatReviewText(text) {
    var escaped = escapeHTML(text);
    var processed = escaped
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
    
    return processed;
}

document.addEventListener('DOMContentLoaded', function() {
    var userData = window.userData || '';
    if (userData) {
        displayUserInfo(userData);
    }
});
