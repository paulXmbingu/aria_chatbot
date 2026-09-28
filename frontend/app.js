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

const collapsedNewChatButton =
    document.getElementById(
        "collapsed-new-chat-btn"
    );

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

const collapseSidebarButton =
    document.getElementById(
        "collapse-sidebar-btn"
    );

const expandSidebarButton =
    document.getElementById(
        "expand-sidebar-btn"
    );

const sidebar =
    document.querySelector(".sidebar");

const sidebarOverlay =
    document.getElementById(
        "sidebar-overlay"
    );

const themeToggle =
    document.getElementById(
        "theme-toggle"
    );


let conversationId = null;
let conversationListData = [];
let isLoading = false;


/* ========================================
   Theme
======================================== */

const THEME_STORAGE_KEY =
    "aria-theme";


const systemThemeMediaQuery =
    window.matchMedia(
        "(prefers-color-scheme: dark)"
    );


function getSystemTheme() {
    return systemThemeMediaQuery.matches
        ? "dark"
        : "light";
}


function getSavedTheme() {
    const savedTheme =
        localStorage.getItem(
            THEME_STORAGE_KEY
        );

    if (
        savedTheme === "light" ||
        savedTheme === "dark" ||
        savedTheme === "system"
    ) {
        return savedTheme;
    }

    return "system";
}


function getCurrentTheme() {
    return getSavedTheme();
}


function getEffectiveTheme() {
    const theme =
        getCurrentTheme();

    if (theme === "system") {
        return getSystemTheme();
    }

    return theme;
}


function updateThemeIcon() {
    if (!themeToggle) {
        return;
    }

    const theme =
        getCurrentTheme();

    const systemIcon =
        themeToggle.querySelector(
            ".theme-icon-system"
        );

    const lightIcon =
        themeToggle.querySelector(
            ".theme-icon-light"
        );

    const darkIcon =
        themeToggle.querySelector(
            ".theme-icon-dark"
        );

    if (systemIcon) {
        systemIcon.style.display =
            theme === "system"
                ? "block"
                : "none";
    }

    if (lightIcon) {
        lightIcon.style.display =
            theme === "light"
                ? "block"
                : "none";
    }

    if (darkIcon) {
        darkIcon.style.display =
            theme === "dark"
                ? "block"
                : "none";
    }

    const labels = {
        system: "Theme: System",
        light: "Theme: Light",
        dark: "Theme: Dark",
    };

    themeToggle.setAttribute(
        "aria-label",
        labels[theme]
    );

    themeToggle.setAttribute(
        "title",
        labels[theme]
    );
}


function applyTheme(theme) {

    if (theme === "system") {

        document.documentElement
            .removeAttribute(
                "data-theme"
            );

    } else {

        document.documentElement
            .setAttribute(
                "data-theme",
                theme
            );
    }

    updateThemeIcon();
}


function restoreTheme() {

    const savedTheme =
        getSavedTheme();

    applyTheme(
        savedTheme
    );
}


function cycleTheme() {

    const currentTheme =
        getCurrentTheme();

    let nextTheme;

    if (currentTheme === "system") {

        nextTheme = "light";

    } else if (currentTheme === "light") {

        nextTheme = "dark";

    } else {

        nextTheme = "system";
    }

    localStorage.setItem(
        THEME_STORAGE_KEY,
        nextTheme
    );

    applyTheme(
        nextTheme
    );
}


if (themeToggle) {

    themeToggle.addEventListener(
        "click",
        cycleTheme
    );
}


systemThemeMediaQuery.addEventListener(
    "change",
    () => {

        if (
            getCurrentTheme() ===
            "system"
        ) {
            applyTheme(
                "system"
            );
        }

    }
);


restoreTheme();


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

    if (collapsedNewChatButton) {
        collapsedNewChatButton.disabled =
            loading;
    }

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
   Conversation Menu
======================================== */

function closeConversationMenus() {
    document
        .querySelectorAll(
            ".conversation-menu.open"
        )
        .forEach(
            (menu) => {
                menu.classList.remove(
                    "open"
                );
            }
        );
}


function toggleConversationMenu(
    menu
) {
    const isOpen =
        menu.classList.contains(
            "open"
        );

    closeConversationMenus();

    if (!isOpen) {
        menu.classList.add(
            "open"
        );
    }
}


/* ========================================
   Rename Conversation
======================================== */

async function renameConversation(
    conversation,
    item,
    titleElement,
    input
) {
    const title =
        input.value.trim();

    if (!title) {
        item.replaceChildren(
            titleElement
        );

        return;
    }

    if (
        title ===
        conversation.title
    ) {
        item.replaceChildren(
            titleElement
        );

        return;
    }

    input.disabled = true;

    try {
        const response =
            await fetch(
                `/api/chat/conversations/${conversation.id}/rename/`,
                {
                    method: "PATCH",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify({
                        title,
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

        conversation.title =
            data.title;

        titleElement.textContent =
            data.title;

        titleElement.title =
            data.title;

        item.replaceChildren(
            titleElement
        );

    } catch (error) {
        console.error(
            error
        );

        item.replaceChildren(
            titleElement
        );

        alert(
            error.message ||
            "Unable to rename conversation."
        );
    }
}


function startRenameConversation(
    conversation,
    item
) {
    closeConversationMenus();

    const titleElement =
        item.querySelector(
            ".conversation-title"
        );

    if (!titleElement) {
        return;
    }

    const input =
        document.createElement(
            "input"
        );

    input.type = "text";
    input.className =
        "conversation-rename-input";
    input.value =
        conversation.title ||
        "New Conversation";
    input.maxLength = 120;
    input.autocomplete = "off";

    item.replaceChildren(
        input
    );

    input.focus();
    input.select();

    let completed = false;

    const save = async () => {
        if (completed) {
            return;
        }

        completed = true;

        await renameConversation(
            conversation,
            item,
            titleElement,
            input
        );
    };

    input.addEventListener(
        "keydown",
        (event) => {
            if (
                event.key ===
                "Enter"
            ) {
                event.preventDefault();

                save();
            }

            if (
                event.key ===
                "Escape"
            ) {
                event.preventDefault();

                completed = true;

                item.replaceChildren(
                    titleElement
                );
            }
        }
    );

    input.addEventListener(
        "blur",
        () => {
            save();
        }
    );
}


/* ========================================
   Delete Conversation
======================================== */

async function deleteConversation(
    conversation
) {
    closeConversationMenus();

    const title =
        conversation.title ||
        "New Conversation";

    const confirmed =
        window.confirm(
            `Delete "${title}"?`
        );

    if (!confirmed) {
        return;
    }

    try {
        const response =
            await fetch(
                `/api/chat/conversations/${conversation.id}/delete/`,
                {
                    method: "DELETE",
                }
            );

        if (
            response.status !==
            204
        ) {
            const data =
                await response.json();

            throw new Error(
                getApiError(data)
            );
        }

        conversationListData =
            conversationListData.filter(
                (item) =>
                    item.id !==
                    conversation.id
            );

        if (
            conversationId ===
            conversation.id
        ) {
            conversationId =
                null;

            messagesContainer.innerHTML =
                "";

            messagesContainer.appendChild(
                emptyState
            );

            updateEmptyState();

            messageInput.value =
                "";

            messageInput.focus();
        }

        renderConversations(
            conversationListData
        );

    } catch (error) {
        console.error(
            error
        );

        alert(
            error.message ||
            "Unable to delete conversation."
        );
    }
}


/* ========================================
   Conversation List
======================================== */

function renderConversations(
    conversations
) {
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

            const titleElement =
                document.createElement(
                    "span"
                );

            titleElement.className =
                "conversation-title";

            titleElement.textContent =
                conversation.title ||
                "New Conversation";

            titleElement.title =
                conversation.title ||
                "New Conversation";

            const actions =
                document.createElement(
                    "div"
                );

            actions.className =
                "conversation-actions";

            const menuButton =
                document.createElement(
                    "button"
                );

            menuButton.type =
                "button";

            menuButton.className =
                "conversation-menu-button";

            menuButton.setAttribute(
                "aria-label",
                "Conversation options"
            );

            menuButton.setAttribute(
                "aria-haspopup",
                "true"
            );

            menuButton.textContent =
                "⋯";

            const menu =
                document.createElement(
                    "div"
                );

            menu.className =
                "conversation-menu";

            const renameButton =
                document.createElement(
                    "button"
                );

            renameButton.type =
                "button";

            renameButton.className =
                "conversation-menu-item";

            renameButton.textContent =
                "Rename";

            const deleteButton =
                document.createElement(
                    "button"
                );

            deleteButton.type =
                "button";

            deleteButton.className =
                "conversation-menu-item delete";

            deleteButton.textContent =
                "Delete";

            renameButton.addEventListener(
                "click",
                (event) => {
                    event.stopPropagation();

                    startRenameConversation(
                        conversation,
                        item
                    );
                }
            );

            deleteButton.addEventListener(
                "click",
                (event) => {
                    event.stopPropagation();

                    deleteConversation(
                        conversation
                    );
                }
            );

            menuButton.addEventListener(
                "click",
                (event) => {
                    event.stopPropagation();

                    toggleConversationMenu(
                        menu
                    );
                }
            );

            menu.addEventListener(
                "click",
                (event) => {
                    event.stopPropagation();
                }
            );

            menu.appendChild(
                renameButton
            );

            menu.appendChild(
                deleteButton
            );

            actions.appendChild(
                menuButton
            );

            actions.appendChild(
                menu
            );

            item.appendChild(
                titleElement
            );

            item.appendChild(
                actions
            );

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

    conversationList.scrollTop =
        scrollTop;
}


document.addEventListener(
    "click",
    () => {
        closeConversationMenus();
    }
);


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

    closeConversationMenus();

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


function setSidebarCollapsed(
    collapsed
) {
    if (!sidebar) {
        return;
    }

    if (
        window.matchMedia(
            "(max-width: 700px)"
        ).matches
    ) {
        return;
    }

    sidebar.classList.toggle(
        "collapsed",
        collapsed
    );

    localStorage.setItem(
        "aria-sidebar-collapsed",
        collapsed ? "true" : "false"
    );

    closeConversationMenus();
}


function restoreSidebarState() {
    if (!sidebar) {
        return;
    }

    if (
        window.matchMedia(
            "(max-width: 700px)"
        ).matches
    ) {
        return;
    }

    const isCollapsed =
        localStorage.getItem(
            "aria-sidebar-collapsed"
        ) === "true";

    if (!isCollapsed) {
        return;
    }

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            sidebar.classList.add(
                "collapsed"
            );
        });
    });
}


function toggleSidebarCollapse() {
    if (!sidebar) {
        return;
    }

    if (
        window.matchMedia(
            "(max-width: 700px)"
        ).matches
    ) {
        return;
    }

    const isCollapsed =
        sidebar.classList.contains(
            "collapsed"
        );

    setSidebarCollapsed(
        !isCollapsed
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


if (collapseSidebarButton) {
    collapseSidebarButton.addEventListener(
        "click",
        toggleSidebarCollapse
    );
}


if (expandSidebarButton) {
    expandSidebarButton.addEventListener(
        "click",
        toggleSidebarCollapse
    );
}


/* ========================================
   New Chat
======================================== */

async function handleNewChat() {
    if (isLoading) {
        return;
    }

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


if (collapsedNewChatButton) {
    collapsedNewChatButton.addEventListener(
        "click",
        handleNewChat
    );
}


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
   Dynamic Greeting
======================================== */

async function loadGreeting() {
    try {
        const response =
            await fetch(
                "/api/chat/greeting/"
            );

        if (!response.ok) {
            return;
        }

        const data =
            await response.json();

        const greetingElement =
            document.querySelector(
                "#empty-state h1"
            );

        if (
            greetingElement &&
            data.greeting
        ) {
            greetingElement.textContent =
                data.greeting;
        }
    } catch (error) {
        console.error(
            "Failed to load greeting:",
            error
        );
    }
}


/* ========================================
   Initialization
======================================== */

restoreSidebarState();

async function initializeChat() {
    try {
        const conversations =
            await loadConversations();

        conversationListData =
            conversations;

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

    await loadGreeting();
}


initializeChat();