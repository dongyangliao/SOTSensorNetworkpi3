<?php
    header("Access-Control-Allow-Origin: *");
    //header("Content-Type: application/json");
    if(is_array($_GET)&&count($_GET)>0){
		if(isset($_GET["channel"]) && isset($_GET["field"]) )//存在"id"
		{
			$channelid=$_GET["channel"];
			$fieldid=$_GET["field"];
			$fnn= "./randomArray/C".$channelid."F".$fieldid;
			//echo $fnn;
			$hdd = fopen($fnn,"r") or die("Unable to open file");
			$contentss = fread($hdd,filesize($fnn));
			//echo $contentss;
			$intconts = (int) $contentss;
			//echo $intconts;
			$item =(string) $intconts;
			//echo $item;
			$myobj->iid = $item;
			$myjson = json_encode($myobj);
			echo $myjson;
		}
	}
    
    //$fn = "./rand_num";
    //$hd = fopen($fn,"r") or die("Unable to open file");
    //$contents = fread($hd,filesize($fn));
    //fclose($hd);
    //echo $contents;
    //$intcont = (int) $contents;
    //$item =(string) $intcont;
    //$myobj->iid = $item;
    //$myobj->iid = "56";
    //$myjson = json_encode($myobj);
    //echo $myjson
    //$data = '{"iid": "23" }';
    //echo json_encode($data);
?>
