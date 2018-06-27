   keyfile = "./dispimage/ChannelAndField.txt";
   obj = Import[keyfile];
   Stringnum = StringSplit[obj, ","];
   Channel = Stringnum[[1]];
   Field = Stringnum[[2]];
   Method1 = Stringnum[[3]];
   Result = Stringnum[[4]];
   integralURL = "http://192.168.2.1:3000/channels/" <> Channel <> "/fields/" <> Field <> ".json?results="<>Result;
   JsonData = Import[integralURL, "JSON"];
   Allfeeds = "feeds" /. JsonData;
   fieldid = "field" <> Field;
   AllData = fieldid /. Allfeeds // ToExpression;
   AllDataLength = AllData // Length;
   fitfunction = Fit[AllData, {1, x}, x];
   FieldDirectory = "./dispimage/" <> Channel <> "/"<> Method1 <>"/"<> Result <> "/";
   If[DirectoryQ[FieldDirectory], null , CreateDirectory[FieldDirectory]];
   P = Show[ListPlot[AllData, PlotStyle -> Red], Plot[fitfunction, {x, 0, AllDataLength}]];
   Export["./dispimage/"<> Channel <>"/"<> Method1 <>"/"<> Result <>"/field"<> Field <>".png", P];
   Quit

