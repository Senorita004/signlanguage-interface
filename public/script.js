let interval

function makeApiCall(formData) {
  var selectedModel = document.getElementById('modelSelect').value;
  formData.append('model', selectedModel);

  const startTime = performance.now();

  fetch('http://127.0.0.1:8000/predict', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      const endTime = performance.now();

      const duration = endTime - startTime;
      var speech = new SpeechSynthesisUtterance(data?.predicted_value ?? "Not found");
      window.speechSynthesis.speak(speech);
      document.getElementById('predictionResult').innerText = 'Prediction: ' + JSON.stringify(data) + '\nResponse Time: ' + duration + ' ms';
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

document.getElementById('imageInput').onchange = function (event) {
  if (interval) {
    clearInterval(interval)
  }
  var image = document.getElementById('selectedImage');
  image.src = URL.createObjectURL(event.target.files[0]);
  image.hidden = false;
  document.getElementById('predictionResult').innerText = ''
};

document.getElementById('modelSelect').onchange = function (event) {
  if (interval) {
    clearInterval(interval)
  }
  document.getElementById('predictionResult').innerText = ''
}

document.getElementById('predictButton').onclick = function () {
  if (interval) {
    clearInterval(interval)
  }
  var imageInput = document.getElementById('imageInput').files[0];
  var formData = new FormData();
  formData.append('file', imageInput);

  makeApiCall(formData)
};

document.getElementById('enableCamera').onclick = function () {
  if (interval) {
    clearInterval(interval)
  }
  document.getElementById('cameraSection').style.display = 'block'
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function (stream) {
        document.getElementById('cameraFeed').srcObject = stream;
      })
      .catch(function (error) {
        console.log("Something went wrong!");
      });
  }
}

document.getElementById('stopCapturing').onclick = function () {
  if (interval) {
    clearInterval(interval)
  }
  document.getElementById('cameraSection').style.display = 'none'
}

document.getElementById('captureButton').onclick = function () {
  if (interval) {
    clearInterval(interval)
  }
  interval = setInterval(() => {
    var canvas = document.createElement('canvas');
    canvas.width = 640;
    canvas.height = 480;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(document.getElementById('cameraFeed'), 0, 0, 640, 480);


    var image = document.getElementById('selectedImage');
    image.src = canvas.toDataURL('image/jpeg');
    image.hidden = false;

    // Convert the canvas to a blob and send it for prediction
    canvas.toBlob(function (blob) {
      var formData = new FormData();
      formData.append('file', blob, 'capture.jpg');

      makeApiCall(formData)
    }, 'image/jpeg');
  }, 1000);
};