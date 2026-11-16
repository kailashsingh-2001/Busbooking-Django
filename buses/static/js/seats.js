(function () {
  var form = document.getElementById('seat-form');
  if (!form) return;

  var price = parseInt(form.dataset.price, 10) || 0;
  var chosen = [];
  var chosenText = document.getElementById('chosen');
  var totalText = document.getElementById('total');
  var seatsInput = document.getElementById('seats-input');

  function render() {
    chosen.sort(function (a, b) { return a - b; });
    chosenText.textContent = chosen.length ? 'Seats ' + chosen.join(', ') : 'No seats selected';
    totalText.textContent = '₹' + (chosen.length * price).toLocaleString('en-IN');
    seatsInput.value = chosen.join(',');
  }

  form.querySelectorAll('.seat').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (btn.classList.contains('booked')) return;
      var n = parseInt(btn.dataset.seat, 10);
      var i = chosen.indexOf(n);
      if (i > -1) { chosen.splice(i, 1); } else { chosen.push(n); }
      btn.classList.toggle('selected');
      render();
    });
  });

  form.addEventListener('submit', function (e) {
    if (!chosen.length) {
      e.preventDefault();
      chosenText.textContent = 'Select at least one seat';
    }
  });
})();