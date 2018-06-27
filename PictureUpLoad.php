<?php
   $local_path = "./PicProc/Cache/";
   if(!is_dir($local_path)){
     mkdir($local_path,0777,true);
   }
   $img_name = basename($_FILES["uploadedfile"]["name"]);
   $target_path = $local_path.$img_name;
   $result = move_uploaded_file($_FILES["uploadedfile"]["tmp_name"],$target_path);
    if($result){
         echo "The file has been uploaded";
   	}else{
	     echo "failed";
   	}
?>
