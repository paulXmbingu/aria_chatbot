const messagesContainer =
    document.getElementById("messages");

const emptyState =
    document.getElementById("empty-state");

const chatForm =
    document.getElementById("chat-form");

const messageInput =
    document.getElementById("message-input");

const sendButton =
    document.getElementById("send-btn");

const newChatButton =
    document.getElementById("new-chat-btn");

const conversationList =
    document.getElementById("conversation-list");

const mobileNewChatButton =
    document.getElementById(
        "mobile-new-chat-btn"
    );

const openSidebarButton =
    document.getElementById(
        "open-sidebar-btn"
    );

const closeSidebarButton =
    document.getElementById(
        "close-sidebar-btn"
    );

const sidebar =
    document.querySelector(".sidebar");

const sidebarOverlay =
    document.getElementById(
        "sidebar-overlay"
    );


let conversationId = null;
let conversationListData = [];
let isLoading = false;


/* ========================================
   Markdown
======================================== */

marked.setOptions({
    gfm: true,
    breaks: true,
    pedantic: false,
});


marked.use({
    renderer: {
        link({ href, title, text }) {
            const link =
                document.createElement("a");

            link.href = href;
            link.textContent = text;
            link.target = "_blank";
            link.rel =
                "noopener noreferrer";

            if (title) {
                link.title = title;
            }

            return link.outerHTML;
        },
    },
});


function renderMarkdown(content) {
    if (!content) {
        return "";
    }

    return marked.parse(content);
}


/* ========================================
   API Errors
======================================== */

function getApiError(data) {
    if (data?.error) {
        return data.error;
    }

    if (
        data &&
        typeof data === "object"
    ) {
        const messages = [];

        Object.values(data).forEach(
            (value) => {
                if (Array.isArray(value)) {
                    messages.push(
                        ...value
                    );
                } else if (
                    typeof value === "string"
                ) {
                    messages.push(
                        value
                    );
                }
            }
        );

        if (messages.length > 0) {
            return messages.join(" ");
        }
    }

    return (
        "Something went wrong. Please try again."
    );
}


/* ========================================
   Code Blocks
======================================== */

function enhanceCodeBlocks(
    container
) {
    const codeBlocks =
        container.querySelectorAll(
            "pre code"
        );

    codeBlocks.forEach(
        (codeBlock) => {
            const pre =
                codeBlock.parentElement;

            if (
                pre.dataset.enhanced ===
                "true"
            ) {
                return;
            }

            pre.dataset.enhanced =
                "true";

            const wrapper =
                document.createElement(
                    "div"
                );

            wrapper.className =
                "code-block";

            const header =
                document.createElement(
                    "div"
                );

            header.className =
                "code-block-header";

            const language =
                codeBlock.className.match(
                    /language-([\w-]+)/
                );

            const languageLabel =
                document.createElement(
                    "span"
                );

            languageLabel.className =
                "code-language";

            languageLabel.textContent =
                language
                    ? language[1]
                    : "Code";

            const copyButton =
                document.createElement(
                    "button"
                );

            copyButton.type = "button";
            copyButton.className =
                "copy-code-button";
            copyButton.textContent =
                "Copy";

            copyButton.addEventListener(
                "click",
                async () => {
                    try {
                        await navigator.clipboard.writeText(
                            codeBlock.textContent
                        );

                        copyButton.textContent =
                            "Copied";

                        setTimeout(
                            () => {
                                copyButton.textContent =
                                    "Copy";
                            },
                            1500
                        );
                    } catch (error) {
                        console.error(
                            error
                        );

                        copyButton.textContent =
                            "Failed";

                        setTimeout(
                            () => {
                                copyButton.textContent =
                                    "Copy";
                            },
                            1500
                        );
                    }
                }
            );

            header.appendChild(
                languageLabel
            );

            header.appendChild(
                copyButton
            );

            pre.parentNode.insertBefore(
                wrapper,
                pre
            );

            wrapper.appendChild(
                header
            );

            wrapper.appendChild(
                pre
            );
        }
    );
}


/* ========================================
   Empty State
======================================== */

function updateEmptyState() {
    const hasMessages =
        messagesContainer.querySelector(
            ".message"
        );

    emptyState.hidden =
        Boolean(hasMessages);
}


/* ========================================
   Messages
======================================== */

function addMessage(
    role,
    content,
    options = {}
) {
    const message =
        document.createElement(
            "div"
        );

    message.className =
        `message ${role}`;

    if (options.messageId) {
        message.dataset.messageId =
            options.messageId;
    }

    const messageContent =
        document.createElement(
            "div"
        );

    messageContent.className =
        "message-content";

    if (role === "assistant") {
        messageContent.innerHTML =
            renderMarkdown(content);

        enhanceCodeBlocks(
            messageContent
        );
    } else {
        messageContent.textContent =
            content;
    }

    message.appendChild(
        messageContent
    );

    if (
        role === "assistant" &&
        options.actions !== false
    ) {
        addMessageActions(
            message,
            content
        );
    }

    messagesContainer.appendChild(
        message
    );

    updateEmptyState();

    messagesContainer.scrollTo({
        top:
            messagesContainer.scrollHeight,
        behavior: "smooth",
    });

    return message;
}


/* ========================================
   Message Actions
======================================== */

function addMessageActions(
    message,
    content
) {
    const actions =
        document.createElement(
            "div"
        );

    actions.className =
        "message-actions";

    const copyButton =
        document.createElement(
            "button"
        );

    copyButton.type = "button";
    copyButton.className =
        "message-action";
    copyButton.textContent =
        "Copy";

    copyButton.addEventListener(
        "click",
        async () => {
            try {
                await navigator.clipboard.writeText(
                    content
                );

                copyButton.textContent =
                    "Copied";

                setTimeout(
                    () => {
                        copyButton.textContent =
                            "Copy";
                    },
                    1500
                );
            } catch (error) {
                console.error(
                    error
                );

                copyButton.textContent =
                    "Failed";

                setTimeout(
                    () => {
                        copyButton.textContent =
                            "Copy";
                    },
                    1500
                );
            }
        }
    );

    const regenerateButton =
        document.createElement(
            "button"
        );

    regenerateButton.type = "button";
    regenerateButton.className =
        "message-action";
    regenerateButton.textContent =
        "Regenerate";

    regenerateButton.addEventListener(
        "click",
        () => {
            regenerateResponse(
                message
            );
        }
    );

    actions.appendChild(
        copyButton
    );

    actions.appendChild(
        regenerateButton
    );

    message.appendChild(
        actions
    );
}


/* ========================================
   Regenerate
======================================== */

async function regenerateResponse(
    assistantMessage
) {
    if (
        isLoading ||
        !conversationId
    ) {
        return;
    }

    const messageId =
        assistantMessage.dataset.messageId;

    if (!messageId) {
        return;
    }

    const originalContent =
        assistantMessage.querySelector(
            ".message-content"
        );

    const originalActions =
        assistantMessage.querySelector(
            ".message-actions"
        );

    if (!originalContent) {
        return;
    }

    if (originalActions) {
        originalActions.remove();
    }

    originalContent.innerHTML =
        `
            <span class="loading-text">
                Aria is thinking
            </span>

            <span class="loading-dots">
                <span>.</span>
                <span>.</span>
                <span>.</span>
            </span>
        `;

    setLoading(true);

    try {
        const response =
            await fetch(
                "/api/chat/regenerate/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify({
                        conversation_id:
                            conversationId,

                        message_id:
                            Number(messageId),
                    }),
                }
            );

        const data =
            await response.json();

        if (!response.ok) {
            throw new Error(
                getApiError(data)
            );
        }

        originalContent.innerHTML =
            renderMarkdown(
                data.response
            );

        enhanceCodeBlocks(
            originalContent
        );

        addMessageActions(
            assistantMessage,
            data.response
        );

        await refreshConversations();

    } catch (error) {
        console.error(
            error
        );

        originalContent.textContent =
            error.message ||
            "Unable to regenerate the response.";

    } finally {
        setLoading(false);

        messageInput.focus();
    }
}


/* ========================================
   Loading Message
======================================== */

function addLoadingMessage() {
    const message =
        document.createElement(
            "div"
        );

    message.className =
        "message assistant loading-message";

    const messageContent =
        document.createElement(
            "div"
        );

    messageContent.className =
        "message-content";

    messageContent.innerHTML =
        `
            <span class="loading-text">
                Aria is thinking
            </span>

            <span class="loading-dots">
                <span>.</span>
                <span>.</span>
                <span>.</span>
            </span>
        `;

    message.appendChild(
        messageContent
    );

    messagesContainer.appendChild(
        message
    );

    updateEmptyState();

    messagesContainer.scrollTo({
        top:
            messagesContainer.scrollHeight,
        behavior: "smooth",
    });

    return message;
}


/* ========================================
   Error
======================================== */

function addErrorMessage(
    content
) {
    const message =
        document.createElement(
            "div"
        );

    message.className =
        "message assistant error-message";

    const messageContent =
        document.createElement(
            "div"
        );

    messageContent.className =
        "message-content";

    messageContent.textContent =
        content;

    message.appendChild(
        messageContent
    );

    messagesContainer.appendChild(
        message
    );

    updateEmptyState();

    messagesContainer.scrollTo({
        top:
            messagesContainer.scrollHeight,
        behavior: "smooth",
    });
}


/* ========================================
   Loading State
======================================== */

function setLoading(
    loading
) {
    isLoading =
        loading;

    messageInput.disabled =
        loading;

    newChatButton.disabled =
        loading;

    sendButton.disabled =
        loading;

    if (mobileNewChatButton) {
        mobileNewChatButton.disabled =
            loading;
    }

    sendButton.textContent =
        "↑";
}


/* ========================================
   Conversation Titles
======================================== */

function createConversationTitle(
    message
) {
    const cleaned =
        message
            .replace(/\s+/g, " ")
            .trim();

    if (!cleaned) {
        return "New chat";
    }

    const words =
        cleaned.split(" ");

    const title =
        words
            .slice(0, 6)
            .join(" ");

    return title.length > 40
        ? `${title.substring(0, 40)}...`
        : title;
}


/* ========================================
   Conversations
======================================== */

async function createConversation() {
    const response =
        await fetch(
            "/api/chat/conversations/",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",
                },

                body: JSON.stringify({}),
            }
        );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            getApiError(data)
        );
    }

    conversationId =
        data.id;

    return data;
}


async function sendMessage(
    message
) {
    const response =
        await fetch(
            "/api/chat/chat/",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",
                },

                body: JSON.stringify({
                    conversation_id:
                        conversationId,

                    message:
                        message,
                }),
            }
        );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            getApiError(data)
        );
    }

    return data;
}


async function loadConversations() {
    const response =
        await fetch(
            "/api/chat/conversations/"
        );

    const data =
        await response.json();

    if (!response.ok) {
        throw new Error(
            getApiError(data)
        );
    }

    return data;
}


/* ========================================
   Conversation List
======================================== */

function renderConversations(
    conversations
) {
    /*
     * Preserve the user's current sidebar
     * scroll position before rebuilding the list.
     */
    const scrollTop =
        conversationList.scrollTop;

    conversationListData =
        conversations;

    conversationList.innerHTML =
        "";

    conversations.forEach(
        (conversation) => {
            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "conversation-item";

            if (
                conversation.id ===
                conversationId
            ) {
                item.classList.add(
                    "active"
                );
            }

            const firstUserMessage =
                conversation.messages.find(
                    (message) =>
                        message.role ===
                        "user"
                );

            const title =
                firstUserMessage
                    ? createConversationTitle(
                          firstUserMessage.content
                      )
                    : "New chat";

            item.textContent =
                title;

            item.title =
                firstUserMessage
                    ? firstUserMessage.content
                    : "New chat";

            item.addEventListener(
                "click",
                () => {
                    selectConversation(
                        conversation.id
                    );
                }
            );

            conversationList.appendChild(
                item
            );
        }
    );

    /*
     * Restore the previous position after
     * the conversation items have been rebuilt.
     */
    conversationList.scrollTop =
        scrollTop;
}


/* ========================================
   Conversation Messages
======================================== */

function renderConversationMessages(
    conversation
) {
    messagesContainer.innerHTML =
        "";

    messagesContainer.appendChild(
        emptyState
    );

    conversation.messages.forEach(
        (message) => {
            addMessage(
                message.role,
                message.content,
                {
                    messageId:
                        message.id,
                }
            );
        }
    );

    updateEmptyState();
}


/* ========================================
   Select Conversation
======================================== */

function selectConversation(
    selectedConversationId
) {
    if (isLoading) {
        return;
    }

    const conversation =
        conversationListData.find(
            (item) =>
                item.id ===
                selectedConversationId
        );

    if (!conversation) {
        return;
    }

    conversationId =
        conversation.id;

    renderConversationMessages(
        conversation
    );

    renderConversations(
        conversationListData
    );

    closeSidebar();

    messageInput.focus();
}


/* ========================================
   Refresh Conversations
======================================== */

async function refreshConversations() {
    const conversations =
        await loadConversations();

    renderConversations(
        conversations
    );
}


/* ========================================
   Sidebar
======================================== */

function openSidebar() {
    if (!sidebar) {
        return;
    }

    sidebar.classList.add(
        "mobile-open"
    );

    if (sidebarOverlay) {
        sidebarOverlay.classList.add(
            "visible"
        );
    }

    document.body.classList.add(
        "sidebar-open"
    );
}


function closeSidebar() {
    if (!sidebar) {
        return;
    }

    sidebar.classList.remove(
        "mobile-open"
    );

    if (sidebarOverlay) {
        sidebarOverlay.classList.remove(
            "visible"
        );
    }

    document.body.classList.remove(
        "sidebar-open"
    );
}


if (openSidebarButton) {
    openSidebarButton.addEventListener(
        "click",
        openSidebar
    );
}


if (closeSidebarButton) {
    closeSidebarButton.addEventListener(
        "click",
        closeSidebar
    );
}


if (sidebarOverlay) {
    sidebarOverlay.addEventListener(
        "click",
        closeSidebar
    );
}


/* ========================================
   New Chat
======================================== */

async function handleNewChat() {
    if (isLoading) {
        return;
    }

    /*
     * A new chat is only a local UI state.
     * Do not create a database conversation
     * until the user actually sends a message.
     */
    conversationId = null;

    messagesContainer.innerHTML =
        "";

    messagesContainer.appendChild(
        emptyState
    );

    updateEmptyState();

    closeSidebar();

    messageInput.focus();
}


newChatButton.addEventListener(
    "click",
    handleNewChat
);


if (mobileNewChatButton) {
    mobileNewChatButton.addEventListener(
        "click",
        handleNewChat
    );
}


/* ========================================
   Keyboard
======================================== */

messageInput.addEventListener(
    "keydown",
    (event) => {
        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {
            event.preventDefault();

            chatForm.requestSubmit();
        }
    }
);


/* ========================================
   Chat Submit
======================================== */

chatForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        if (isLoading) {
            return;
        }

        const message =
            messageInput.value.trim();

        if (!message) {
            return;
        }

        messageInput.value =
            "";

        addMessage(
            "user",
            message
        );

        setLoading(true);

        const loadingMessage =
            addLoadingMessage();

        try {
            /*
             * Create the conversation only when
             * the user actually sends a message.
             */
            if (!conversationId) {
                await createConversation();
            }

            const data =
                await sendMessage(
                    message
                );

            loadingMessage.remove();

            addMessage(
                "assistant",
                data.response,
                {
                    messageId:
                        data.message_id,
                }
            );

            await refreshConversations();

        } catch (error) {
            console.error(
                error
            );

            loadingMessage.remove();

            addErrorMessage(
                error.message ||
                "Sorry, I couldn't process your message. Please try again."
            );

        } finally {
            setLoading(false);

            messageInput.focus();
        }
    }
);


/* ========================================
   Initialization
======================================== */

async function initializeChat() {
    try {
        const conversations =
            await loadConversations();

        conversationListData =
            conversations;

        /*
         * Load chat history into the sidebar,
         * but do not automatically select a chat.
         */
        conversationId =
            null;

        renderConversations(
            conversations
        );

        messagesContainer.innerHTML =
            "";

        messagesContainer.appendChild(
            emptyState
        );

        updateEmptyState();

    } catch (error) {
        console.error(
            error
        );

        conversationId =
            null;

        updateEmptyState();
    }

    messageInput.focus();
}


initializeChat();