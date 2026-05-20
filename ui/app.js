// State Management
let sessionToken = localStorage.getItem("session_token");
let currentUser = JSON.parse(localStorage.getItem("current_user"));
let chatHistory = [];
let currentSessionId = null;

// DOM Elements
const loginContainer = document.getElementById("login-container");
const mainContainer = document.getElementById("main-container");
const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");
const loginBtn = document.getElementById("login-btn");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const btnNewChat = document.getElementById("btn-new-chat");
const btnLogout = document.getElementById("btn-logout");

const userAvatar = document.getElementById("user-avatar");
const userNameDisplay = document.getElementById("user-name-display");
const userRoleDisplay = document.getElementById("user-role-display");
const userHeaderWelcome = document.getElementById("user-header-welcome");

// New Tab and Calendar elements
const tabChat = document.getElementById("tab-chat");
const tabSchedule = document.getElementById("tab-schedule");
const panelChat = document.getElementById("panel-chat");
const panelSchedule = document.getElementById("panel-schedule");
const meetingsList = document.getElementById("meetings-list");
const btnRefreshSchedule = document.getElementById("btn-refresh-schedule");
const deckTitle = document.getElementById("deck-title");
const recentChatsList = document.getElementById("recent-chats-list");

// Initialize Marked configuration
marked.setOptions({
    breaks: true,
    gfm: true
});

// App Initialization
function init() {
    if (sessionToken && currentUser) {
        showChatView();
    } else {
        showLoginView();
    }
}

// UI Toggles
function showLoginView() {
    loginContainer.classList.remove("hidden");
    mainContainer.classList.add("hidden");
    loginError.classList.add("hidden");
    passwordInput.value = "";
}

function showChatView() {
    loginContainer.classList.add("hidden");
    mainContainer.classList.remove("hidden");

    // Set Profile Info
    const initials = currentUser.name.split(" ").map(n => n[0]).join("").toUpperCase();
    userAvatar.textContent = initials;
    userNameDisplay.textContent = currentUser.name.toUpperCase();
    userRoleDisplay.textContent = currentUser.role.replace("_", " ").toUpperCase();

    const formattedRole = currentUser.role.replace("_", " ").toLowerCase();
    userHeaderWelcome.textContent = `Welcome, ${currentUser.name} · ${formattedRole}`;

    // Load recent chats
    loadRecentChats();

    // Start clean chat state if no active session
    if (!currentSessionId) {
        startNewChat();
    }
}

// Start New Chat / Reset
function startNewChat() {
    currentSessionId = null;
    chatHistory = [];
    chatMessages.innerHTML = "";

    // Initial welcome message
    appendMessage("assistant", `Hello ${currentUser.name}! I'm your enterprise AI assistant. How can I help you today?`);
    loadRecentChats();
}

async function loadRecentChats() {
    recentChatsList.innerHTML = `
    <div class="text-slate-500 text-xxs italic px-3 py-2 animate-pulse">Loading chats...</div>
    `;
    try {
        const response = await fetch("/api/chats", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${sessionToken}`
            }
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to load chats");
        }

        recentChatsList.innerHTML = "";

        if (data.length === 0) {
            recentChatsList.innerHTML = `
            <div class="text-slate-500 text-xxs italic px-3 py-2">No active chats</div>
            `;
            return;
        }

        data.forEach(chat => {
            const chatItem = document.createElement("div");
            const isActive = chat.id === currentSessionId;
            chatItem.className = `chat-item flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-slate-300 hover:bg-white/5 hover:text-white transition-all cursor-pointer group ${isActive ? 'bg-white/10 text-white font-bold border-l-2 border-cyan-400' : ''}`;
            chatItem.innerHTML = `
            <div class="flex items-center gap-2 truncate flex-1">
                <span class="chat-icon">💬</span>
                <span class="chat-text text-sm truncate">${escapeHtml(chat.title)}</span>
            </div>
            <button class="delete-chat-btn text-slate-600 hover:text-rose-400 p-0.5 rounded opacity-0 group-hover:opacity-100 transition-all text-xs font-bold" data-id="${chat.id}">×</button>
            `;

            chatItem.addEventListener("click", (e) => {
                if (e.target.classList.contains("delete-chat-btn")) {
                    e.stopPropagation();
                    deleteChatSession(chat.id);
                } else {
                    selectChatSession(chat.id);
                }
            });

            recentChatsList.appendChild(chatItem);
        });
    } catch (err) {
        console.error(err);
        recentChatsList.innerHTML = `
        <div class="text-rose-400/80 text-xxs italic px-3 py-2">Error loading chats</div>
        `;
    }
}

async function selectChatSession(sessionId) {
    currentSessionId = sessionId;
    chatMessages.innerHTML = `
    <div class="text-center py-12 flex flex-col items-center justify-center gap-3">
        <div class="spinner"></div>
        <span class="text-slate-400 text-xs font-semibold uppercase tracking-wider animate-pulse">Loading chat history...</span>
    </div>
    `;

    // Highlight active chat immediately
    const items = recentChatsList.querySelectorAll(".chat-item");
    items.forEach(item => {
        item.classList.remove("bg-white/10", "text-white", "font-bold", "border-l-2", "border-cyan-400");
    });

    try {
        const response = await fetch(`/api/chats/${sessionId}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${sessionToken}`
            }
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Failed to load chat session");
        }

        chatHistory = data.messages || [];
        chatMessages.innerHTML = "";

        if (chatHistory.length === 0) {
            appendMessage("assistant", `Hello ${currentUser.name}! This conversation has no messages yet. How can I help you today?`);
        } else {
            chatHistory.forEach(msg => {
                const messageDiv = document.createElement("div");
                messageDiv.className = `flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} w-full`;
                const isUser = msg.role === "user";
                messageDiv.innerHTML = `
                <div class="${isUser ? 'chat-bubble-user' : 'chat-bubble-assistant'} max-w-[75%] px-5 py-4 text-sm leading-relaxed animate-fade-in">
                    ${!isUser ? `
                    <div class="flex items-center gap-2 mb-2 text-xxs font-bold text-cyan-400 uppercase tracking-widest">
                        <span>◆ ASSISTANT</span>
                    </div>
                    ` : ''}
                    <div class="markdown-content text-slate-100">
                        ${isUser ? escapeHtml(msg.content) : marked.parse(msg.content)}
                    </div>
                </div>
                `;
                chatMessages.appendChild(messageDiv);
            });
            scrollToBottom();
        }

        loadRecentChats();

    } catch (err) {
        console.error(err);
        chatMessages.innerHTML = `
        <div class="text-center py-12 text-rose-400 font-semibold">
            Error loading conversation history.
        </div>
        `;
    }
}

async function deleteChatSession(sessionId) {
    if (!confirm("Are you sure you want to delete this chat session?")) return;
    try {
        const response = await fetch(`/api/chats/${sessionId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${sessionToken}`
            }
        });
        if (response.ok) {
            if (currentSessionId === sessionId) {
                startNewChat();
            } else {
                loadRecentChats();
            }
        }
    } catch (err) {
        console.error(err);
    }
}

// Append Message to UI & Log
function appendMessage(role, content) {
    const msgObj = { role, content };
    if (role !== "system") {
        chatHistory.push(msgObj);
    }

    const messageDiv = document.createElement("div");
    messageDiv.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'} w-full`;

    const isUser = role === "user";

    messageDiv.innerHTML = `
    <div class="${isUser ? 'chat-bubble-user' : 'chat-bubble-assistant'} max-w-[75%] px-5 py-4 text-sm leading-relaxed">
        ${!isUser ? `
        <div class="flex items-center gap-2 mb-2 text-xxs font-bold text-cyan-400 uppercase tracking-widest">
            <span>◆ ASSISTANT</span>
        </div>
        ` : ''}
        <div class="markdown-content text-slate-100">
            ${isUser ? escapeHtml(content) : marked.parse(content)}
        </div>
    </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Append Thinking Loader
function appendLoader() {
    const loaderDiv = document.createElement("div");
    loaderDiv.id = "thinking-loader";
    loaderDiv.className = "flex justify-start w-full";
    loaderDiv.innerHTML = `
    <div class="chat-bubble-assistant max-w-[75%] px-5 py-4 text-sm">
        <div class="flex items-center gap-3">
            <div class="spinner"></div>
            <span class="text-xs text-cyan-400 font-semibold tracking-wider uppercase animate-pulse">Running multi-agent reasoning...</span>
        </div>
    </div>
    `;
    chatMessages.appendChild(loaderDiv);
    scrollToBottom();
}

function removeLoader() {
    const loader = document.getElementById("thinking-loader");
    if (loader) {
        loader.remove();
    }
}

// Scroll chat window to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Escape HTML utility for user messages
function escapeHtml(text) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

// Event Listeners: Login Form
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    loginError.classList.add("hidden");
    loginBtn.disabled = true;
    loginBtn.textContent = "AUTHENTICATING...";

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: emailInput.value,
                password: passwordInput.value
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            localStorage.setItem("session_token", data.token);
            localStorage.setItem("current_user", JSON.stringify(data.user));
            sessionToken = data.token;
            currentUser = data.user;

            showChatView();
        } else {
            loginError.textContent = data.detail || "Authentication failed.";
            loginError.classList.remove("hidden");
        }
    } catch (err) {
        console.error("Login request failed", err);
        loginError.textContent = "Network error. Please try again.";
        loginError.classList.remove("hidden");
    } finally {
        loginBtn.disabled = false;
        loginBtn.textContent = "AUTHENTICATE →";
    }
});

// Event Listeners: Chat Submission
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;

    // Clear input and adjust textarea height
    chatInput.value = "";
    chatInput.style.height = "auto";

    // Add user message to UI
    appendMessage("user", query);

    // Append loading bubble
    appendLoader();

    try {
        const response = await fetch("/api/chats/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${sessionToken}`
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                message: query
            })
        });

        const data = await response.json();
        removeLoader();

        if (response.ok && data.response) {
            // Update current session ID
            currentSessionId = data.session_id;

            // Render assistant response
            appendMessage("assistant", data.response);

            // Reload sidebar list to show correct titles and active highlights
            loadRecentChats();
        } else {
            appendMessage("assistant", `**Error:** ${data.detail || 'Could not fetch response from server.'}`);
        }
    } catch (err) {
        console.error("Chat request failed", err);
        removeLoader();
        appendMessage("assistant", "**Error:** Network error occurred. Please check connection.");
    }
});

// Auto-resizing textarea & handling Enter to submit
chatInput.addEventListener("input", function() {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});

chatInput.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event("submit"));
    }
});

// New Chat Button
btnNewChat.addEventListener("click", () => {
    startNewChat();
});

// Logout Button
btnLogout.addEventListener("click", async () => {
    if (sessionToken) {
        try {
            await fetch("/api/logout", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${sessionToken}`
                }
            });
        } catch (e) {
            console.error("Logout request failed", e);
        }
    }

    localStorage.removeItem("session_token");
    localStorage.removeItem("current_user");
    sessionToken = null;
    currentUser = null;
    chatHistory = [];

    showLoginView();
});

// Tab Toggling & Calendar View Actions
tabChat.addEventListener("click", () => {
    tabChat.className = "chat-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-white bg-white/10 font-bold transition-all cursor-pointer";
    tabSchedule.className = "chat-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-white/5 hover:text-white transition-all cursor-pointer";

    panelChat.classList.remove("hidden");
    panelSchedule.classList.add("hidden");
    deckTitle.textContent = "COMMAND DECK";
});

tabSchedule.addEventListener("click", () => {
    tabChat.className = "chat-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-white/5 hover:text-white transition-all cursor-pointer";
    tabSchedule.className = "chat-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-white bg-white/10 font-bold transition-all cursor-pointer";

    panelChat.classList.add("hidden");
    panelSchedule.classList.remove("hidden");
    deckTitle.textContent = "SCHEDULE DECK";

    loadMeetings();
});

btnRefreshSchedule.addEventListener("click", () => {
    loadMeetings();
});

async function loadMeetings() {
    meetingsList.innerHTML = `
    <div class="text-center py-12 flex flex-col items-center justify-center gap-3">
        <div class="spinner"></div>
        <span class="text-slate-400 text-xs font-semibold uppercase tracking-wider animate-pulse">Loading scheduled events...</span>
    </div>
    `;
    try {
        const response = await fetch("/api/meetings", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${sessionToken}`
            }
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to load meetings");
        }

        meetingsList.innerHTML = "";

        if (data.length === 0) {
            meetingsList.innerHTML = `
            <div class="text-center py-12 text-slate-500 text-sm font-medium">
                No scheduled meetings found. Use the Chat assistant to draft and send new invites.
            </div>
            `;
            return;
        }

        // Sort by date_time descending
        data.reverse().forEach(meeting => {
            const isSent = meeting.status === "sent";
            const badgeClass = isSent 
                ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400 shadow-sm shadow-emerald-500/10" 
                : "bg-amber-500/10 border-amber-500/30 text-amber-400 shadow-sm shadow-amber-500/10";
            const badgeLabel = isSent ? "SCHEDULED & SENT" : "DRAFTED (PENDING)";

            const card = document.createElement("div");
            card.className = "p-5 rounded-2xl border border-white/5 bg-white/[0.02] backdrop-blur-2xl hover:border-white/10 transition-all flex flex-col gap-4 animate-fade-in";
            card.innerHTML = `
            <div class="flex justify-between items-start gap-4">
                <div>
                    <span class="text-xxs px-2 py-1 border rounded-full font-bold tracking-wider ${badgeClass}">
                        ${badgeLabel}
                    </span>
                    <h3 class="text-base font-bold text-white mt-2">${escapeHtml(meeting.subject)}</h3>
                </div>
                <div class="text-right">
                    <div class="text-xs text-slate-400 font-semibold">${escapeHtml(meeting.date_time)}</div>
                    <div class="text-xxs text-slate-500 font-medium mt-1">${meeting.duration_minutes} mins</div>
                </div>
            </div>

            <div class="text-xs text-slate-300 bg-black/25 p-3 rounded-lg border border-white/[0.02]">
                <div class="font-bold text-slate-400 mb-1 text-xxs uppercase tracking-wider">Agenda</div>
                <p class="whitespace-pre-wrap">${escapeHtml(meeting.agenda)}</p>
            </div>

            <div class="flex justify-between items-center gap-4 flex-wrap">
                <div class="flex items-center gap-1.5 flex-wrap">
                    <span class="text-xxs text-slate-500 font-bold uppercase tracking-wider">Attendees:</span>
                    ${meeting.participants.map(email => `
                        <span class="text-xxs px-2 py-0.5 rounded bg-white/5 border border-white/5 text-slate-300 font-medium">${escapeHtml(email)}</span>
                    `).join("")}
                </div>

                <a href="/api/meetings/${meeting.id}/ics" download
                   class="text-xxs font-bold px-3 py-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20 hover:bg-cyan-500/25 hover:border-cyan-400/30 text-cyan-400 transition-all flex items-center gap-1.5 shadow-sm shadow-cyan-500/5">
                    <span>📥</span> ADD TO CALENDAR
                </a>
            </div>
            `;
            meetingsList.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        meetingsList.innerHTML = `
        <div class="text-center py-12 text-rose-400 text-sm font-semibold animate-fade-in">
            Error loading scheduled meetings. Please check connection.
        </div>
        `;
    }
}

// Run app init
init();
