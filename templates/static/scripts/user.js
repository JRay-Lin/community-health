document.addEventListener("DOMContentLoaded", function () {
    const userSelect = document.getElementById("modify-user_id");
    const birthdayInput = document.getElementById("modify-birthday");
    const genderInput = document.getElementById("modify-gender");
    const heightInput = document.getElementById("modify-height");
    const newHealthSelect = document.getElementById("newHealth-user_id");
    const historyHealthSelect = document.getElementById(
        "historyHealth-user_id"
    );
    const deleteButton = document.getElementById("userDel-button");

    // Fetch and populate user list
    fetch("/userlist")
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            data.forEach((user) => {
                const option = document.createElement("option");
                option.value = user.id;
                option.textContent = user.name;
                userSelect.appendChild(option);
                newHealthSelect.appendChild(option.cloneNode(true));
                historyHealthSelect.appendChild(option.cloneNode(true));
            });
        })
        .catch((error) => console.error("Error fetching user list:", error));

    userSelect.addEventListener("change", function () {
        fetch("/userlist")
            .then((response) => response.json())
            .then((data) => {
                const selectedUser = data.find(
                    (user) => user.id == userSelect.value
                );
                if (selectedUser) {
                    birthdayInput.value = selectedUser.birthday;
                    genderInput.value = selectedUser.gender;
                    heightInput.value = selectedUser.height;
                }
            })
            .catch((error) =>
                console.error("Error fetching user data:", error)
            );
    });

    deleteButton.addEventListener("click", function (e) {
        e.preventDefault();
        const selectedUser = userSelect.value;
        if (selectedUser && confirm("確定要刪除此用戶嗎？")) {
            fetch(`/deleteuser/${selectedUser}`, {
                method: "POST",
            })
                .then((response) => {
                    if (response.ok) {
                        window.location.reload(); // 重新加載頁面或重定向到其他頁面
                    } else {
                        console.error("Failed to delete user.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        }
    });
});
