document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var file = document.getElementById('csv-file').files[0];
    if (!file) {
        alert('Please choose a CSV file.');
        return;
    }
    var formData = new FormData();
    formData.append('file', file);
    fetch('/api/dirichlet', { method: 'POST', body: formData })
        .then(r => r.json())
        .then(showChart);
});

function loadSample(name) {
    fetch('/static/samples/' + name)
        .then(r => r.text())
        .then(text => {
            var blob = new Blob([text], { type: 'text/csv' });
            var formData = new FormData();
            formData.append('file', blob, name);
            return fetch('/api/dirichlet', { method: 'POST', body: formData });
        })
        .then(r => r.json())
        .then(showChart);
}

function showChart(data) {
    var priors = data.priors || [];
    var width = 500,
        height = 300,
        margin = { top: 20, right: 20, bottom: 30, left: 40 };

    d3.select('#chart').select('svg').remove();

    var svg = d3.select('#chart').append('svg')
        .attr('width', width)
        .attr('height', height);

    var x = d3.scaleBand().domain(d3.range(priors.length))
        .range([margin.left, width - margin.right]).padding(0.1);
    var y = d3.scaleLinear().domain([0, d3.max(priors)]).nice()
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
