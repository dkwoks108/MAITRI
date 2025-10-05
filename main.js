const video = document.getElementById('webcam');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const emotionElem = document.getElementById('emotion');
const messageElem = document.getElementById('message');

const API_URL = "https://abcd-1234-56-78-90.ngrok.io/predict"; // Replace with your ngrok URL

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
        await video.play();
    } catch (err) {
        emotionElem.textContent = '';
        messageElem.textContent = 'Could not access webcam. Please allow camera permissions.';
        console.error(err);
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
            }, 5000); // Record 5 seconds of audio
        } catch (err) {
            reject(err);
        }
    });
}

async function sendToAPI(imageBlob, audioBlob) {
    try {
        const formData = new FormData();
        formData.append('frame', imageBlob, 'frame.jpg');  // Must match backend key
        formData.append('voice', audioBlob, 'voice.webm'); // Must match backend key

        const res = await fetch(API_URL, { 
            method: 'POST', 
            body: formData,
            mode: 'cors'
        });

        if (!res.ok) throw new Error('API response error');
        const data = await res.json();
        displayResult(data);
    } catch (err) {
        console.error(err);
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
        messageElem.textContent = "Recording audio...";
        const audioBlob = await recordAudioSegment();
        messageElem.textContent = "Analyzing...";
        await sendToAPI(imageBlob, audioBlob);
    } catch (err) {
        console.error(err);
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
    detectionInterval = setInterval(detectEmotion, 10000); // Run every 10 sec
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
