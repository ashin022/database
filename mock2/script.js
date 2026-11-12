const form = document.getElementById("studentForm");
let students = JSON.parse(localStorage.getItem("students")) || [];
let editIndex = -1;

function show(list = students) {
  const tbody = document.getElementById("studentTableBody");
  tbody.innerHTML = "";
  document.getElementById("studentCount").innerText = list.length;
  document.getElementById("noStudents").style.display = list.length? "none" : "block";
  list.forEach(s => {
    tbody.innerHTML += `<tr>
      <td>${s.id}</td><td>${s.name}</td><td>${s.email}</td>
      <td>${s.course}</td><td>${s.phone}</td>
      <td>
        <button class="edit-btn" onclick="editS('${s.id}')">Edit</button>
        <button class="delete-btn" onclick="delS('${s.id}')">Delete</button>
      </td></tr>`;
  });
}

function save() {
  localStorage.setItem("students", JSON.stringify(students));
  show();
}

form.onsubmit = e => {
  e.preventDefault();
  let id = studentId.value.trim();
  let name = studentName.value.trim();
  let mail = email.value.trim();
  let crs = course.value;
  let ph = phone.value.trim();

  if (!id ||!name ||!mail ||!crs ||!ph) { alert("Fill all fields"); return; }
  if (students.some((s,i)=> s.id==id && i!=editIndex)) { alert("ID already exists"); return; }

  let data = {id, name, email: mail, course: crs, phone: ph};

  if (editIndex >= 0) students[editIndex] = data;
  else students.push(data);

  save(); form.reset(); editIndex = -1;
  formTitle.innerText = "Add Student";
  submitBtn.innerText = "Add Student";
};
  

show();

