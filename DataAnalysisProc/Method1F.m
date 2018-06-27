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
   fitfunction = Fit[AllData, {1, x}, x];
   FieldDirectory = "./savedimage/" <> Channel <> "/"<> Method1 <>"/"<> Result <> "/";
   If[DirectoryQ[FieldDirectory], null , CreateDirectory[FieldDirectory]];
   P = Show[ListPlot[AllData, PlotStyle -> Red], Plot[fitfunction, {x, 0, AllDataLength}]];
   Export["./savedimage/"<> Channel <>"/"<> Method1 <>"/"<> Result <>"/field"<> Field <>"_"<> strr <> ".png", P];
   Quit

