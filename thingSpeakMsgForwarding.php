<?php
   
  if(is_array($_GET)&&count($_GET)>0){
        
        if(isset($_GET["sid"])){
			$sid=$_GET["sid"];
			$url1 = 'http://192.168.2.'.$sid.':3000/update?';
			if(isset($_GET["key"])){
				$key1=$_GET["key"];
				$url1 = $url1.'key='.$key1;
				if(isset($_GET["field1"])){
					$field1=$_GET["field1"];
					printf("field1\n");
					$url1 = $url1.'&field1='.$field1;
					//printf($url1);
				}
				if(isset($_GET["field2"]))
				{
					$field2=$_GET["field2"];
					printf("field2\n");
					$url1 = $url1.'&field2='.$field2;
					//printf($url1);
				}
				if(isset($_GET["field3"]))
				{
					$field3=$_GET["field3"];
					printf("field3\n");
					$url1 = $url1.'&field3='.$field3;
					//printf($url1);
				}
				if(isset($_GET["field4"]))
				{
					$field4=$_GET["field4"];
					printf("field4\n");
					$url1 = $url1.'&field4='.$field4;
					//printf($url1);
				}
				if(isset($_GET["field5"]))
				{
					$field5=$_GET["field5"];
					printf("field5\n");
					$url1 = $url1.'&field5='.$field5;
					//printf($url1);
				}
				if(isset($_GET["field6"]))
				{
					$field6=$_GET["field6"];
					printf("field6\n");
					$url1 = $url1.'&field6='.$field6;
					//printf($url1);
				}
				if(isset($_GET["field7"]))
				{
					$field7=$_GET["field7"];
					printf("field7\n");
					$url1 = $url1.'&field7='.$field7;
					//printf($url1);
				}
				if(isset($_GET["field8"]))
				{
					$field8=$_GET["field8"];
					printf("field8\n");
					$url1 = $url1.'&field8='.$field8;
					//printf($url1);
				}
				printf($url1);
				$html = file_get_contents($url1);
				echo $html;
			}
		}
    }
?>
