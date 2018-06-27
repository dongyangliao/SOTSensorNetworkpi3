   keyfile = "./ChannelAndField";
   obj = Import[keyfile];
   Stringnum = StringSplit[obj, ","];
   Channel = Stringnum[[1]];
   Field = Stringnum[[2]];
   Method1 = Stringnum[[3]];
   Result = Stringnum[[4]];
   rannum = Random[Integer,{0,99}];
   strr = ToString[rannum];
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
   Quit

