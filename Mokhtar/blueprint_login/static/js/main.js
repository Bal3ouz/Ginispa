$(document).ready(function () {
//$('#dtBasicExample').DataTable();
$('#dtBasicExample').DataTable({
columnDefs: [{
orderable: false,
targets: 3
},{
orderable: false,
targets: 4
}]
});
$('.dataTables_length').addClass('bs-select');
});