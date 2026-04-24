const form = document.getElementById("form");

let subjects = JSON.parse(localStorage.getItem("subjects")) || [];

window.onload = () => {
    render();
};

function addSubject() {
    const subject = document.getElementById("subject").value.trim();
    const short = document.getElementById("short").value.trim();
    const professor = document.getElementById("professor").value.trim();
    const message = document.getElementById("message").value.trim();

    if (!subject || !short || !professor || !message) {
        alert("모든 값을 입력하세요");
        return;
    }

    subjects.push({
        subject,
        short,
        professor,
        message
    });

    saveSubjects();
    render();

    document.getElementById("subject").value = "";
    document.getElementById("short").value = "";
    document.getElementById("professor").value = "";
    document.getElementById("message").value = "";
}

function removeSubject(index) {
    subjects.splice(index, 1);
    saveSubjects();
    render();
}

function saveSubjects() {
    localStorage.setItem("subjects", JSON.stringify(subjects));
}

function render() {
    const list = document.getElementById("list");
    list.innerHTML = "";

    if (subjects.length === 0) {
        list.innerHTML = "<p>등록된 과목이 없습니다</p>";
        return;
    }

    subjects.forEach((s, i) => {
        list.innerHTML += `
            <div style="margin-bottom:10px; padding:8px; border:1px solid #ddd;">
                <b>${s.subject}</b> (${s.professor})<br>
                <small>${s.short}</small><br>
                <button onclick="removeSubject(${i})" style="border-radius: 5px; border: none; background: #0095f6; color: white; cursor: pointer;">삭제</button>
            </div>
        `;
    });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    try {
        const formData = new FormData(form);

        formData.append("subjects", JSON.stringify(subjects));

        const res = await fetch("/run", {
            method: "POST",
            body: formData
        });

        const text = await res.text();

        if (!res.ok) {
            throw new Error("서버 에러: " + res.status + " / " + text);
        }

        const data = JSON.parse(text);
        alert(data.message);

    } catch (err) {
        console.error(err);
        alert(err.message);
    }
});