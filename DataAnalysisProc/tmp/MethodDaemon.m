thepath = "./ChannelAndField";
randompath = "./randomArray/";
thesavepath = "./savedimage/";
getChannel[pathobj_] := (Stinngnum = StringSplit[obj, ","]; Channel2 = Stinngnum[[1]]; Return[Channel2])
getField[pathobj_] := (Stinngnum = StringSplit[obj, ","]; Field2 = Stinngnum[[2]]; Return[Field2])
getMethod[pathobj_] := (Stinngnum = StringSplit[obj, ","]; Method2 = Stinngnum[[3]]; Return[Method2])
getResult[pathobj_] := (Stinngnum = StringSplit[obj, ","]; Result2 = Stinngnum[[4]]; Return[Result2])

Method1L[pathobj_] := (
  Result = getResult[pathobj];
  Result1 = ToExpression[Result];
  Result2 = ToString[Result1];
  Field = getField[pathobj];
  Channel = getChannel[pathobj];
  Method11 = getMethod[pathobj];
  rannum = Random[Integer, {0, 99}];
  strr = ToString[rannum];
  Export[randompath <> "C" <> Channel <> "F" <> Field <> ".txt", rannum, "Text"] ; 
  integralURL = "http://192.168.2.212:3000/channels/" <> Channel <> "/fields/" <> Field <> ".json?results=" <> Result2 <> "";
  JsonData = Import[integralURL, "JSON"];
  Allfeeds = "feeds" /. JsonData;
  fieldid = "field" <> Field;
  AllData = fieldid /. Allfeeds // ToExpression;
  AllDataLength = AllData // Length; 
  fitfunction = Fit[AllData, {1, x}, x]; 
  FieldDirectory = "./savedimage/" <> Channel <> "/"<> Method11 <>"/"<> Result2 <> "/";
  If[DirectoryQ[FieldDirectory], null, CreateDirectory[FieldDirectory]]; 
  P = Show[ListPlot[AllData, PlotStyle -> Red], Plot[fitfunction, {x, 0, AllDataLength}]]; 
  Export["./savedimage/"<> Channel <>"/"<> Method11 <>"/"<> Result2 <>"/field"<> Field <>"_"<> strr <> ".png", P];
  )

Method2L[pathobj_] := (
  Result = getResult[pathobj];
  Result1 = ToExpression[Result];
  Result2 = ToString[Result1];
  Field = getField[pathobj];
  Channel = getChannel[pathobj];
  Method11 = getMethod[pathobj];
  rannum = Random[Integer, {0, 99}];
  strr = ToString[rannum];
  Export[randompath <> "C" <> Channel <> "F" <> Field <> ".txt", rannum, "Text"] ; 
  integralURL = "http://192.168.2.212:3000/channels/" <> Channel <> "/fields/" <> Field <> ".json?results=" <> Result2 <> "";
  JsonData = Import[integralURL, "JSON"];
  Allfeeds = "feeds" /. JsonData;
  fieldid = "field" <> Field;
  AllData = fieldid /. Allfeeds // ToExpression;
  AllDatasize = Length[AllData];
  AllDataMean = Mean[AllData];
  AllDatacenter = (Max[AllData] + Min[AllData])/2;
  model = a Sin[b x + c] + d;
  fit = FindFit[AllData, model, {{a, AllDatacenter}, {b, (2 Pi/1440)}, c, {d, AllDataMean}}, x];
  P = Show[Plot[Evaluate[model /. fit], {x, 0, AllDatasize}], ListPlot[{AllData}, PlotStyle -> Red]]; 
  FieldDirectory = "./savedimage/" <> Channel <> "/"<> Method11 <>"/"<> Result2 <> "/";
  If[DirectoryQ[FieldDirectory], null, CreateDirectory[FieldDirectory]]; 
  Export["./savedimage/"<> Channel <>"/"<> Method11 <>"/"<> Result2 <>"/field"<> Field <>"_"<> strr <> ".png", P];
  )

n = 1;
While[ True,
 If[FileExistsQ[thepath],
  obj = Import[thepath];
  DeleteFile[thepath];
  Method2 = getMethod[obj];
  
  (* Method 1 *)
  If[Method2 == "1",
   Print["M1"];
   Method1L[obj];
   ,null];
  
  (* Method 2 *)
  If[Method2 == "2",
   Print["M2"];
   Method2L[obj];
   ,null];
  
  (* Method 3 *)
  If[Method2 == "3",
   Print["M3"];
   ,null];
  
  ,null];
 Pause[1];
 ]
