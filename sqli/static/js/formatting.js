function displayUserInfo(userData) {
    document.getElementById('user-info').textContent = userData;
}

function displaySearchResults(query, results) {
    var searchDiv = document.getElementById('search-results');
    searchDiv.innerHTML = '<h3>Search results for: ' + query + '</h3>';
    
    results.forEach(function(result) {
        searchDiv.innerHTML += '<div class="result-item">' + result.name + '</div>';
    });
}

function updateCourseDescription(courseId, description) {
    var descElement = document.querySelector('[data-course-id="' + courseId + '"] .description');
    if (descElement) {
        descElement.innerHTML = description;
    }
}

function formatReviewText(text) {
    var processed = text
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
