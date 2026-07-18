const menuButton = document.querySelector("[data-menu]");
const navigation = document.querySelector("[data-nav]");
if (menuButton && navigation) {
    menuButton.addEventListener("click", () => navigation.classList.toggle("open"));
}

const roleSelect = document.querySelector("[data-role]");
const parentSection = document.querySelector("[data-parent-section]");
const studentFields = document.querySelectorAll(".student-field");
if (roleSelect && parentSection) {
    const toggleRole = () => {
        const isParent = roleSelect.value === "parent";
        parentSection.classList.toggle("hidden", !isParent);
        studentFields.forEach((field) => field.classList.toggle("hidden", isParent));
    };
    roleSelect.addEventListener("change", toggleRole);
    toggleRole();
}

document.querySelectorAll("[data-speak]").forEach((button) => {
    button.addEventListener("click", () => {
        if (!("speechSynthesis" in window)) {
            alert("이 브라우저는 영어 듣기를 지원하지 않습니다.");
            return;
        }
        speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(button.dataset.speak);
        utterance.lang = "en-US";
        utterance.rate = 0.82;
        speechSynthesis.speak(utterance);
    });
});

document.querySelectorAll("[data-recognize]").forEach((button) => {
    const target = document.getElementById(button.dataset.target);
    const status = document.querySelector(`[data-status-for="${button.dataset.target}"]`);
    button.addEventListener("click", () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            if (status) status.textContent = "음성인식은 Chrome 또는 Edge 브라우저에서 이용해 주세요.";
            return;
        }
        const recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        button.disabled = true;
        if (status) status.textContent = "듣고 있어요. 문장을 말해 주세요…";
        recognition.onresult = (event) => {
            target.value = event.results[0][0].transcript;
            target.dispatchEvent(new Event("input", { bubbles: true }));
            if (status) status.textContent = `인식 결과: ${target.value}`;
        };
        recognition.onerror = (event) => {
            const messages = {
                "not-allowed": "마이크 권한이 필요합니다. 브라우저 설정에서 허용해 주세요.",
                "no-speech": "음성이 들리지 않았어요. 다시 말해 주세요.",
                "network": "음성인식 네트워크에 연결하지 못했습니다."
            };
            if (status) status.textContent = messages[event.error] || "음성을 인식하지 못했습니다. 다시 시도해 주세요.";
        };
        recognition.onend = () => {
            button.disabled = false;
        };
        recognition.start();
    });
});

const quiz = document.querySelector("[data-quiz]");
if (quiz) {
    const updateProgress = () => {
        const names = [...new Set(Array.from(quiz.elements).filter((element) => element.name?.startsWith("answer_")).map((element) => element.name))];
        const answered = names.filter((name) => {
            const fields = quiz.querySelectorAll(`[name="${name}"]`);
            return Array.from(fields).some((field) => field.type === "radio" ? field.checked : field.value.trim());
        }).length;
        const counter = document.querySelector("[data-answered]");
        if (counter) counter.textContent = answered;
    };
    quiz.addEventListener("input", updateProgress);
    quiz.addEventListener("change", updateProgress);
    quiz.addEventListener("submit", (event) => {
        if (quiz.dataset.autoSubmit !== "true" && !confirm("답안을 제출하고 채점할까요? 제출 후에는 수정할 수 없습니다.")) event.preventDefault();
    });
}

const timerBox = document.querySelector("[data-timer]");
if (timerBox) {
    const timeLeftDisplay = timerBox.querySelector("[data-time-left]");
    const limitSeconds = parseInt(timerBox.dataset.limit, 10);
    const startedAt = new Date(timerBox.dataset.started);
    const autoFlag = document.querySelector("[data-auto-submit-flag]");
    const endTime = new Date(startedAt.getTime() + limitSeconds * 1000);
    let warned = false;

    const pad = (n) => String(n).padStart(2, "0");
    const tick = () => {
        const remaining = Math.max(0, Math.floor((endTime - Date.now()) / 1000));
        const hours = Math.floor(remaining / 3600);
        const minutes = Math.floor((remaining % 3600) / 60);
        const seconds = remaining % 60;
        if (timeLeftDisplay) timeLeftDisplay.textContent = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
        if (!warned && remaining <= 300 && remaining > 0) {
            warned = true;
            alert("시험 종료 5분 전입니다. 마무리해 주세요.");
        }
        if (remaining <= 0) {
            if (autoFlag) autoFlag.value = "1";
            const form = document.querySelector("[data-quiz]");
            if (form) {
                form.dataset.autoSubmit = "true";
                form.submit();
            }
        }
    };
    tick();
    setInterval(tick, 1000);
}