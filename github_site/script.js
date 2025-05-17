const API_BASE = window.API_BASE || '';

function uploadToServer(file) {
    const formData = new FormData();
    formData.append('file', file);
    return fetch(`${API_BASE}/api/dirichlet`, { method: 'POST', body: formData })
        .then(r => r.json());
}

document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const file = document.getElementById('csv-file').files[0];
    if (!file) {
        alert('Please choose a CSV file.');
        return;
    }
    uploadToServer(file).then(showChart);
});

function loadSample(name) {
    fetch(`samples/${name}`)
        .then(r => r.text())
        .then(text => new Blob([text], { type: 'text/csv' }))
        .then(uploadToServer)
        .then(showChart);
}

function showChart(data) {
    const priors = data.priors || [];
    const width = 500,
        height = 300,
        margin = { top: 20, right: 20, bottom: 30, left: 40 };

    d3.select('#chart').select('svg').remove();

    const svg = d3.select('#chart').append('svg')
        .attr('width', width)
        .attr('height', height);

    const x = d3.scaleBand().domain(d3.range(priors.length))
        .range([margin.left, width - margin.right]).padding(0.1);
    const y = d3.scaleLinear().domain([0, d3.max(priors)]).nice()
        .range([height - margin.bottom, margin.top]);

    svg.append('g')
        .selectAll('rect')
        .data(priors)
        .enter().append('rect')
        .attr('x', (d, i) => x(i))
        .attr('y', d => y(d))
        .attr('height', d => y(0) - y(d))
        .attr('width', x.bandwidth())
        .attr('fill', '#69b3a2');

    svg.append('g')
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).tickFormat(i => i + 1));

    svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));
}
