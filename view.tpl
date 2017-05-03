<!DOCTYPE html>
<html>
<body>
  <link rel="stylesheet" type="text/css" href="static/style.css" media="screen" />
  <h1>Upload and monitor with serial interface</h1>
  
  <form action="/upload" method="post" enctype="multipart/form-data">
    Select a HEX File: <input type="file" name="upload" /><br><br>
    Erase: <input type="checkbox" name="erase" value="true" checked><br><br>
    Fuse bits <input id = "checkbox_fuses" type="checkbox" name="program_fuses" value="true"/><br>
    <div id="fuses">
      Low: <input type="text" size = 2 name="low_fuses" value="EF"/><br>
      High: <input type="text" size = 2 name="high_fuses" value="D8"/><br>
      Ext: <input type="text" size = 2 name="ext_fuses" value="FF"/><br>
    </div>
    <br>
    <br>
    <input type="submit" name = "upload" value="Upload" />
    <input type="submit" name = "download" value="Read" />
    <input type="submit" name = "lock_read" value="Lock read" />
  </form>
  
  
  <textarea disabled id="prog_text" rows="30" cols="50"> </textarea>
    
  <div id = "serial">
    <textarea id="sdata" rows="30" cols="50"> </textarea>
    <input type="checkbox" id="auto_scroll" name = "auto_scroll" value="auto scroll" checked/>
    <a class="button" href="/serial" download="log.txt" >Save</a>
    <a class="button" href="/clear">Clear</a>
  </div>

  <script src="/static/jquery.min.js"></script>
  <script type="text/javascript" src="/static/script.js"></script>
  
</body>
</html>


<!--Category:      <input type="text" name="category" /> -->
