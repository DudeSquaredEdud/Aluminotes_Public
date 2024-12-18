class AlertBox {
  // the actual function
  static show(Message) {
    let alert_box = document.getElementById('alert_box');
    let visible = false; // used to prevent jankyness
    // remove on click
    alert_box.onclick = () => {
      if (visible == true) alert_box.classList.toggle('fade');
      visible = false;
    };
    alert_box.innerHTML = Message;
    visible = true;
    alert_box.classList.toggle('fade');
    setTimeout(function () {
      if (visible == true) {
        // only toggle if it's actually visible
        alert_box.classList.toggle('fade');
        visible = false;
      }
    }, 5000);
  }
}
