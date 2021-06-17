$(function() {
    $('#Telegram').change(function() {
      $('#telegram-event').html('Toggle: ' + $(this).prop('checked'))
    })
  })