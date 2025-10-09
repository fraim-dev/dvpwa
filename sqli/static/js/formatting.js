function escapeHTML(str) {
    return str.replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#39;');
}

function displayUserInfo(userData) {
    var userInfoElem = document.getElementById('user-info');
    userInfoElem.textContent = userData;
}

function displaySearchResults(query, results) {
    var searchDiv = document.getElementById('search-results');
    searchDiv.innerHTML = '';
    var header = document.createElement('h3');
    header.textContent = 'Search results for: ' + query;
    searchDiv.appendChild(header);

    results.forEach(function(result) {
        var itemDiv = document.createElement('div');
        itemDiv.className = 'result-item';
        itemDiv.textContent = result.name;
        searchDiv.appendChild(itemDiv);
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
