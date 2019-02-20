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
	Channel = strspt[[1]];
	Field = strspt[[2]];
	Method1 = strspt[[3]];
	Result = strspt[[4]];
	rannum = Random[Integer,{0,99}];
	If[Method1 == "1",
		strr = ToString[rannum];
		Print["Method1"]
		Export["./randomArray/C"<>Channel<>"F"<>Field,rannum,"Text"];
		integralURL = "http://localhost:3000/channels/" <> Channel <> "/fields/" <> Field <> ".json?results="<>Result;
		JsonData = Import[integralURL, "JSON"];
		Allfeeds = "feeds" /. JsonData;
		fieldid = "field" <> Field;
		AllData = fieldid /. Allfeeds // ToExpression;
		AllDataLength = AllData // Length;
		
		fitfunction = Fit[AllData, {1, x}, x];
                FieldDirectory = "./savedimage/" <> Channel <> "/"<> Method1 <>"/"<> Result <> "/";
                If[DirectoryQ[FieldDirectory], null , CreateDirectory[FieldDirectory]];
                P = Show[ListPlot[AllData, PlotStyle -> Red], Plot[fitfunction, {x, 0, AllDataLength}]];
		
		Export["./savedimage/"<> Channel <>"/"<> Method1 <>"/"<> Result <>"/field"<> Field <>"_"<> strr <> ".png", P];
		Print["Method1 end"]
	, null]
	
	If[Method1 == "2",
		strr = ToString[rannum];
		Print["Method2"]
		Export["./randomArray/C"<>Channel<>"F"<>Field,rannum,"Text"];
		
		integralURL = "http://localhost:3000/channels/" <> Channel <> "/fields/" <> Field <> ".json?results="<>Result;
		JsonData = Import[integralURL, "JSON"];
		Allfeeds = "feeds" /. JsonData;
		fieldid = "field" <> Field;
		AllData = fieldid /. Allfeeds // ToExpression;
		AllDatasize = Length[AllData];
		AllDataMean = Mean[AllData];
		AllDatacenter = (Max[AllData] + Min[AllData])/2;
		model = a Sin[b x + c] + d;
		fit = FindFit[AllData, model, {{a, AllDatacenter}, {b, (2 Pi/1440)}, c, {d, AllDataMean}},x];
		P = Show[Plot[Evaluate[model /. fit], {x, 0, AllDatasize}], ListPlot[{AllData}, PlotStyle -> Red]];
		
		FieldDirectory = "./savedimage/" <> Channel <> "/"<> Method1 <>"/"<> Result <> "/";
		If[DirectoryQ[FieldDirectory], null , CreateDirectory[FieldDirectory]];
		Export["./savedimage/"<> Channel <>"/"<> Method1 <>"/"<> Result <>"/field"<> Field <>"_"<> strr <> ".png", P];
		Print["Method2 end"]
	, null]
	
	If[Method1 == "3",
		strr = ToString[rannum];
		Print["Method3"];
		Export["./randomArray/C"<>Channel<>"F"<>Field,rannum,"Text"];
		
		graphlist={};
		graphxlist={};
		JsonData=None;
		For[i=1,i<9,i++, 
			integralURL="http://localhost:3000/channels/"<>Channel<>"/fields/"<>ToString[i]<>".json?results="<>Result;
			JsonData=Import[integralURL,"JSON"];
			allfeeds="feeds"/.JsonData;
			allchannels="channel"/.JsonData;
			mfield=ToString[i];
			fieldid="field"<>mfield;
			allData=fieldid/.allfeeds//ToExpression;
			fieldname=fieldid/.allchannels//ToExpression;
			alldataresized=DeleteCases[allData,Null];
			Length[alldataresized];
			If[Length[alldataresized]==0,
				Continue[],
				AppendTo[graphlist,Mean[alldataresized]];AppendTo[graphxlist,fieldname]
			];
		];
		graphlist1=Cases[graphlist,Except[_Symbol]];
		graphxlist1=Cases[graphxlist,Except[_Symbol]];
		glist=Transpose[{graphxlist1,graphlist1}];
		graphlist1length=graphlist1//Length;
		fitfunc=LinearModelFit[glist,{1, x},x];
		fitfunstr=ToString[fitfunc[{"BestFit","RSquared"}]];
		align[Left]={-2.5, -30};

		lText = Text[fitfunstr, {0.5, 0.6}, align[Left]];
		txt = Graphics[{lText}];
		P = Show[ListPlot[glist, PlotStyle -> Red], Plot[fitfunc["BestFit"], {x, First[graphxlist1], Last[graphxlist1]}], txt];
		
		FieldDirectory = "./savedimage/" <> Channel <> "/"<> Method1 <>"/"<> Result <> "/";
		If[DirectoryQ[FieldDirectory], null , CreateDirectory[FieldDirectory]];
		Export["./savedimage/"<> Channel <>"/"<> Method1 <>"/"<> Result <>"/field"<> Field <>"_"<> strr <> ".png", P];
		Print["Method3 end"]
	, null]
	
	Print[FileByteCount[keyrt]];
, null]

Pause[2];

]
