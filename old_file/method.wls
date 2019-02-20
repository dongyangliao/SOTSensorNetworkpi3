#!/usr/bin wolframscript

While[True ,

keyDir = "./";
keyFile = "ChannelAndField";
keyrt = FileNameJoin[{keyDir, keyFile}];
Print[FileByteCount[keyrt]]
If[ FileByteCount[keyrt] !=  3, 
	readobj = OpenRead[keyrt];
	strobj = ReadLine[readobj];
	Close[readobj];
	ow=OpenWrite[keyrt];
	Write[ow, -1];
	Close[ow];
	strspt = StringSplit[strobj, ","];
	ch = strspt[[1]];
	Print[ch];
	fd = strspt[[2]];
	Print[fd];
	mh = strspt[[3]];
	Print[mh];
	rs = strspt[[4]];
	Print[rs];
	If[mh == "1",
		rannum = Random[Integer,{0,99}];
		strr = ToString[rannum];
		Export["./randomArray/C"<>Channel<>"F"<>Field,rannum,"Text"];
		integralURL = "http://localhost:3000/channels/" <> ch <> "/fields/" <> fd <> ".json?results="<>rs;
		JsonData = Import[integralURL, "JSON"];
		Allfeeds = "feeds" /. JsonData;
		fieldid = "field" <> fd;
		AllData = fieldid /. Allfeeds // ToExpression;
		AllDataLength = AllData // Length;
		fitfunction = Fit[AllData, {1, x}, x];
		FieldDirectory = "./dispimage/" <> Channel <> "/"<> Method1 <>"/"<> Result <> "/";
		If[DirectoryQ[FieldDirectory], null , CreateDirectory[FieldDirectory]];
		P = Show[ListPlot[AllData, PlotStyle -> Red], Plot[fitfunction, {x, 0, AllDataLength}]]
		Export["./dispimage/"<> Channel <>"/"<> Method1 <>"/"<> Result <>"/field"<> fd <>".png", P];
		(*Export["./fd" <> fd <> ".png", P];*)
	, null]
	Print[FileByteCount[keyrt]];
, null]

Pause[2];

]
