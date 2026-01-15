document.addEventListener("DOMContentLoaded", () => {
    const welcomeScreen = document.getElementById("welcome-screen");
    const pageContent = document.getElementById("page-content");

    // Default sichtbar machen, falls kein welcome-screen
    pageContent.style.opacity = welcomeScreen ? "0" : "1";

    if (welcomeScreen) {
        setTimeout(() => {
            welcomeScreen.classList.add("fade-out");

            setTimeout(() => {
                welcomeScreen.remove();
                pageContent.style.transition = "opacity 1.1s ease";
                pageContent.style.opacity = "1";
            }, 1200);

        }, 5000); // 5 Sekunden Anzeige
    }
});

document.querySelectorAll('.invisible-input').forEach(input => {
       input.addEventListener('input', () => {
           document.getElementById('save-bar').style.display = 'block';
       });
});

document.addEventListener('DOMContentLoaded', () => {
  const editModal = document.getElementById('editUserModal');
  if (!editModal) return;

  const editForm = document.getElementById('editUserForm');
  const editUserId = document.getElementById('editUserId');
  const editUsername = document.getElementById('editUsername');
  const editEmail = document.getElementById('editEmail');
  const editRole = document.getElementById('editRole');
  const editClassGroup = document.getElementById('editClassGroup');
  const editPhoneNumber = document.getElementById('editPhoneNumber');
  const editPosition = document.getElementById('editPosition');
  const editDepartment = document.getElementById('editDepartment');
  const editPicture = document.getElementById('editPicture');
  const cancelEdit = document.getElementById('cancelEdit');

  document.querySelectorAll('.user-action-edit[title="Bearbeiten"]').forEach(btn => {
    btn.addEventListener('click', () => {
      editUserId.value = btn.dataset.userId;
      editUsername.value = btn.dataset.username;
      editEmail.value = btn.dataset.email;
      editRole.value = btn.dataset.role;
      editClassGroup.value = btn.dataset.classGroup || '';
      editPhoneNumber.value = btn.dataset.phone || '';
      editPosition.value = btn.dataset.position || '';
      editDepartment.value = btn.dataset.department || '';
      editPicture.value = '';

      editModal.style.display = 'flex';
    });
  });

  cancelEdit.addEventListener('click', () => {
    editModal.style.display = 'none';
  });

  editModal.addEventListener('click', e => {
    if (e.target === editModal) editModal.style.display = 'none';
  });
});
