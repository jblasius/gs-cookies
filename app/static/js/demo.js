// NOTE: You must replace the client id on the following line.
//var clientId = '549821307845-9ef2xotqflhcqbv10.apps.googleusercontent.com';
var clientId = '176592896048-ver8bjf3errq8t0rcpe6htre8ol5tbqq.apps.googleusercontent.com';
var scopes = 'https://spreadsheets.google.com/feeds';

function init() {
  gapi.auth.authorize(
      {client_id: clientId, scope: scopes, immediate: true},
      handleAuthResult);
}

function handleAuthResult(authResult) {
  var authorizeButton = document.getElementById('authorize-button');
  if (authResult && !authResult.error) {
    authorizeButton.style.visibility = 'hidden';
    makeApiCall();
  } else {
    authorizeButton.style.visibility = '';
    authorizeButton.onclick = handleAuthClick;
  }
}

function handleAuthClick(event) {
  gapi.auth.authorize(
      {client_id: clientId, scope: scopes, immediate: false},
      handleAuthResult);
  return false;
}

function makeApiCall() {
  // Note: The below spreadsheet is "Public on the web" and will work
  // with or without an OAuth token.  For a better test, replace this
  // URL with a private spreadsheet.
  var tqUrl = 'https://docs.google.com/spreadsheets' +
//      '/d/1XWJLkAwch5GXAt_7zOFDcg8Wm8Xv29_8PWuuW15qmAE/gviz/tq' +
      '/d/1I8un3pP8aE3b2ixeQTN9mVPwMzTsE_TEkaFzAHEWZ-A/gviz/tq' +
      '?tq=select%20A%2C%20B%2C%20C%2C%20D%2C%20E' +
//      '?tqx=responseHandler:handleTqResponse' +
      '&access_token=' + encodeURIComponent(gapi.auth.getToken().access_token);

  document.write('<script src="' + tqUrl +'" type="text/javascript"></script>');
}

function handleTqResponse(resp) {
  document.write(JSON.stringify(resp));
}