document.addEventListener('DOMContentLoaded', (event) => {
    const calculateLabelsButton = document.getElementById('calculateLabels');
    const loadModelButton = document.getElementById('loadModel');

    calculateLabelsButton.addEventListener('click', calculateLabels);
    loadModelButton.addEventListener('click', loadModel);
});

function calculateLabels() {
    inputValue = document.getElementById('calculateLabelsInput').value;
    axios.post('/api/calculateLabels', {inputText: inputValue}, {
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(function (response) {
            document.getElementById('calculateLabelsOutput').value = response.data;
        })
        .catch(function (error) {
            console.log(error);
        });
}

function loadModel() {
    axios.get('/api/loadModel')
        .then(function (response) {
            document.getElementById('loadModelOutput').value = response.data;
        })
        .catch(function (error) {
            console.log(error);
        });
    document.getElementById('loadModelOutput').value = "Model is loading...";
}