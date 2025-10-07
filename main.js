const video = document.getElementById('webcam');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const emotionElem = document.getElementById('emotion');
const messageElem = document.getElementById('message');
const alertIndicator = document.getElementById('alert-indicator');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');
const chatMessages = document.getElementById('chat-messages');

// Configure API URL - will use environment variable or localhost
const API_URL = window.location.hostname === 'localhost' 
    ? "http://localhost:8000/predict"
    : (window.API_URL || "http://localhost:8000/predict");

const CHAT_API_URL = API_URL.replace('/predict', '/chat');
const SAVE_API_URL = API_URL.replace('/predict', '/save');

let stream = null;
let audioStream = null;
let mediaRecorder = null;
let detectionInterval = null;
let isDetecting = false;
let chunks = [];
let currentEmotion = 'neutral';
let emotionHistory = [];
let emotionChart = null;

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
    
    // Update emotion display
    const emotion = data.emotion || 'neutral';
    currentEmotion = emotion;
    
    // Get emotion emoji
    const emotionEmojis = {
        'happy': '😊',
        'sad': '😢',
        'stressed': '😰',
        'anxious': '😟',
        'neutral': '😐',
        'calm': '😌',
        'alert': '😲'
    };
    const emoji = emotionEmojis[emotion] || '😐';
    
    emotionElem.textContent = `${emoji} Detected: ${emotion.toUpperCase()}`;
    messageElem.textContent = data.message || '';
    
    // Show/hide alert indicator
    if (data.alert_triggered) {
        alertIndicator.classList.remove('hidden');
    } else {
        alertIndicator.classList.add('hidden');
    }
    
    // Add to emotion history for chart
    addEmotionToHistory(emotion, data.confidence || 0.5);
    
    // Save session data
    saveSessionData(data);
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

// Chat functionality
function addChatMessage(message, isBot = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isBot ? 'bot-message' : 'user-message'} p-3 rounded-lg border`;
    
    if (isBot) {
        messageDiv.classList.add('bg-indigo-900/30', 'border-indigo-700');
        messageDiv.innerHTML = `
            <strong class="text-indigo-300">MAITRI:</strong>
            <p class="text-slate-200 mt-1">${message}</p>
        `;
    } else {
        messageDiv.classList.add('bg-gray-700/50', 'border-gray-600', 'ml-8');
        messageDiv.innerHTML = `
            <strong class="text-cyan-300">You:</strong>
            <p class="text-slate-200 mt-1">${message}</p>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Display user message
    addChatMessage(message, false);
    chatInput.value = '';
    
    try {
        // Send to chat API
        const response = await fetch(CHAT_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                emotion_state: currentEmotion,
                user_id: 'astronaut_1'
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            addChatMessage(data.reply, true);
        } else {
            addChatMessage("I'm having trouble processing that. Could you try again?", true);
        }
    } catch (err) {
        console.error('Chat error:', err);
        addChatMessage("I'm experiencing connection issues. Please check if the backend is running.", true);
    }
}

// Emotion history and chart
function addEmotionToHistory(emotion, confidence) {
    const timestamp = new Date().toLocaleTimeString();
    emotionHistory.push({
        emotion: emotion,
        confidence: confidence,
        timestamp: timestamp
    });
    
    // Keep only last 10 entries
    if (emotionHistory.length > 10) {
        emotionHistory.shift();
    }
    
    updateEmotionChart();
}

function updateEmotionChart() {
    const ctx = document.getElementById('emotion-chart');
    if (!ctx) return;
    
    // Prepare data
    const labels = emotionHistory.map(h => h.timestamp);
    const confidenceData = emotionHistory.map(h => h.confidence * 100);
    
    // Destroy existing chart
    if (emotionChart) {
        emotionChart.destroy();
    }
    
    // Create new chart
    emotionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Emotion Confidence (%)',
                data: confidenceData,
                borderColor: '#60a5fa',
                backgroundColor: 'rgba(96, 165, 250, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#cbd5e1'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: '#cbd5e1'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#cbd5e1'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

async function saveSessionData(data) {
    try {
        const sessionData = {
            timestamp: new Date().toISOString(),
            emotion: data.emotion,
            confidence: data.confidence,
            video_emotion: data.video_emotion,
            audio_emotion: data.audio_emotion,
            alert_triggered: data.alert_triggered || false,
            message: data.message
        };
        
        await fetch(SAVE_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_data: sessionData,
                user_id: 'astronaut_1'
            })
        });
    } catch (err) {
        console.error('Error saving session:', err);
    }
}

// Event listeners
startBtn.addEventListener('click', startDetection);
stopBtn.addEventListener('click', stopDetection);
chatSend.addEventListener('click', sendChatMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendChatMessage();
    }
});

window.addEventListener('DOMContentLoaded', async () => {
    await startWebcam();
    updateEmotionChart();
});
