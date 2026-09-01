(function () {
    const container = document.querySelector("[data-listen-write]");
    if (!container) return;

    let allLessons = [];
    try {
        allLessons = JSON.parse(container.dataset.lessons || "[]");
    } catch (e) {
        console.error("Failed to parse lessons", e);
        return;
    }

    const levelSelect = container.querySelector('[data-filter="level"]');
    const categorySelect = container.querySelector('[data-filter="category"]');
    const card = container.querySelector("[data-card]");
    const empty = container.querySelector("[data-empty]");

    const els = {
        category: container.querySelector("[data-category]"),
        level: container.querySelector("[data-level]"),
        sentence: container.querySelector("[data-sentence]"),
        meaning: container.querySelector("[data-meaning]"),
        grammar: container.querySelector("[data-grammar]"),
        sentenceBox: container.querySelector("[data-sentence-box]"),
        answer: container.querySelector("[data-answer]"),
        feedback: container.querySelector("[data-feedback]"),
        listenBtn: container.querySelector("[data-listen]"),
        toggleTextBtn: container.querySelector("[data-toggle-text]"),
        checkBtn: container.querySelector("[data-check]"),
        nextBtn: container.querySelector("[data-next]"),
        prevBtn: container.querySelector("[data-prev]"),
        finishBtn: container.querySelector("[data-finish]"),
        current: container.querySelector("[data-current]"),
        total: container.querySelector("[data-total]"),
        progress: container.querySelector("[data-progress]"),
        score: container.querySelector("[data-score]"),
        attempts: container.querySelector("[data-attempts]"),
    };

    let index = 0;
    let showText = true;
    let checked = false;
    let isPlaying = false;
    let activeWord = -1;
    let timer = null;
    let answers = [];
    let score = 0;
    let attempts = 0;

    function getLessons() {
        const level = levelSelect.value;
        const category = categorySelect.value;
        return allLessons.filter((item) => {
            const matchLevel = level === "all" || item.level === level;
            const matchCategory = category === "all" || item.category === category;
            return matchLevel && matchCategory;
        });
    }

    function setQueryParams() {
        const params = new URLSearchParams();
        if (levelSelect.value !== "elementary") params.set("level", levelSelect.value);
        if (categorySelect.value !== "all") params.set("category", categorySelect.value);
        const query = params.toString();
        const url = query ? `${window.location.pathname}?${query}` : window.location.pathname;
        window.history.replaceState({}, "", url);
    }

    function normalize(text) {
        return text
            .toLowerCase()
            .replace(/[.,?!]/g, "")
            .replace(/\s+/g, " ")
            .trim();
    }

    function render() {
        const lessons = getLessons();
        els.total.textContent = lessons.length;

        if (lessons.length === 0) {
            card.classList.add("hidden");
            empty.classList.remove("hidden");
            return;
        }

        card.classList.remove("hidden");
        empty.classList.add("hidden");

        if (index >= lessons.length) index = lessons.length - 1;
        const item = lessons[index];

        els.current.textContent = index + 1;
        els.category.textContent = item.category;
        els.level.textContent = item.level === "elementary" ? "초등" : "중등";
        els.level.className = "level-badge " + item.level;
        els.meaning.textContent = item.ko;
        els.grammar.innerHTML = item.grammar
            .map((tag) => `<span class="grammar-tag">${escapeHtml(tag)}</span>`)
            .join("");
        els.answer.value = answers[index] || "";
        els.answer.disabled = false;
        els.answer.classList.remove("correct", "wrong");
        els.feedback.classList.add("hidden");
        els.feedback.textContent = "";
        checked = false;

        renderSentence(item.en);
        updateProgress();
        updateButtons();
    }

    function renderSentence(text) {
        const words = text.split(/\s+/);
        els.sentence.innerHTML = words
            .map((word, i) =>
                showText
                    ? `<span class="word" data-index="${i}">${escapeHtml(word)}</span>`
                    : `<span class="word hidden-text" data-index="${i}">${"•".repeat(word.length)}</span>`
            )
            .join(" ");
        els.toggleTextBtn.textContent = showText ? "글 숨기기" : "글 보이기";
    }

    function updateProgress() {
        const lessons = getLessons();
        const pct = lessons.length ? ((index + 1) / lessons.length) * 100 : 0;
        els.progress.style.width = `${pct}%`;
    }

    function updateButtons() {
        const lessons = getLessons();
        els.prevBtn.disabled = index === 0;
        if (checked) {
            els.checkBtn.classList.add("hidden");
            if (index < lessons.length - 1) {
                els.nextBtn.classList.remove("hidden");
                els.finishBtn.classList.add("hidden");
            } else {
                els.nextBtn.classList.add("hidden");
                els.finishBtn.classList.remove("hidden");
            }
        } else {
            els.checkBtn.classList.remove("hidden");
            els.nextBtn.classList.add("hidden");
            els.finishBtn.classList.add("hidden");
        }
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    function clearHighlightTimer() {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
    }

    function stopSpeech() {
        clearHighlightTimer();
        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
        }
        isPlaying = false;
        activeWord = -1;
        els.sentence.querySelectorAll(".word.active").forEach((el) => el.classList.remove("active"));
    }

    function speak(text) {
        if (!("speechSynthesis" in window)) {
            alert("이 브라우저는 영어 듣기를 지원하지 않습니다.");
            return;
        }
        stopSpeech();
        isPlaying = true;
        activeWord = 0;

        const words = text.split(/\s+/);
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.rate = 0.85;

        utterance.onboundary = (event) => {
            if (event.name === "word") {
                const spoken = text.slice(0, event.charIndex);
                const idx = spoken.trim().split(/\s+/).length - 1;
                highlightWord(idx);
            }
        };

        utterance.onend = () => {
            stopSpeech();
        };

        utterance.onerror = () => {
            stopSpeech();
        };

        window.speechSynthesis.speak(utterance);

        // Fallback for browsers with limited boundary support
        const estimatedMs = Math.max((text.length / 5) * 1000 * (1 / utterance.rate), words.length * 120);
        const step = Math.max(120, estimatedMs / words.length);
        let i = 0;
        const next = () => {
            if (!isPlaying) return;
            highlightWord(i);
            i += 1;
            if (i < words.length) {
                timer = setTimeout(next, step);
            } else {
                timer = setTimeout(() => stopSpeech(), step);
            }
        };
        next();
    }

    function highlightWord(idx) {
        els.sentence.querySelectorAll(".word.active").forEach((el) => el.classList.remove("active"));
        const word = els.sentence.querySelector(`[data-index="${idx}"]`);
        if (word) word.classList.add("active");
    }

    function checkAnswer() {
        const lessons = getLessons();
        if (!lessons.length) return;
        const item = lessons[index];
        const value = els.answer.value.trim();
        if (!value) return;

        answers[index] = value;
        const ok = normalize(value) === normalize(item.en);
        if (!checked) {
            attempts += 1;
            if (ok) score += 1;
        }
        checked = true;
        els.attempts.textContent = attempts;
        els.score.textContent = score;

        els.answer.disabled = true;
        els.answer.classList.toggle("correct", ok);
        els.answer.classList.toggle("wrong", !ok);
        els.feedback.classList.remove("hidden", "correct", "wrong");
        els.feedback.classList.add(ok ? "correct" : "wrong");
        els.feedback.textContent = ok
            ? "정답이에요! Great job!"
            : `정답은 "${item.en}" 이에요.`;

        updateButtons();
    }

    function goNext() {
        const lessons = getLessons();
        if (index < lessons.length - 1) {
            index += 1;
            render();
        }
    }

    function goPrev() {
        if (index > 0) {
            index -= 1;
            render();
        }
    }

    function finish() {
        const form = document.getElementById("finish-form");
        const inputs = document.getElementById("finish-inputs");
        if (!form || !inputs) return;
        inputs.innerHTML = "";
        const lessons = getLessons();
        lessons.forEach((item, i) => {
            const ans = answers[i] || "";
            inputs.appendChild(createHiddenInput("answer", ans));
            inputs.appendChild(createHiddenInput("correct", item.en));
        });
        form.submit();
    }

    function createHiddenInput(name, value) {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = name;
        input.value = value;
        return input;
    }

    function onFilterChange() {
        setQueryParams();
        index = 0;
        answers = [];
        score = 0;
        attempts = 0;
        els.score.textContent = "0";
        els.attempts.textContent = "0";
        render();
    }

    levelSelect.addEventListener("change", onFilterChange);
    categorySelect.addEventListener("change", onFilterChange);

    els.listenBtn.addEventListener("click", () => {
        const lessons = getLessons();
        if (!lessons.length) return;
        speak(lessons[index].en);
    });

    els.toggleTextBtn.addEventListener("click", () => {
        showText = !showText;
        const lessons = getLessons();
        if (lessons.length) renderSentence(lessons[index].en);
    });

    els.checkBtn.addEventListener("click", checkAnswer);
    els.nextBtn.addEventListener("click", goNext);
    els.prevBtn.addEventListener("click", goPrev);
    els.finishBtn.addEventListener("click", finish);

    els.answer.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            if (checked) {
                const lessons = getLessons();
                if (index < lessons.length - 1) goNext();
                else finish();
            } else {
                checkAnswer();
            }
        }
    });

    window.addEventListener("beforeunload", stopSpeech);

    render();
})();
