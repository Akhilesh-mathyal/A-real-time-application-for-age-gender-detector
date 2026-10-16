const video = document.querySelector('#video');
const canvas = document.querySelector('#canvas');
const preview = document.querySelector('#preview');
const cameraButton = document.querySelector('#cameraButton');
const imageInput = document.querySelector('#imageInput');
const analyzeButton = document.querySelector('#analyzeButton');
const downloadButton = document.querySelector('#downloadButton');
const status = document.querySelector('#status');
const results = document.querySelector('#results');
let stream, currentFile;

cameraButton.onclick = async () => {
  try { stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false }); video.srcObject = stream; video.hidden = false; preview.hidden = true; currentFile = null; analyzeButton.disabled = false; status.textContent = 'Camera ready. Analyze a frame when you are ready.'; }
  catch { status.textContent = 'Camera access was unavailable. Choose an image instead.'; }
};
imageInput.onchange = () => { currentFile = imageInput.files[0]; if (!currentFile) return; preview.src = URL.createObjectURL(currentFile); preview.hidden = false; video.hidden = true; analyzeButton.disabled = false; status.textContent = 'Image ready to analyze.'; };
function frameFile() { return new Promise(resolve => { canvas.width = video.videoWidth; canvas.height = video.videoHeight; canvas.getContext('2d').drawImage(video, 0, 0); canvas.toBlob(blob => resolve(new File([blob], 'camera.jpg', {type:'image/jpeg'})), 'image/jpeg'); }); }
async function selectedFile() { return currentFile || await frameFile(); }
analyzeButton.onclick = async () => { const file = await selectedFile(); if (!file || (!currentFile && !video.videoWidth)) return; const body = new FormData(); body.append('image', file); status.textContent = 'Analyzing…'; try { const response = await fetch('/api/predict', {method:'POST', body}); const data = await response.json(); if (!response.ok) throw Error(data.error); results.innerHTML = data.faces.length ? data.faces.map((face, i) => `<div class="face"><strong>Face ${i + 1}</strong><br>${face.gender_presentation} presentation (${(face.gender_confidence*100).toFixed(1)}%) · age ${face.age} (${(face.age_confidence*100).toFixed(1)}%)</div>`).join('') : '<p>No face found. Try a well-lit, front-facing image.</p>'; status.textContent = 'Analysis complete.'; downloadButton.disabled = false; } catch (error) { status.textContent = error.message; } };
downloadButton.onclick = async () => { const file = await selectedFile(); const body = new FormData(); body.append('image', file); const response = await fetch('/api/annotate', {method:'POST', body}); if (!response.ok) { status.textContent = 'Could not create annotated image.'; return; } const a = document.createElement('a'); a.href = URL.createObjectURL(await response.blob()); a.download = 'annotated.jpg'; a.click(); URL.revokeObjectURL(a.href); };
