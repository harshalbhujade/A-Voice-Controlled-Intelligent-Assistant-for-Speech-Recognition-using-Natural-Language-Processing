document.addEventListener('DOMContentLoaded', () => {
    const orb = document.getElementById('orb');
    const statusText = document.getElementById('status-text');
    const chatBox = document.getElementById('chat-box');
    const textInput = document.getElementById('text-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');

    function appendMessage(text, type) {
        if (!text) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${type}-msg`;
        msgDiv.innerHTML = `<p>${text}</p>`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function setOrbState(state, text) {
        orb.className = `orb ${state}`;
        statusText.innerText = text;
        if(state === 'listening') {
            micBtn.classList.add('active');
        } else {
            micBtn.classList.remove('active');
        }
    }

    async function handleCommand(query) {
        appendMessage(query, 'user');
        setOrbState('processing', 'Thinking...');
        
        try {
            const res = await fetch('/api/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });
            const data = await res.json();
            
            if(data.success && data.response) {
                appendMessage(data.response, 'bot');
            } else if (!data.success) {
                appendMessage("Error processing command: " + (data.error || "Unknown"), 'system');
            }
        } catch (err) {
            console.error(err);
            appendMessage("Failed to reach server.", 'system');
        } finally {
            setOrbState('idle', 'Click to Wake');
        }
    }

    async function triggerListen() {
        if(orb.classList.contains('listening')) return;
        
        setOrbState('listening', 'Listening...');
        appendMessage("Listening...", 'system');

        try {
            const res = await fetch('/api/listen', { method: 'POST' });
            const data = await res.json();
            
            if(data.success && data.query) {
                handleCommand(data.query);
            } else {
                appendMessage("Could not hear anything.", 'system');
                setOrbState('idle', 'Click to Wake');
            }
        } catch (err) {
            console.error(err);
            appendMessage("Microphone error.", 'system');
            setOrbState('idle', 'Click to Wake');
        }
    }

    // Event Listeners
    orb.addEventListener('click', triggerListen);
    micBtn.addEventListener('click', triggerListen);

    sendBtn.addEventListener('click', () => {
        const val = textInput.value.trim();
        if(val) {
            textInput.value = '';
            handleCommand(val);
        }
    });

    textInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') {
            sendBtn.click();
        }
    });
});
