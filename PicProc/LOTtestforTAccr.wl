


While[True ,

keyDir = "/var/www/html/PicProc/";
keyFile = "WKEY";
keyrt = FileNameJoin[{keyDir, keyFile}];
Print[FileByteCount[keyrt]];

If[ FileByteCount[keyrt] !=  3, 

	Print["log Math and thingspeak start"];
	SetDirectory["/var/www/html/PicProc/sig"];
	fn=FileNames["*.jpg"];
	sigData=Table[Import[a],{a,fn}];
	SetDirectory["/var/www/html/PicProc/con"];
	fn=FileNames["*.jpg"];
	conData=Table[Import[a],{a,fn}];
	oneoffn=First[fn];
	key=StringTake[oneoffn,16];
	imageDivide[img1_,img2_]:=Module[{work},
				 work=img2//ImageData//Map[Function[a,If[a==0.,1,1/a]],#,{2}]&//Image;
				 ImageMultiply[img1,work]
				 ];
	analysis[sig_,con_,gaussianFilterR_,erosionR_,fraction_]:=Module[{sigImg,conImg,threshold,mask,transmittance,transData,intensity,checkSaturation,saturationNumber},
								   sigImg=sig//ImageCrop[#,ImageDimensions[#]+20]&//GaussianFilter[#,gaussianFilterR]&;
								   conImg=con//ImageCrop[#,ImageDimensions[#]+20]&//GaussianFilter[#,gaussianFilterR]&;
								   threshold=sigImg//FindThreshold[#,Method->"Cluster"]&;
								   mask=sigImg//Binarize[#,threshold]&//Erosion[Pruning[#],DiskMatrix[erosionR]]&;
								   transmittance=imageDivide[sigImg,conImg]//ImageMultiply[#,mask]&;
								   transData=transmittance//ImageData//Flatten//DeleteCases[#,0.]&;
								   intensity=transData//TrimmedMean[#,fraction]&;
								   checkSaturation=transmittance//ImageData//Flatten;
								   saturationNumber=checkSaturation//Count[#,1.]&;
								   intensity
								 ];
	transmittance=analysis[sigData[[1]]//ColorSeparate[#,"RGB"]&//Part[#,2]&,conData[[1]]//ColorSeparate[#,"RGB"]&//Part[#,2]&,5,5,0.1];
	Import[URLBuild[{"http://localhost:3000","update"},{"key"->key,"field1"->transmittance*RandomReal[]}]];
	
	Print["log thingspeak OK"];
	
	ow=OpenWrite["/var/www/html/PicProc/WKEY"];
	Write[ow, -1];
	Close[ow];
	
, null];

Pause[2];

];
