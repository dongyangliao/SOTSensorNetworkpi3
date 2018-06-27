<?php
  if(is_array($_GET)&&count($_GET)>0)//
    {
        if(isset($_GET["channel"]) && isset($_GET["field"]) && isset($_GET["method"]) && isset($_GET["results"]) )//存在"id"
        {
            	$channelid=$_GET["channel"];//存在
		$fieldid=$_GET["field"];
		$methodid = $_GET["method"];
		$resultid = $_GET["results"];
		$fileurl = "./DataQueue";
		//echo $fileurl;
		//$filerecenturl = "./dispimage/recentCF".$channelid.".txt";
	    	//echo $filerecenturl;
		$myfile = fopen($fileurl, "a") or die("Unable to open file!");
		$txt = $channelid.",".$fieldid.",".$methodid.",".$resultid.",".$randomk."\n";
		fwrite($myfile, $txt);
		fclose($myfile);
		
		// prev code 
		//if(file_exists($filerecenturl))
		//{
    		//	echo "FILE".$filerecenturl."exzit\r\n";
		//	chmod($filerecenturl,0777);
		//}
		//else
		//{
   		//	echo "FILE".$filerecenturl."noexit\r\n";
    		//	$myfile = fopen($filerecenturl,"w");
    		//	fclose($myfile);
		//	chmod($filerecenturl,0777);
		//}
		
		//$resultCheck = file_get_contents('http://192.168.2.1:3000/channels/'.$channelid.'/fields/'.$fieldid.'/last.json');
		//$checkobj = json_decode($resultCheck);
		//$myfile = fopen($fileurl,"r");
		//$recentCF = fopen($filerecenturl,"r");
		//$checktxt = fread($myfile,"10");
		//$recentCFtxt = fread($recentCF,"10");
		//if($checkobj == "-1"){
    		//	print "NO exec";
			//$testfile = fopen("testb.txt","w") or die("Unable");
			//$text = "NO";
			//fwrite($testfile,$text);
			//fclose($testfile);
		//}elseif($checktxt == $recentCFtxt){
    		//	print "same as recent";
		//	
			//$testfile = fopen("testb.txt","w") or die("Unable");
			//$text = "Yes";
			//fwrite($testfile,$text);
			//fclose($testfile);
		//}else{
		//	print "exec";
		//	$lastentry = fopen("./dispimage/lastCFpy.txt","w");
		//	$topythontxt = $channelid.",".$fieldid;
		//	fwrite($lastentry,$topythontxt);
		//	fclose($lastentry);
		//}
		//fclose($myfile);
		//fclose($recentCF);
        }
    }
?>
