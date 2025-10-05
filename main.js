const video = document.getElementById('webcam');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const emotionElem = document.getElementById('emotion');
const messageElem = document.getElementById('message');

const API_URL = 'https://example.ngrok.io/predict'; // Placeholder

let stream = null;
let audioStream = null;
let mediaRecorder = null;
let detectionInterval = null;
let isDetecting = false;
let chunks = [];

async function startWebcam() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
    } catch (err) {
        emotionElem.textContent = '';
        messageElem.textContent = 'Could not access webcam. Please allow camera permissions.';
    }
}

async function getAudioStream() {
    if (!audioStream) {
        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
    }
    return audioStream;
}

function captureFrame() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 320;
    canvas.height = video.videoHeight || 320;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    return new Promise(resolve => {
        canvas.toBlob(blob => resolve(blob), 'image/jpeg', 0.92);
    });
}

function recordAudioSegment() {
    return new Promise(async (resolve, reject) => {
        try {
            const stream = await getAudioStream();
            mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
            chunks = [];
            mediaRecorder.ondataavailable = e => {
                if (e.data.size > 0) chunks.push(e.data);
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(chunks, { type: 'audio/webm' });
                resolve(audioBlob);
            };
            mediaRecorder.start();
            setTimeout(() => {
                if (mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();
                }
            }, 5000);
        } catch (err) {
            reject(err);
        }
    });
}

async function sendToAPI(imageBlob, audioBlob) {
    try {
        const formData = new FormData();
        formData.append('image', imageBlob, 'frame.jpg');
        formData.append('audio', audioBlob, 'audio.webm');

        const res = await fetch(API_URL, { method: 'POST', body: formData });
        if (!res.ok) throw new Error('API response error');
        const data = await res.json();
        displayResult(data);
    } catch (err) {
        emotionElem.textContent = '';
        messageElem.textContent = 'Could not connect to backend. Please try again.';
    }
}

function displayResult(data) {
    if (!data) {
        emotionElem.textContent = '';
        messageElem.textContent = '';
        return;
    }
    emotionElem.textContent = data.emotion ? `Detected Emotion: ${data.emotion}` : '';
    messageElem.textContent = data.message || '';
}

async function detectEmotion() {
    if (!isDetecting) return;
    try {
        const imageBlob = await captureFrame();
        messageElem.textContent = "Listening...";
        emotionElem.textContent = '';
        const audioBlob = await recordAudioSegment();
        messageElem.textContent = "Analyzing...";
        await sendToAPI(imageBlob, audioBlob);
    } catch (err) {
        emotionElem.textContent = '';
        messageElem.textContent = 'Error during detection.';
    }
}

function startDetection() {
    if (isDetecting) return;
    isDetecting = true;
    startBtn.disabled = true;
    stopBtn.disabled = false;
    emotionElem.textContent = '';
    messageElem.textContent = 'Starting detection...';
    detectEmotion();
    detectionInterval = setInterval(detectEmotion, 5000);
}

function stopDetection() {
    isDetecting = false;
    startBtn.disabled = false;
    stopBtn.disabled = true;
    clearInterval(detectionInterval);
    detectionInterval = null;
    emotionElem.textContent = '';
    messageElem.textContent = 'Detection stopped.';
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
}

startBtn.addEventListener('click', startDetection);
stopBtn.addEventListener('click', stopDetection);

window.addEventListener('DOMContentLoaded', async () => {
    await startWebcam();
});
