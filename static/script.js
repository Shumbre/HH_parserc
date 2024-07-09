document.getElementById('searchForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const company = document.getElementById('company').value;

    fetch(`/search?title=${title}&company=${company}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>No results found</p>';
            } else {
                data.forEach(job => {
                    const jobDiv = document.createElement('div');
                    jobDiv.innerHTML = `
                        <h3>${job.title}</h3>
                        <p><a href="${job.url}" target="_blank">${job.url}</a></p>
                        <p>${job.company}</p>
                        <p>${job.description}</p>
                    `;
                    resultsDiv.appendChild(jobDiv);
                });
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
});
