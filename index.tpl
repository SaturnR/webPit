<!doctype html>
<title>jQuery Example</title>
<script type="text/javascript"
  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type="text/javascript">
  var $SCRIPT_ROOT = "{{ request.script_name }}";
</script>

<script type="text/javascript">
  $(function() {
    var submit_form = function(e) {
      $.getJSON($SCRIPT_ROOT + '_add_numbers', {
        a: $('input[name="a"]').val(),
      }, function(data) {
        $('#result').text(data.result);
      });
      return false;
    };

    $('a#calculate').bind('click', submit_form);
  });
</script>
<p>
  <input type="text" size="5" name="a"> +
  <span id="result">?</span>
<p><a href=# id="calculate">calculate server side</a>
</body>
</html>
