// chat.js
class ChatManager {
    constructor(currentUser, otherUser) {
        console.log(` setting up chat between ${currentUser} and ${otherUser}!`); 
               this.currentUser = currentUser;
        this.currentUser = currentUser;

        this.otherUser = otherUser; 
        this.socket = null;                  
        this.messageInput = document.getElementById('chat-message-input');  // Input field for typing messages
        this.messageForm = document.getElementById('chat-form');           // Form for submitting messages
        this.messagesDiv = document.getElementById('chat-messages');       // Where messages appear
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 'N/A';
        this.typingTimeout = null;           // Timer for typing indicator
        this.hasStartedChat = false;         // Track if we've started the chat session

        this.otherUser = otherUser;
        this.socket = null;
        this.messageInput = document.getElementById('chat-message-input');
        this.messageForm = document.getElementById('chat-form');
        this.messagesDiv = document.getElementById('chat-messages');
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        this.typingIndicator = document.getElementById('typing-indicator');
        this.typingUsername = document.getElementById('typing-username');
        this.typingTimeout = null;

        
        this.initializeWebSocket();
        this.setupEventListeners();
        this.setupTypingDetection();
    }

    setupTypingDetection() {
        this.messageInput.addEventListener('input', () => {
            if (!this.typingTimeout) {
                this.socket.send(JSON.stringify({
                    'type': 'typing',
                    'username': this.currentUser
                }));
            }
            
            // Clear existing timeout
            clearTimeout(this.typingTimeout);
            
            // Set new timeout
            this.typingTimeout = setTimeout(() => {
                this.socket.send(JSON.stringify({
                    'type': 'stopped_typing',
                    'username': this.currentUser
                }));
                this.typingTimeout = null;
            }, 1000); // We stop typing indicator after 1 second of no input
        });
    }

    /**
     * Sets up the ws connection to handle real-time chat updates.
     */
    initializeWebSocket() {
        const wsSchema = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsSchema}//${window.location.host}/ws/chat/`; 
        console.log('Chat: Attempting to connect to WebSocket at:', wsUrl);
        
        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = () => {
            console.log('Chat WebSocket connection established');
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            switch (data.type) {
                case 'init':
                    console.log(`Connected as ${data.username}`);
                    break;
                case 'chat_message':
                    this.appendMessage(data.message, data.sender === this.currentUser, data.timestamp);
                    break;
                case 'typing_indicator':
                    this.handleTypingIndicator(data.sender, data.is_typing);
                    break;
                case 'user_list':
                    break;
            }
        };

        this.socket.onclose = () => {
            console.log('Oops, chat connection dropped. Reconnecting in 5...');
            setTimeout(() => this.initializeWebSocket(), 5000);
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'typing') {
                this.showTypingIndicator(data.username);
            } else if (data.type === 'stopped_typing') {
                this.hideTypingIndicator();
            } else {
                this.appendMessage(data.message, data.sender === this.currentUser);
                this.hideTypingIndicator();
            }
        };
    }

    showTypingIndicator(username) {
        if (username !== this.currentUser) {
            this.typingUsername.textContent = username;
            this.typingIndicator.classList.remove('hidden');
        }
    }

    hideTypingIndicator() {
        this.typingIndicator.classList.add('hidden');
    }

    async saveMessageToDatabase(message) {
        try {
            const response = await fetch('/save-message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({
                    message: message,
                    receiver: this.otherUser
                })
            });

        this.socket.onerror = (error) => {
            console.error('Uh-oh, chat WebSocket hit a snag:', error);
        };
    }

    /**
     * Sets up listeners for form submission and typing events.
     */
    setupEventListeners() {
        if (this.messageForm) {
            this.messageForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const message = this.messageInput?.value.trim();
                if (!message) return;
                if (this.socket.readyState === WebSocket.OPEN) {
                    if (!this.hasStartedChat) {
                        console.log('Chat: Starting private chat with:', this.otherUser);
                        this.socket.send(JSON.stringify({
                            'type': 'start_chat',
                            'receiver': this.otherUser
                        }));
                        this.hasStartedChat = true;
                    }
                    console.log('Chat: Sending chat message:', message);
                    this.socket.send(JSON.stringify({

                        'type': 'chat_message',

                        'type': 'message',

                        'message': message,
                        'sender': this.currentUser,
                        'receiver': this.otherUser
                    }));
                    this.messageInput.value = '';
                }
            });
        }

        // Show typing indicator when user types
        if (this.messageInput) {
            this.messageInput.addEventListener('input', () => {
                if (this.socket.readyState === WebSocket.OPEN) {
                    console.log('Chat: Sending typing indicator');
                    this.socket.send(JSON.stringify({
                        'type': 'typing',
                        'is_typing': true,
                        'receiver': this.otherUser
                    }));

                    // Clear any existing timeout and set a new one to stop typing indicator
                    clearTimeout(this.typingTimeout);
                    this.typingTimeout = setTimeout(() => {
                        this.socket.send(JSON.stringify({
                            'type': 'typing',
                            'is_typing': false,
                            'receiver': this.otherUser
                        }));
                    }, 1000);
                }
            });
        }
    }

    /**
     * Adds a new message to the chat window.
     * @param {string} message - The text of the message
     * @param {boolean} isSender - True if the current user sent it
     * @param {string} timestamp - When the message was sent
     */
    appendMessage(message, isSender, timestamp) {
        console.log('Chat: Appending message:', message);
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex ${isSender ? 'justify-end' : ''}`; // Right for sender, left for receiver
        const time = timestamp ? new Date(timestamp).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }) : new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
        messageDiv.innerHTML = `
            <div class="max-w-xs lg:max-w-md p-3 rounded-lg ${isSender ? 'bg-indigo-600 text-white' : 'bg-gray-200'}">
                <p>${this.escapeHtml(message)}</p>
                <span class="text-xs ${isSender ? 'text-indigo-200' : 'text-gray-500'}">${time}</span>
            </div>
        `;
        if (this.messagesDiv) {
            this.messagesDiv.appendChild(messageDiv);
            this.messagesDiv.scrollTop = this.messagesDiv.scrollHeight; // Scroll to the bottom
        }
    }

    /**
     * Shows or hides the "X is typing..." indicator.
     * @param {string} sender - Who’s typing
     * @param {boolean} isTyping - Are they currently typing?
     */
    handleTypingIndicator(sender, isTyping) {
        console.log(`${sender} typing status: ${isTyping}`);
        const typingDiv = document.getElementById('typing-indicator') || document.createElement('div');
        typingDiv.id = 'typing-indicator';
        const typingArea = document.getElementById('typing-area'); // New target
        
        const isCurrentUser = sender === this.currentUser;
        const typingText = isCurrentUser ? '' : (sender + ' is typing...');
    
        if (isTyping) {
            typingDiv.textContent = typingText;
            typingDiv.className = `text-sm italic ${isCurrentUser ?  'text-gray-500': 'text-blue-500'}`;
            if (typingArea && !typingDiv.parentNode) {
                typingArea.appendChild(typingDiv); // Append to typing-area instead
            }
        } else if (typingDiv.parentNode) {
            typingDiv.parentNode.removeChild(typingDiv);
        }
    
        if (this.messagesDiv) {
            this.messagesDiv.scrollTop = this.messagesDiv.scrollHeight;
        }
    }

    /**
     * Escapes HTML to prevent XSS attacks.
     * @param {string} unsafe - The raw text to escape
     * @returns {string} - Safe HTML
     */
    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&")
            .replace(/</g, "<")
            .replace(/>/g, ">")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "'");
    }
}

/**
 * Keeps track of which users are online/offline & updates the UI.
 */
class UserStatusManager {
    constructor(currentUser) {
        this.currentUser = currentUser;
        this.statusSocket = null;
        this.initializeStatusWebSocket();
    }

    initializeStatusWebSocket() {
        const wsSchema = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsSchema}//${window.location.host}/ws/chat/`;
        console.log('Status: Attempting to connect to WebSocket at:', wsUrl);
        
        this.statusSocket = new WebSocket(wsUrl);

        this.statusSocket.onopen = () => {
            console.log('Status WebSocket connection established');
        };

        this.statusSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'user_list') {
                data.users.forEach(user => {
                    this.updateUserStatus(user.username, user.is_online);
                });
            }
        };

        this.statusSocket.onclose = () => {
            console.log('Status WebSocket connection closed');
            setTimeout(() => this.initializeStatusWebSocket(), 5000);
        };

        this.statusSocket.onerror = (error) => {
            console.error('Status WebSocket error:', error);
        };
    }

    /**
     * Updates the UI to show if a user is online or offline.
     * @param {string} username - The user to update
     * @param {boolean} isOnline - Their online status
     */
    updateUserStatus(username, isOnline) {
        setTimeout(() => {
            const userElements = document.querySelectorAll(`.user-item a[data-username="${username}"]`);
            userElements.forEach(element => {
                const nameContainer = element.querySelector('.ml-4.flex.items-center');
                if (nameContainer) {
                    const existingStatus = nameContainer.querySelector('.status-indicator');
                    if (existingStatus) {
                        existingStatus.remove();
                    }
                    const statusSpan = document.createElement('span');
                    statusSpan.className = `status-indicator ml-2 inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${
                        isOnline ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`;
                    statusSpan.textContent = isOnline ? 'Online' : 'Offline';
                    nameContainer.appendChild(statusSpan);
                } else {
                    console.log(`Status: No name container found for ${username}`);
                }
            });
        }, 100);
       
    }
}

// Initialize based on page context
console.log('chat.js loaded');
const currentUser = document.querySelector('meta[name="current-user"]')?.content;
console.log(`Current user is: ${currentUser || 'nobody yet'}`);

// Show online/offline status on the users list page
if (currentUser) {
    console.log(`Starting status updates for ${currentUser}`);
    new UserStatusManager(currentUser);
} else {
    console.error('No current user found in meta tag');
}

// Initialize ChatManager only on chat page
if (document.getElementById('chat-messages')) {
    const otherUser = document.querySelector('meta[name="other-user"]')?.content;
    console.log('Initializing ChatManager for:', currentUser, otherUser);
    if (currentUser && otherUser) {
        new ChatManager(currentUser, otherUser);
    } else {
        console.error('Missing currentUser or otherUser for ChatManager');
    }
}