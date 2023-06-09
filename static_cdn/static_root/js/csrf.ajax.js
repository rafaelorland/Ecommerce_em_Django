 // This is the new way to do form ajax csrf token in django - Using Fetch API
$(document).ready(function(){
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie('csrftoken');
  console.log("CSRF Token:", csrftoken);

  function sendData(url, data, method='POST') {
    console.log("URL:", url);

    return fetch(url, {
      method: method,
      headers: {
        'X-CSRFToken': csrftoken,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      credentials: 'same-origin',
      body: JSON.stringify(data)
    });
  }
  const url = window.location.pathname;
  sendData(url)
});