<!DOCTYPE html>
<html>
<body>
  <link rel="stylesheet" type="text/css" href="static/style.css" media="screen" />
  <h1>Upload and monitor with serial interface</h1>
  
  <form action="/upload" method="post" enctype="multipart/form-data">
    Select a HEX File: <input type="file" name="upload" />
    <input type="submit" value="Start upload" />
  </form>

  <textarea disabled id="prog_text" rows="30" cols="50"> </textarea>
    
  <div id = "serial">
  
    <textarea id="sdata" rows="30" cols="50">
    </textarea>
    
    <a class="button" href="/serial" download="log.txt" >Save</a>
  </div>

  <script src="/static/jquery.min.js"></script>
  <script type="text/javascript" src="/static/script.js"></script>
  
</body>
</html>


<!--Category:      <input type="text" name="category" /> -->
