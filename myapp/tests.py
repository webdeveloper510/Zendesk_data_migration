import pandas as pd
import re

# Create a DataFrame with your data
data = {'column': ['INV 31/10/2019', 'NA', 'DT 02/10/2020', '04/10/22']}
df = pd.DataFrame(data)

# Define a function to remove alpha items before the date using regex
def remove_alpha(text):
    if isinstance(text, str):  # Check if input is a string
        return re.sub(r'^.*?(\d{1,2}/\d{1,2}/\d{2,4}).*', r'\1', text)
    else:
        return str(text)

# Apply the function to the DataFrame
df['column'] = df['column'].apply(remove_alpha)

# Convert the date format to YYYY-MM-DD
df['column'] = pd.to_datetime(df['column'], dayfirst=True).dt.strftime('%Y-%m-%d')

# Output the modified DataFrame
print(df)



# def test(request):
#     base_url = "https://yokohama-atg.zendesk.com/api/v2/users/"
#     username = "sreevidya@godigitalcx.com"
#     password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
#     auth_string = f"{username}/token:{password}"
#     encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
#     headers = {
#         "Content-Type": "application/json",
#         'Authorization': f'Basic {encoded_auth}'
#     }
    
#     user_ids = [23264123084177, 23264123084305, 23264123084433, 23264123084561, 23264123084689, 23264123084817, 23264123084945, 23264123085073, 23264123085201, 23264123085329, 23264123085457, 23264123085585, 23264123085713, 23264123085841, 23264123085969, 23264123086097, 23264123086225, 23264123086353, 23264123086481, 23264123086609, 23264123086737, 23264123086865, 23264130609937, 23264130610065, 23264130610193, 23264130610321, 23264130610449, 23264130610577, 23264130610705, 23264130610833, 23264130610961, 23264130611089, 23264130611217, 23264130611345, 23264130611473, 23264130611601, 23264130611729, 23264130611857, 23264130611985, 23264130612113, 23264130612241, 23264130612369, 23264130612497, 23264130612625, 23264130612753, 23264130612881, 23264130613009, 23264130613137, 23264130613265, 23264130613393, 23264130613521, 23264130613649, 23264130613777, 23264130613905, 23264134659345, 23264134659473, 23264134659601, 23264134676241, 23264137773201, 23264137773329, 23264137773457, 23264137773585, 23264137773713, 23264137773841, 23264137773969, 23264137774097, 23264137774225, 23264137774353, 23264137774481, 23264137774609, 23264137774737, 23264137774865, 23264137774993, 23264137775121, 23264137775249, 23264137775377, 23264137775505, 23264137775633, 23264137775761, 23264137775889, 23264137776017, 23264137776145, 23264137776273, 23264137776401, 23264137776529, 23264137776657, 23264137776785, 23264137776913, 23264137777041, 23264137777169, 23264137777297, 23264137777425, 23264137777553, 23264137777681, 23264137777809, 23264137777937, 23264137778065, 23264137778193, 23264137778321, 23264137778449, 23264137778577, 23264137778705, 23264137778833, 23264137778961, 23264137779089, 23264137779217, 23264137779345, 23264137779473, 23264137779601, 23264137779729, 23264137779857, 23264137779985, 23264137780113, 23264137780241, 23264137780369, 23264137780497, 23264137780625, 23264137780753, 23264137780881, 23264137781009, 23264137781137, 23264137781265, 23264137781393, 23264137781521, 23264137781649, 23264137781777, 23264137781905, 23264137782161, 23264137782289, 23264137782417, 23264137782545, 23264137782673, 23264137782801, 23264137782929, 23264137783057, 23264137783185, 23264137783313, 23264137783441, 23264137783569, 23264137783697, 23264137783825, 23264137783953, 23264138045201, 23264138045329, 23264138045457, 23264138045585, 23264138045713, 23264138045841, 23264138045969, 23264138046097, 23264138046225, 23264138046353, 23264138046481, 23264138046609, 23264140259217, 23264140259345, 23264140259473, 23264140259601, 23264140259729, 23264140259857, 23264140259985, 23264140260113, 23264140260241, 23264140260369, 23264140260497, 23264140260625, 23264140260753, 23264140260881, 23264140261009, 23264140261137, 23264140261265, 23264140261393, 23264140261521, 23264140261649, 23264140261777, 23264140261905, 23264140262033, 23264140262161, 23264140262289, 23264140262417, 23264140262545, 23264140262673, 23264140262801, 23264140262929, 23264140263057, 23264140263185, 23264140263313, 23264140263441, 23264140263569, 23264140263697, 23264140263825, 23264140263953, 23264142458897, 23264142459025, 23264142459153, 23264142459281, 23264142459409, 23264142459537, 23264142459665, 23264142459793, 23264142459921, 23264142460049, 23264142460177, 23264142460305, 23264142460433, 23264142460561, 23264142460689, 23264142460817, 23264142460945, 23264142461073, 23264142461201, 23264142461329, 23264142461457, 23264142461585, 23264142461713, 23264142461841, 23264142461969, 23264142462097, 23264142462225, 23264142462353, 23264142462481, 23264142462609, 23264142462737, 23264142462865, 23264142462993, 23264142463121, 23264142463249, 23264142463377, 23264142463505, 23264142463633, 23264142463761, 23264142463889, 23264142464017, 23264142464145, 23264142464273, 23264142464401, 23264142464529, 23264152798097, 23264152798225, 23264152798353, 23264152798481, 23264152798609, 23264152798737, 23264152798865, 23264152798993, 23264152799121, 23264152799249, 23264152799377, 23264152799505, 23264152799633, 23264152799761, 23264152799889, 23264152800017, 23264152800145, 23264152800273, 23264152800401, 23264152800529, 23264152800657, 23264152800785, 23264152800913, 23264152801041, 23264152801169, 23264152801297, 23264152801425, 23264152801553, 23264152801681, 23264152801809, 23264152801937, 23264152802065, 23264152802193, 23264152802321, 23264152802449, 23264152802577, 23264152802705, 23264152802833, 23264152802961, 23264152803089, 23264152803217, 23264152803345, 23264152803473, 23264152803601, 23264152803729, 23264152803857, 23264152803985, 23264152804113, 23264152804241, 23264152804369, 23264152804497, 23264152804625, 23264152804753, 23264152804881, 23264152805009, 23264152805137, 23264152805265, 23264152805393, 23264152805521, 23264152805649, 23264152805777, 23264152805905, 23264152806033, 23264152806161, 23264152806289, 23264152806417, 23264152806545, 23264152806673, 23264152806801, 23264152806929, 23264152807057, 23264152807185, 23264152807313, 23264152807441, 23264152807569, 23264152807697, 23264152807825, 23264152807953, 23264156435985, 23264156436113, 23264156436241, 23264156436369, 23264156436497, 23264156436625, 23264156436753, 23264156436881, 23264156437009, 23264156437137, 23264156437265, 23264156437393, 23264156437521, 23264156437649, 23264156437777, 23264156437905, 23264156438033, 23264157055505, 23264157055633, 23264157055761, 23264157055889, 23264157056017, 23264157056145, 23264157056273, 23264157056401, 23264158411665, 23264158411793, 23264158411921, 23264158412049, 23264158412177, 23264158412305, 23264158412433, 23264158412561, 23264158412689, 23264158412817, 23264158412945, 23264158413073, 23264158413201, 23264158413329, 23264158413457, 23264158413585, 23264158413713, 23264158413841, 23264158413969, 23264158414097, 23264158414225, 23264158414353, 23264158414481, 23264158414609, 23264158414737, 23264158414865, 23264158414993, 23264158415121, 23264158415249, 23264158415377, 23264158415505, 23264158415633, 23264158415761, 23264158415889, 23264158416017, 23264158416145, 23264158416273, 23264158416401, 23264158416529, 23264158416657, 23264158416785, 23264158416913, 23264158417041, 23264158417169, 23264158417297, 23264158417425, 23264158417553, 23264158417681, 23264158417809, 23264158417937, 23264158418065, 23264158418193, 23264158418321, 23264158418449, 23264158418577, 23264158418705, 23264158418833, 23264158418961, 23264161464465, 23264161464593, 23264161464721, 23264161464849, 23264161464977, 23264161465105, 23264161465233, 23264161465361, 23264161465489, 23264161465617, 23264161465745, 23264161465873, 23264161466001, 23264161466129, 23264161466257, 23264161466385, 23264161466513, 23264161466641, 23264161466769, 23264161466897, 23264161467025, 23264161467153, 23264161467281, 23264161467409, 23264161467537, 23264161467665, 23264161467793, 23264161467921, 23264161468049, 23264161468177, 23264161468305, 23264177603473, 23264177603601, 23264177603729, 23264177603857, 23264177603985, 23264178317585, 23264179139601, 23264179139729, 23264179139857, 23264179139985, 23264179140113, 23264179140241, 23264179140369, 23264179140497, 23264179140625, 23264179140753, 23264179140881, 23264179141009, 23264179141137, 23264179141265, 23264179141393, 23264179141521, 23264179141649, 23264179141777, 23264179141905, 23264179142033, 23264181849233, 23264181849361, 23264181849489, 23264181849617, 23264181849745, 23264181849873, 23264181850001, 23264181850129, 23264181850257, 23264181850385, 23264181850513, 23264181850641, 23264181850769, 23264181850897, 23264181851025, 23264181851153, 23264181851281, 23264181851409, 23264181851537, 23264181851665, 23264181851793, 23264181851921, 23264181852049, 23264181852177, 23264181852305, 23264181852433, 23264181852561, 23264181852689, 23264181852817, 23264181852945, 23264181853073, 23264181853201, 23264181853329, 23264181853457, 23264181853585, 23264181853713, 23264181853841, 23264181853969, 23264181854097, 23264181854225, 23264181854353, 23264181854481, 23264181854609, 23264181854737, 23264181854865, 23264181854993, 23264181855121, 23264181855249, 23264181855377, 23264181855505, 23264197153425, 23264197153553, 23264197153681, 23264197153809, 23264197153937, 23264197154065, 23264197154193, 23264197154321, 23264197154449, 23264197154577, 23264197154705, 23264197154833, 23264197154961, 23264197155089, 23264197155217, 23264197155345, 23264197155473, 23264197155601, 23264197155729, 23264197155857, 23264197155985, 23264197156113, 23264197156241, 23264197156369, 23264197156497, 23264210887057, 23264210887185, 23264210887313, 23264210887441, 23264210887569, 23264210887697, 23264210887825, 23264210887953, 23264210888081, 23264210888209, 23264210888337, 23264210888465, 23264210888593, 23264210888721, 23264210888849, 23264210888977, 23264210889105, 23264210889233, 23264210889361, 23264210889489, 23264210889617, 23264210889745, 23264210889873, 23264210890001, 23264210890129, 23264210890257, 23264210890385, 23264210890513, 23264210890641, 23264210890769, 23264210890897, 23264210891025, 23264210891153, 23264210891281, 23264210891409, 23264210891537, 23264210891665, 23264210891793, 23264216313233, 23264216313361, 23264216313489, 23264216313617, 23264216313745, 23264216313873, 23264217176593, 23264217176721, 23264217176849, 23264217176977, 23264217177105, 23264217177233, 23264217177361, 23264217177489, 23264217177617, 23264217177745, 23264217177873, 23264217178001, 23264217178129, 23264217178257, 23264217178385, 23264217178513, 23264217178641, 23264217178769, 23264217178897, 23264217179025, 23264217179153, 23264217179281, 23264217179409, 23264217179537, 23264217179665, 23264217179793, 23264217179921, 23264217180049, 23264217180177, 23264217180305, 23264217180433, 23264217180561, 23264217180689, 23264217180817, 23264217180945, 23264217181073, 23264217181201, 23264217181329, 23264217181457, 23264217181585, 23264217181713, 23264217181841, 23264217181969, 23264217182097, 23264217182225, 23264217182353, 23264217182481, 23264217182609, 23264217182737, 23264217182865, 23264217182993, 23264217183121, 23264217183249, 23264217183377, 23264217183505, 23264217183633, 23264217183761, 23264218529297, 23264222691089, 23264222691217, 23264222691345, 23264222691473, 23264222691601, 23264222691729, 23264222691857, 23264222691985, 23264222692113, 23264222692241, 23264222692369, 23264222692497, 23264222692625, 23264222692753, 23264222692881, 23264222693009, 23264222693137, 23264222693265, 23264222693393, 23264222693521, 23264222693649, 23264222693777, 23264222693905, 23264222694033, 23264222694161, 23264222694289, 23264222694417, 23264222694545, 23264222694673, 23264222694801, 23264222694929, 23264222695057, 23264222695185, 23264222695313, 23264222695441, 23264222695569, 23264222695697, 23264229455249, 23264229455377, 23264229455505, 23264229455633, 23264229455761, 23264229455889, 23264229456017, 23264229456145, 23264229456273, 23264229456401, 23264229456529, 23264229456657, 23264229456785, 23264229456913, 23264229457041, 23264229457169, 23264229457297, 23264229457425, 23264229457553, 23264229457681, 23264229457809, 23264229457937, 23264229458065, 23264229458193, 23264229458321, 23264229458449, 23264229458577, 23264229458705, 23264229458833, 23264229458961, 23264229459089, 23264229459217, 23264229459345, 23264229459473, 23264229459601, 23264229459729, 23264229459857, 23264229459985, 23264229460113, 23264229460241, 23264229460369, 23264229460497, 23264229460625, 23264229460753, 23264229460881, 23264233318289, 23264233318417, 23264233318545, 23264233318673, 23264233318801, 23264233318929, 23264233319057, 23264233319185, 23264233319313, 23264233319441, 23264233319569, 23264233319697, 23264233319825, 23264233319953, 23264233320081, 23264233320209, 23264233320337, 23264233320465, 23264233320593, 23264233320721, 23264233320849, 23264233320977, 23264233321105, 23264233321233, 23264233321361, 23264233321489, 23264233321617, 23264233321745, 23264233321873, 23264233322001, 23264233322129, 23264233322257, 23264233322385, 23264233322513, 23264233322641, 23264233322769, 23264233322897, 23264233323025, 23264233323153, 23264233323281, 23264233323409, 23264233323537, 23264233323665, 23264233323793, 23264233323921, 23264233324049, 23264233647889, 23264233648017, 23264233648145, 23264233648273, 23264233648401, 23264233648529, 23264233648657, 23264233648785, 23264233648913, 23264233649041, 23264240582673, 23264240582801, 23264240582929, 23264240583057, 23264240583185, 23264240583313, 23264240583441, 23264240583569, 23264240583697, 23264240583825, 23264240583953, 23264240584081, 23264240584209, 23264240584337, 23264240584465, 23264240584593, 23264240584721, 23264240584849, 23264240584977, 23264240585105, 23264240585233, 23264240585361, 23264240585489, 23264240585617, 23264240585745, 23264240585873, 23264240586001, 23264257211281, 23264257211409, 23264257211537, 23264257211665, 23264257211793, 23264257211921, 23264257212049, 23264257212177, 23264257212305, 23264257212433, 23264257212561, 23264257212689, 23264257212817, 23264257212945, 23264257213073, 23264257213201, 23264257213329, 23264257213457, 23264257213585, 23264257213713, 23264257213841, 23264257213969, 23264257214097, 23264257214225, 23264257214353, 23264257214481, 23264257214609, 23264257214737, 23264263960593, 23264263960721, 23264263960849, 23264263960977, 23264263961105, 23264263961233, 23264263961361, 23264263961489, 23264263961617, 23264263961745, 23264263961873, 23264263962001, 23264263962129, 23264263962257, 23264263962385, 23264263962513, 23264263962641, 23264263962769, 23264263962897, 23264263963025, 23264263963153, 23264263963281, 23264263963409, 23264263963537, 23264263963665, 23264263963793, 23264263963921, 23264263964049, 23264263964177, 23264263964305, 23264263964433, 23264263964561, 23264263964689, 23264263964817, 23264263964945, 23264263965073, 23264263965201, 23264263965329, 23264263965457, 23264267521041, 23264267521169, 23264267521297, 23264267521425, 23264267521553, 23264267521681, 23264267521809, 23264267521937, 23264267522065, 23264267522193, 23264267522321, 23264267522449, 23264267522577, 23264267522705, 23264267522833, 23264267522961, 23264267523089, 23264267523217, 23264267523345, 23264267523473, 23264267523601, 23264267523729, 23264267523857, 23264267523985, 23264267524113, 23264267524241, 23264267524369, 23264267524497, 23264267524625, 23264267524753, 23264267524881, 23264267525009, 23264267525137, 23264267525265, 23264267525393, 23264267525521, 23264267525649, 23264267525777, 23264267525905, 23264267526033, 23264267526161, 23264267526289, 23264267526417, 23264267526545, 23264267526673, 23264267526801, 23264267526929, 23264267527057, 23264267527185, 23264267527313, 23264267527441, 23264267527569, 23264267527697, 23264267527825, 23264267527953, 23264267528081, 23264267528209, 23264267528337, 23264267528465, 23264267528593, 23264267528721, 23264267528849, 23264267528977, 23264267529105, 23264267529233, 23264267529361, 23264267529489, 23264267529617, 23264267529745, 23264267529873, 23264267530001, 23264267530129, 23264267530257, 23264267530385, 23264267530513, 23264267530641, 23264267530769, 23264267530897, 23264267531025, 23264267531153, 23264267531281, 23264267531409, 23264267531537, 23264267531665, 23264267531793, 23264267531921, 23264267532049, 23264267532177, 23264267532305, 23264267532433, 23264272742929, 23264272743057, 23264272743185, 23264272743313, 23264272743441, 23264272743569, 23264272743697, 23264272743825, 23264272743953, 23264272744081, 23264272744209, 23264272744337, 23264272744465, 23264272744593, 23264272744721, 23264272744849, 23264272744977, 23264272745105, 23264272745233, 23264272745361, 23264272745489, 23264272745617, 23264272745745, 23264281694481, 23264281694609, 23264281694737, 23264281694865, 23264281694993, 23264281695121, 23264281695249, 23264281695377, 23264281695505, 23264281695633, 23264281695761, 23264281695889, 23264281696017, 23264281696145, 23264281696273, 23264281696401, 23264281696529, 23264281696657, 23264281696785, 23264281696913, 23264281697041, 23264281697169, 23264281697297, 23264281697425, 23264281697553, 23264281697681, 23264281697809, 23264281697937, 23264281698065, 23264281698193, 23264281698321, 23264281698449, 23264281698577, 23264281698705, 23264281698833, 23264281698961, 23264281699089, 23264281699217, 23264281699345, 23264281699473, 23264281699601, 23264281699729, 23264281699857, 23264281699985, 23264281700113, 23264281700241, 23264281700369, 23264281700497, 23264281700625, 23264281700753, 23264281700881, 23264281701009, 23264281701137, 23264282443025, 23264282443153, 23264282443281, 23264282443409, 23264282443537, 23264282443665, 23264282443793, 23264282443921, 23264282444049, 23264282444177, 23264282444305, 23264282444433, 23264282444561, 23264282444689, 23264282444817, 23264282444945, 23264282445073, 23264282445201, 23264282445329, 23264282445457, 23264282445585, 23264282445713, 23264282445841, 23264282445969, 23264282446097, 23264282446225, 23264282446353, 23264282446481, 23264282446609, 23264282446737, 23264282446865, 23264282446993, 23264282447121, 23264282447249, 23264282447377, 23264282447505, 23264288381585, 23264288381713, 23264288381841, 23264288381969, 23264288382097, 23264288382225, 23264288382353, 23264288382481, 23264288382609, 23264288382737, 23264288382865, 23264288382993, 23264288383121, 23264288383249, 23264288383377, 23264288383505, 23264288383633, 23264288383761, 23264288383889, 23264288384017, 23264288384145, 23264288384273, 23264288384401, 23264288384529, 23264288384657, 23264288384785, 23264288384913, 23264288385041, 23264288385169, 23264288385297, 23264288385425, 23264288385553, 23264288385681, 23264288385809, 23264288385937, 23264288386065, 23264288386193, 23264288386321, 23264288386449, 23264288386577, 23264288386705, 23264288386833, 23264288386961, 23264288387089, 23264288387217, 23264288387345, 23264288387473, 23264293269137, 23264293269265, 23264293269393, 23264293269521, 23264293269649, 23264293269777, 23264293269905, 23264293270033, 23264293270161, 23264293270289, 23264293270417, 23264293270545, 23264293270673, 23264293270801, 23264293270929, 23264293271057, 23264293271185, 23264293271313, 23264293271441, 23264293271569, 23264293271697, 23264293271825, 23264293271953, 23264293272081, 23264293272209, 23264293272337, 23264293272465, 23264293272593, 23264293272721, 23264293272849, 23264293272977, 23264293273105, 23264293273233, 23264293273361, 23264293273489, 23264293273617, 23264300507537, 23264300507665, 23264300507793, 23264300507921, 23264300508049, 23264300508177, 23264300508305, 23264300508433, 23264300508561, 23264300508689, 23264300508817, 23264300508945, 23264300509073, 23264300509201, 23264300509329, 23264300509457, 23264300509585, 23264300509713, 23264300509841, 23264300509969, 23264301877393, 23264301877521, 23264301877649, 23264301877777, 23264301877905, 23264307737617, 23264307737745, 23264307737873, 23264307738001, 23264307738129, 23264307738257, 23264307738385, 23264307738513, 23264307738641, 23264307738769, 23264307738897, 23264307739025, 23264307739153, 23264307739281, 23264307739409, 23264307739537, 23264307739665, 23264307739793, 23264307739921, 23264307740049, 23264307740177, 23264308147089, 23264308147217, 23264308147345, 23264308147473, 23264308147601, 23264308147729, 23264308147857, 23264308147985, 23264308148113, 23264308148241, 23264308148369, 23264308148497, 23264308148625, 23264308148753, 23264308148881, 23264308149009, 23264308149137, 23264308149265, 23264308149393, 23264308149521, 23264308149649, 23264308149777, 23264308149905, 23264308150033, 23264308150161, 23264308150289, 23264308150417, 23264308150545, 23264308150673, 23264308150801, 23264308150929, 23264308151057, 23264308151185, 23264308151313, 23264308151441, 23264308151569, 23264308151697, 23264308151825, 23264308151953, 23264308152081, 23264308152209, 23264308152337, 23264308152465, 23264308152593, 23264308152721, 23264308152849, 23264308152977, 23264308153105, 23264308153233, 23264308153361, 23264308153489, 23264308153617, 23264308153745, 23264308153873, 23264308154001, 23264308154129, 23264308154257, 23264308154385, 23264308154513, 23264308154641, 23264308154769, 23264308154897, 23264308155025, 23264308155153, 23264308155281, 23264308155409, 23264329469841, 23264329469969, 23264329470097, 23264329470225, 23264329470353, 23264329470481, 23264329470609, 23264329470737, 23264329470865, 23264329470993, 23264329471121, 23264329471249, 23264329471377, 23264329471505, 23264329471633, 23264329471761, 23264329471889, 23264329472017, 23264329472145, 23264329472273, 23264329472401, 23264329472529, 23264329472657, 23264329472785, 23264329472913, 23264329473041, 23264329473169, 23264329473297, 23264329473425, 23264329473553, 23264329473681, 23264329473809, 23264329473937, 23264329474065, 23264329474193, 23264329474321, 23264329474449, 23264329474577, 23264329474705, 23264329474833, 23264329474961, 23264329475089, 23264329475217, 23264329475345, 23264329475473, 23264329475601, 23264329475729, 23264335287697, 23264335287825, 23264335287953, 23264335288081, 23264335288209, 23264335845777, 23264335845905, 23264335846033, 23264335846161, 23264335846289, 23264335846417, 23264335846545, 23264335846673, 23264335846801, 23264335846929, 23264335847057, 23264335847185, 23264335847313, 23264335847441, 23264335847569, 23264335847697, 23264335847825, 23264335847953, 23264335848081, 23264335848209, 23264335848337, 23264335848465, 23264335848593, 23264335848721, 23264335848849, 23264335848977, 23264335849105, 23264335849233, 23264335849361, 23264335849489, 23264335849617, 23264335849745, 23264335849873, 23264335850001, 23264340598033, 23264340598161, 23264340598289, 23264340598417, 23264340598545, 23264340598673, 23264340598801, 23264340598929, 23264340599057, 23264340599185, 23264340599313, 23264340599441, 23264340599569, 23264340599697, 23264340599825, 23264340599953, 23264340600081, 23264340600209, 23264340600337, 23264340600465, 23264340600593, 23264340600721, 23264340600849, 23264340600977, 23264340601105, 23264340601233, 23264340601361, 23264340601489, 23264340601617, 23264340601745, 23264340601873, 23264340602001, 23264340602129, 23264340602257, 23264340602385, 23264340602513, 23264340602641, 23264340602769, 23264340602897, 23264340603025, 23264340603153, 23264340603281, 23264340603409, 23264340603537, 23264340603665, 23264340603793, 23264340603921, 23264340604049, 23264340604177, 23264340604305, 23264340604433, 23264340604561, 23264340604689, 23264340604817, 23264340604945, 23264340605073, 23264340605201, 23264340605329, 23264340605457, 23264340605585, 23264340605713, 23264340605841, 23264340605969, 23264340606097, 23264341210257, 23264341210385, 23264341373969, 23264341374097, 23264341374225, 23264341374353, 23264341374481, 23264341374609, 23264341374737, 23264341374865, 23264341374993, 23264341375121, 23264341375249, 23264341375377, 23264341375505, 23264341375633, 23264341375761, 23264341375889, 23264341376017, 23264341376145, 23264341376273, 23264341376401, 23264341376529, 23264341376657, 23264341376785, 23264341376913, 23264341377041, 23264341377169, 23264341377297, 23264341377425, 23264341377553, 23264341377681, 23264341377809, 23264341377937, 23264341378065, 23264341378193, 23264341378321, 23264341378449, 23264341378577, 23264341378705, 23264341378833, 23264341378961, 23264341379089, 23264341379217, 23264341379345, 23264341379473, 23264341379601, 23264341379729, 23264341379857, 23264341379985, 23264341380113, 23264341380241, 23264341380369, 23264341380497, 23264341380625, 23264341380753, 23264341380881, 23264341381009, 23264341381137, 23264341381265, 23264341381393, 23264341381521, 23264341381649, 23264341400977, 23264341401105, 23264341401233, 23264341401361, 23264341401489, 23264341401617, 23264341401745, 23264341401873, 23264341402001, 23264341402129, 23264341402257, 23264341402385, 23264341402513, 23264341402641, 23264341402769, 23264341402897, 23264341403025, 23264341403153, 23264341403281, 23264341403409, 23264341403537, 23264341403665, 23264341403793, 23264341403921, 23264341404049, 23264341404177, 23264341404305, 23264341404433, 23264341404561, 23264341404689, 23264341404817, 23264341404945, 23264341405073, 23264341405201, 23264341405329, 23264341405457, 23264341405585, 23264341405713, 23264341405841, 23264341405969, 23264341406097, 23264341406225, 23264341406353, 23264341406481, 23264341406609, 23264341406737, 23264341406865, 23264341406993, 23264341407121, 23264341407249, 23264341407377, 23264341407505, 23264341616785, 23264341766033, 23264344322321, 23264344322449, 23264344322577, 23264344322705, 23264344322833, 23264344322961, 23264344323089, 23264344323217, 23264344323345, 23264344323473, 23264344323601, 23264344323729, 23264344323857, 23264344323985, 23264344324113, 23264344324241, 23264344324369, 23264344324497, 23264344324625, 23264344324753, 23264344324881, 23264344325009, 23264344325137, 23264344325265, 23264344325393, 23264344325521, 23264344325649, 23264344325777, 23264344325905, 23264344326033, 23264344326161, 23264344326289, 23264344326417, 23264344326545, 23264344326673, 23264344326801, 23264344326929, 23264344327057, 23264344327185, 23264344327313, 23264344327441, 23264344327569, 23264344327697, 23264344327825, 23264344327953, 23264344328081, 23264344328209, 23264344328337, 23264344328465, 23264344328593, 23264344328721, 23264344328849, 23264344328977, 23264344329105, 23264344329233, 23264344329361, 23264344329489, 23264344329617, 23264344329745, 23264344329873, 23264344330001, 23264344330129, 23264344330257, 23264344330385, 23264344330513, 23264344330641, 23264344330769, 23264344330897, 23264344331025, 23264344331153, 23264344331281, 23264344331409, 23264344331537, 23264344331665, 23264344331793, 23264344331921, 23264344332049, 23264344332177, 23264344332305, 23264344332433, 23264344332561, 23264344332689, 23264344332817, 23264344332945, 23264344333073, 23264344333201, 23264344333329, 23264344333457, 23264344333585, 23264350593553, 23264350593681, 23264350593809, 23264350593937, 23264350594065, 23264350594193, 23264350594321, 23264350594449, 23264350594577, 23264350594705, 23264350594833, 23264350594961, 23264350595089, 23264350595217, 23264350595345, 23264350595473, 23264350595601, 23264350595729, 23264350595857, 23264350595985, 23264350596113, 23264350596241, 23264350596369, 23264350596497, 23264350596625, 23264350596753, 23264350596881, 23264350597009, 23264350597137, 23264350597265, 23264350597393, 23264350597521, 23264350597649, 23264350597777, 23264351202833, 23264351202961, 23264351203089, 23264351203217, 23264351203345, 23264351203473, 23264351203601, 23264351203729, 23264351203857, 23264351203985, 23264351204113, 23264351204241, 23264351204369, 23264351204497, 23264351204625, 23264351204753, 23264351204881, 23264351205009, 23264351205137, 23264351205265, 23264351205393, 23264351205521, 23264351205649, 23264351205777, 23264351205905, 23264351206033, 23264351206161, 23264351206289, 23264351206417, 23264351206545, 23264351206673, 23264351206801, 23264351206929, 23264351207057, 23264351207185, 23264351207313, 23264351207441, 23264351207569, 23264351207697, 23264351207825, 23264351207953, 23264351208081, 23264351208209, 23264351208337, 23264351208465, 23264351208593, 23264351208721, 23264351208849, 23264351208977, 23264351209105, 23264351209233, 23264351209361, 23264351209489, 23264351209617, 23264351209745, 23264351209873, 23264351210001, 23264351210129, 23264353324433, 23264353324561, 23264353324689, 23264353324817, 23264353324945, 23264353325073, 23264353325201, 23264353325329, 23264353325457, 23264353325585, 23264353325713, 23264353325841, 23264353325969, 23264353326097, 23264353326225, 23264354945169, 23264354945297, 23264354945425, 23264354945553, 23264354945681, 23264354945809, 23264354945937, 23264354946065, 23264354946193, 23264354946321, 23264354946449, 23264354946577, 23264354946705, 23264354946833, 23264354946961, 23264354947089, 23264354947217, 23264354947345, 23264354947473, 23264354947601, 23264354947729, 23264354947857, 23264354947985, 23264354948113, 23264354948241, 23264354948369, 23264354948497, 23264354948625, 23264354948753, 23264354948881, 23264354949009, 23264354949137, 23264354949265, 23264354949393, 23264354949521, 23264354949649, 23264354949777, 23264354949905, 23264354950033, 23264354950161, 23264354950289, 23264354950417, 23264354950545, 23264354950673, 23264354950801, 23264354950929, 23264354951057, 23264354951185, 23264354951313, 23264354951441, 23264354951569, 23264354951697, 23264354951825, 23264354951953, 23264354952081, 23264354952209, 23264354952337, 23264354952465, 23264354952593, 23264354952721, 23264354952849, 23264354952977, 23264354953105, 23264354953233, 23264354953361, 23264354953489, 23264354953617, 23264354953745, 23264354953873, 23264354954001, 23264354954129, 23264354954257, 23264354954385, 23264354954513, 23264354954641, 23264354954769, 23264354954897, 23264354955025, 23264354955153, 23264354955281, 23264354955409, 23264354955537, 23264354955665, 23264354955793, 23264354955921, 23264354956049, 23264354956177, 23264354956305, 23264354956433, 23264354956561, 23264354956689, 23264354956817, 23264354956945, 23264354957073, 23264354957201, 23264354957329, 23264354957457, 23264354957585, 23264354957713, 23264354957841, 23264356296465, 23264356302481, 23264356302609, 23264357193873, 23264362938769, 23264362938897, 23264362939025, 23264362939153, 23264362939281, 23264362939409, 23264362939537, 23264362939665, 23264362939793, 23264362939921, 23264362940049, 23264362940177, 23264362940305, 23264362940433, 23264362940561, 23264362940689, 23264362940817, 23264362940945, 23264362941073, 23264362941201, 23264362941329, 23264362941457, 23264362941585, 23264362941713, 23264362941841, 23264362941969, 23264362942097, 23264362942225, 23264362942353, 23264362942481, 23264362942609, 23264362942737, 23264362942865, 23264362942993, 23264362943121, 23264362943249, 23264362943377, 23264362943505, 23264362943633, 23264362943761, 23264362943889, 23264362944017, 23264362944145, 23264362944273, 23264362944401, 23264362944529, 23264362944657, 23264362944785, 23264362944913, 23264362945041, 23264362945169, 23264362945297, 23264362945425, 23264362945681, 23264362945809, 23264381886609, 23264395416081, 23264395416209, 23264395416337, 23264395416465, 23264395416593, 23264404161169, 23264404311313, 23264405848721, 23264435577489, 23264435577617, 23264496072337, 23264496072465, 23264496072593, 23264496072721, 23264496072849, 23264496072977, 23264496073105, 23264496073233, 23264496073361, 23264496073489, 23264496073617, 23264496073745, 23264546272785, 23264546272913, 23264546273041, 23264546273169, 23264546273297, 23264546273425, 23264546273553, 23264546273681, 23264546273809, 23264546273937, 23264546274065, 23264546274193, 23264546274321, 23264546274449, 23264546274577, 23264546274705, 23264546274833, 23264546274961, 23264546275089, 23264546275217, 23264546275345, 23264546275473, 23264546275601, 23264601936273, 23264601936401, 23264601936529, 23264601936657, 23264601936785, 23264601936913, 23264601937041, 23264601937169, 23264601937297, 23264601937425, 23264601937553, 23264601937681, 23264601937809, 23264601937937, 23264601938065, 23264601938193, 23264601938321, 23264601938449, 23264601938577, 23264601938705, 23264601938833, 23264601938961, 23264601939089, 23264601939217, 23264612680337, 23264612680465, 23264612680593, 23264612680721, 23264612680849, 23264612680977, 23264612681105, 23264612681233, 23264612681361, 23264612681489, 23264612681617, 23264612681745, 23264612681873, 23264612682001, 23264612682129, 23264612682257, 23264612682385, 23264612682513, 23264612682641, 23264612682769, 23264612682897, 23264612683025, 23264612683153, 23264612683281, 23264612683409, 23264612683537, 23264612683665, 23264612683793, 23264612683921, 23264612684049, 23264612684177, 23264612684305, 23264612684433, 23264612684561, 23264612684689, 23264612684817, 23264612684945, 23264612685073, 23264612685201, 23264612685329, 23264612685457, 23264612685585, 23264612685713, 23264612685841, 23264612685969, 23264612686097, 23264612686225, 23264612686353, 23264612686481, 23264612686609, 23264612686737, 23264612686865, 23264612686993, 23264612687121, 23264612687249, 23264612687377, 23264612687505, 23264612687633, 23264612687761, 23264612687889, 23264612688017, 23264612688145, 23264612688273, 23264612688401, 23264612688529, 23264612688657, 23264612688785, 23264612688913, 23264612689041, 23264612689169, 23264612689297, 23264612689425, 23264612689553, 23264612689681, 23264612689809, 23264612689937, 23264622992529, 23264622992657, 23264622992785, 23264622992913, 23264622993041, 23264622993169, 23264622993297, 23264622993425, 23264622993553, 23264622993681, 23264622993809, 23264622993937, 23264622994065, 23264622994193, 23264653152145, 23264653152273, 23264653152401, 23264653152529, 23264653152657, 23264653152785, 23264653152913, 23264653153041, 23264653153169, 23264653153297, 23264653153425, 23264653153553, 23264653153681, 23264653153809, 23264653153937, 23264653154065, 23264653154193, 23264653154321, 23264653154449, 23264653154577, 23264653154705, 23264653154833, 23264653154961, 23264653155089, 23264653155217, 23264653155345, 23264653155473, 23264653155601, 23264653155729, 23264659120145, 23264659120273, 23264659120401, 23264659120529, 23264659120657, 23264659120785, 23264659120913, 23264659121041, 23264659121169, 23264659121297, 23264659121425, 23264659121553, 23264659121681, 23264659121809, 23264659121937, 23264659122065, 23264659122193, 23264659122321, 23264659122449, 23264659122577, 23264659122705, 23264659122833, 23264659122961, 23264659123089, 23264659123217, 23264659123345, 23264659123473, 23264659123601, 23264659123729, 23264659123857, 23264659123985, 23264659124113, 23264659124241, 23264659124369, 23264659124497, 23264659124625, 23264659124753, 23264659124881, 23264659125009, 23264659125137, 23264659125265, 23264659125393, 23264659125521, 23264659125649, 23264659125777, 23264659125905, 23264659126033, 23264659126161, 23264659126289, 23264726487057, 23264726487185, 23264726487313, 23264726487441, 23264726487569, 23264726487697, 23264726487825, 23264726487953, 23264726488081, 23264726488209, 23264726488337, 23264726488465, 23264726488593, 23264726488721, 23264726488849, 23264726488977, 23264726489105, 23264726489233, 23264726489361, 23264726489489, 23264726489617, 23264726489745, 23264726489873, 23264726490001, 23264726490129, 23264726490257, 23264726490385, 23264726490513, 23264726490641, 23264726490769, 23264726490897, 23264726491025, 23264726491153, 23264726491281, 23264726491409, 23264726491537, 23264726491665, 23264726491793, 23264726491921, 23264726492049, 23264726492177, 23264726492305, 23264726492433, 23264726492561, 23264726492689, 23264726492817, 23264726492945, 23264726493073, 23264726493201, 23264726493329, 23264726493457, 23264726493585, 23264726493713, 23264726493841, 23264726493969, 23264726494097, 23264841598865, 23264841598993, 23264841599121, 23264841599249, 23264841599377, 23264841599505, 23264841599633, 23264841599761, 23264841599889, 23264841600017, 23264841600145, 23264841600273, 23264841600401, 23264841600529, 23264841600657, 23264841600785, 23264841600913, 23264841601041, 23264841601169, 23264841601297, 23264841601425, 23264841601553, 23264841601681, 23264841601809, 23264841601937, 23264841602065, 23264841602193, 23264841602321, 23264841602449, 23264841602577, 23264841602705, 23264841602833, 23264841602961, 23264841603089, 23264841603217, 23264841603345, 23264841603473, 23264841603601, 23264841603729, 23264841603857, 23264841603985, 23264841604113, 23264841604241, 23264841604369, 23264841604497, 23264841604625, 23264841604753, 23264841604881, 23264841605009, 23264841605137, 23264841605265, 23264841605393, 23264841605521, 23264841605649, 23264841605777, 23264841605905, 23264841606033, 23264841606161, 23264841606289, 23264841606417, 23264841606545, 23264841606673, 23264841606801, 23264841606929, 23264841607057, 23264841607185, 23264841607313, 23264841607441, 23264841607569, 23264841607697, 23264841607825, 23264841607953, 23264841608081, 23264841608209, 23264841608337, 23264841608465, 23266445115409, 23266445795089, 23266445795217, 23266445795345, 23266445800337, 23266445800465, 23266445800593, 23266449449105, 23266449449361, 23266455209361, 23266455209489, 23266455209617, 23266455209745, 23266455209873, 23266455210001, 23266455210129, 23266455210257, 23266455210385, 23266455210513, 23266455210641, 23266455210769, 23266455210897, 23266455211025, 23266455211153, 23266455211281, 23266455211409, 23266455211537, 23266455211665, 23266455211793, 23266455211921, 23266455212049, 23266455212177, 23266455212305, 23266455212433, 23266455212561, 23266455212689, 23266455212817, 23266455212945, 23266455213073, 23266455213201, 23266455213329, 23266455213457, 23266455429009, 23266455435537, 23266455440017, 23266455440145, 23266455440273, 23266455440401, 23266455440529, 23266455440657, 23266455440785, 23266455440913, 23266455777041, 23266455777169, 23266455777297, 23266455784721, 23266456130321, 23266456509073, 23266458464273, 23266458464401]
#     user_data = []
    
#     for user_id in user_ids:
#         url = f"{base_url}{user_id}"
#         response = requests.delete(url, headers=headers)
#         if response.status_code == 200:
#             user_data.append(response.json())
#         else:
#             user_data.append({"error": f"Failed to fetch data for user ID {user_id}"})
    
#     return JsonResponse({"users": user_data})


# import base64
# import requests
# from rest_framework.views import APIView
# from django.http import JsonResponse



