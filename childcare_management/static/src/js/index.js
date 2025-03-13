// Function to check if this JavaScript file has been loaded in the layout
function checkJsLoaded() {
  console.log("Childcare Management JS file has been loaded successfully!");
  // You can add more verification logic here if needed
  return true;
}
function checkPassword() {
  var password = document.getElementById("password").value;
  var confirmPassword = document.getElementById("confirmPassword").value;

  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return false;
  }
  return true;
}
// Execute the function when the document is ready
document.addEventListener("DOMContentLoaded", function () {
  checkJsLoaded();

  // Verificar si jQuery está disponible
  if (typeof jQuery !== "undefined") {
    console.log("jQuery is loaded!");

    // Código para manejar los botones de edición de perfil
    $(document).ready(function () {
      console.log("Script loaded"); // Para debug

      $("#editProfileBtn").on("click", function () {
        console.log("Edit button clicked"); // Para debug
        $("#profileViewMode").hide();
        $("#profileEditMode").show();
      });

      $("#cancelEditBtn").on("click", function () {
        console.log("Cancel button clicked"); // Para debug
        $("#profileEditMode").hide();
        $("#profileViewMode").show();
      });
    });
  } else {
    console.error(
      "jQuery is not loaded! The profile edit functionality won't work."
    );
  }
});
