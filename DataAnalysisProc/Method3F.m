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
   AllDataLength = AllData // Length;
   allData2 = Table[{i, AllData[[i]]}, {i, Length[AllData]}];
   model[x_] = ampl Evaluate[PDF[NormalDistribution[x0, sigma], x]];
   fit = FindFit[allData2, model[x], {{ampl, 1}, {x0, 0}, {sigma, 1}}, x];
   P = Show[ListPlot[allData2], Plot[model[x] /. fit, {x, 0, AllDataLength}, PlotStyle -> Red]];
   FieldDirectory = "./savedimage/" <> Channel <> "/"<> Method1 <>"/"<> Result <> "/";
   If[DirectoryQ[FieldDirectory], null , CreateDirectory[FieldDirectory]];
   Export["./savedimage/"<> Channel <>"/"<> Method1 <>"/"<> Result <>"/field"<> Field <>"_"<> strr <> ".png", P];
   Quit

