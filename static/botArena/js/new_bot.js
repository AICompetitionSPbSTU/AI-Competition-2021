    function uploadFile(file, s3Data, url){

      const xhr = new XMLHttpRequest();
      xhr.open('POST', s3Data.url);
      xhr.setRequestHeader('x-amz-acl', 'public-read');

      const postData = new FormData();
      for(key in s3Data.fields){
        postData.append(key, s3Data.fields[key]);
      }
      postData.append('file', file);

      xhr.onreadystatechange = () => {
        if(xhr.readyState === 4){
          if(xhr.status === 200 || xhr.status === 204){
            //ocument.getElementById('preview').src = url;
            document.getElementById("id_url_source").value = url;
          }
          else{
              document.getElementById("demo").innerHTML = xhr.status;
            alert('Could not upload file.'+xhr.status);
          }
        }
      };
      xhr.send(postData);
    }

    /*
      Function to get the temporary signed request from the Python app.
      If request successful, continue to upload the file using this signed
      request.
    */
    function getSignedRequest(file){
      const xhr = new XMLHttpRequest();
        //let game = document.getElementsByName("game_name");
        xhr.open('GET', "/botArena/sign-s3?file_name="+file.name+"&file_type="+file.type+"&game_name="+"{{ game_name }}");
      xhr.onreadystatechange = () => {
        if(xhr.readyState === 4){
          if(xhr.status === 200){
            const response = JSON.parse(xhr.responseText);
            uploadFile(file, response.data, response.url);
          }
          else{
              //
            alert('Could not get signed URL.');
          }
        }
      };
      xhr.send();
    }


    /*
       Function called when file input updated. If there is a file selected, then
       start upload procedure by asking for a signed request from the app.
    */
    function initUpload(){
      const files = document.getElementById('file-input').files;
      const file = files[0];
      document.getElementById("demo").innerHTML = 5 + 6;
      if(!file){
        return alert('No file selected.');
      }
      getSignedRequest(file);
    }

    /*
       Bind listeners when the page loads.
    */
    (() => {
        document.getElementById('submit').onclick = initUpload;
      // document.getElementById('file-input').onchange = initUpload;
    })();
