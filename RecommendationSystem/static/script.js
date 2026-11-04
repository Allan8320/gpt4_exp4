
const profileForm = document.getElementById("profileForm");
const profileError = document.getElementById("profileError");
const generateButton = document.getElementById("generateButton");

const resultsPanel = document.getElementById("resultsPanel");
const chatPanel = document.getElementById("chatPanel");

const recommendationList = document.getElementById("recommendationList");
const explanationList = document.getElementById("explanationList");

const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");


function addMessage(message, type = "assistant") {
    const element = document.createElement("div");
    element.className = type === "user"
        ? "message user-message"
        : "message assistant-message";

    element.textContent = message;
    chatMessages.appendChild(element);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function showRecommendations(items) {
    recommendationList.replaceChildren();

    items.forEach((item, index) => {
        const card = document.createElement("article");
        card.className = "recommendation-card";

        const rank = document.createElement("div");
        rank.className = "rank-label";
        rank.textContent = `RANK #${index + 1}`;

        const title = document.createElement("h3");
        title.textContent = item.name;

        const description = document.createElement("p");
        description.textContent = item.description;

        const reason = document.createElement("p");
        reason.textContent = `Reason: ${item.reason}`;

        const scoreRow = document.createElement("div");
        scoreRow.className = "score-row";

        const scoreLabel = document.createElement("span");
        scoreLabel.textContent = "Suitability Score";

        const score = document.createElement("span");
        score.className = "score";
        score.textContent = `${item.score}/100`;

        scoreRow.append(scoreLabel, score);
        card.append(rank, title, description, reason, scoreRow);
        recommendationList.appendChild(card);
    });
}


function showExplanations(items) {
    explanationList.replaceChildren();

    items.forEach(item => {
        const container = document.createElement("div");
        container.className = "explanation-item";

        const title = document.createElement("h3");
        title.textContent = `${item.rank}. ${item.name}`;

        const explanation = document.createElement("p");
        explanation.textContent = item.explanation;

        container.append(title, explanation);
        explanationList.appendChild(container);
    });
}


function displayProfile(profile) {
    const details = Object.entries(profile)
        .map(([key, value]) => `${key.replaceAll("_", " ")}: ${value}`)
        .join("\n");

    addMessage(`Your profile:\n${details}`);
}


function handleResponse(data) {
    if (data.recommendations) {
        showRecommendations(data.recommendations);
        resultsPanel.classList.remove("hidden");
    }

    if (data.explanations) {
        showExplanations(data.explanations);
    }

    if (data.profile) {
        displayProfile(data.profile);
    }

    if (data.reply) {
        addMessage(data.reply);
    }

    if (data.message) {
        addMessage(data.message);
    }

    if (data.saved_file) {
        addMessage(`Saved file: ${data.saved_file}`);
    }

    if (data.exit) {
        chatInput.disabled = true;
        sendButton.disabled = true;
        addMessage("You can refresh the page to start a new session.");
    }
}


profileForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    profileError.textContent = "";
    generateButton.disabled = true;
    generateButton.textContent = "Generating recommendations...";

    const profile = {
        name: document.getElementById("name").value.trim(),
        age: Number(document.getElementById("age").value),
        background: document.getElementById("background").value.trim(),
        interests: document.getElementById("interests").value.trim(),
        skill_level: document.getElementById("skill_level").value,
        preferred_category: document.getElementById("preferred_category").value.trim(),
        goal: document.getElementById("goal").value.trim(),
        number_of_recommendations: Number(
            document.getElementById("number_of_recommendations").value
        )
    };

    try {
        const response = await fetch("/start", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(profile)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to generate recommendations.");
        }

        document.getElementById("profilePanel").classList.add("hidden");
        resultsPanel.classList.remove("hidden");
        chatPanel.classList.remove("hidden");

        handleResponse(data);

        chatPanel.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        profileError.textContent = error.message;
    } finally {
        generateButton.disabled = false;
        generateButton.innerHTML = 'Generate My Recommendations <span>→</span>';
    }
});


async function sendChatMessage(message) {
    if (!message.trim()) return;

    addMessage(message, "user");

    chatInput.value = "";
    sendButton.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to process your message.");
        }

        handleResponse(data);

    } catch (error) {
        addMessage(`Error: ${error.message}`);
    } finally {
        sendButton.disabled = false;
        chatInput.focus();
    }
}


chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await sendChatMessage(chatInput.value);
});


document.querySelectorAll(".quick-actions button").forEach(button => {
    button.addEventListener("click", async () => {
        await sendChatMessage(button.dataset.message);
    });
});
