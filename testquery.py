from bs4 import BeautifulSoup
import urllib.request
from pymongo import MongoClient

class CodeSearch:
	def __init__(self, code):
		self.code = code
		self.legit = True
		self.search_url = "https://www.healthcarebluebook.com/page_SearchResults.aspx?SearchTerms=" + code + "&tab=ShopForCare"
		self.get_price_page()
		if self.legit:
			self.get_price()

	def get_price_page(self):
		response = urllib.request.urlopen(self.search_url)
		soup = BeautifulSoup(response, 'html.parser')
		legit = soup.findAll("h3", {"class": "physician"})
		print(legit)
		if len(legit) == 0:
			self.legit = False
		mydivs = soup.findAll("div", {"class": "service-name"})
		for div in mydivs:
			a_s = div.find_all('a')
			self.price_page = a_s[0]['href']
			break
		self.price_page = "https://www.healthcarebluebook.com/page_ProcedureDetails.aspx?" + self.price_page.split("?",1)[1] 
		print(self.price_page)

	def get_price(self):
		response = urllib.request.urlopen(self.price_page)
		soup = BeautifulSoup(response, 'html.parser')
		mydivs = soup.findAll("div", {"class": "fee-detail-row"})
		#print(soup)
		div = mydivs[0]
		values = div.findAll("div", {"class": "value"})
		self.procedure_desc = values[0].text
		self.fair_price = values[1].text.split("$", 1)[1]
		self.low_price = soup.findAll("span", {"class": "fair"})[0].text.split("$", 1)[1]
		self.high_price = soup.findAll("span", {"class": "not-fair"})[0].text.split("$", 1)[1].split("\r", 1)[0]
		self.procedure = soup.findAll("div", {"class": "fair-price-results-summary"})[0].findAll("h3")[0].text
		#print(self.procedure + ": " + self.low_price + " " + self.high_price)

	def return_values(self):
		return {
			"code" : self.code,
			"procedure" : self.procedure,
			"description" : self.procedure_desc,
			"fair_price" : self.fair_price,
			"low_price" : self.low_price,
			"high_price" : self.high_price,
		}

codes = [70480, 70481, 70482, 70486, 70487, 70488, 70490, 70491, 70492, 73700, 73701, 73702, 70450, 70460, 70470, 72125, 72126, 72127, 71250, 71260, 71270, 72128, 72129, 72130, 74176, 74177, 74178, 72131, 72132, 72133, 70540, 70543, 70336, 73221, 73222, 73223, 73218, 73220, 73721, 73722, 73723, 73718, 73720, 70551, 70553, 72141, 72156, 71550, 71552, 77059, 72146, 72157, 74181, 74183, 72148, 72158, 72195, 72197]
# codes = [
# "86152",
# "86153",
# "86890",
# "86891",
# "86927",
# "86930",
# "86931",
# "86932",
# "86945",
# "86950",
# "86960",
# "86965",
# "86985",
# "0008M",
# "0357T",
# "0058T",
# "0111T",
# "36415",
# "78110",
# "78111",
# "78120",
# "78121",
# "78122",
# "78130",
# "78191",
# "78267",
# "78268",
# "78270",
# "78271",
# "78272",
# "78725",
# "G0027",
# "G0103",
# "G0123",
# "G0124",
# "G0141",
# "G0143",
# "G0144",
# "G0145",
# "G0147",
# "G0148",
# "G0306",
# "G0307",
# "G0328",
# "G0416",
# "G0432",
# "G0433",
# "G0435",
# "G0475",
# "G0476",
# "G9143",
# "P2028",
# "P2029",
# "P2033",
# "P2038",
# "P3000",
# "P3001",
# "P9612",
# "P9615",
# "Q0111",
# "Q0112",
# "Q0113",
# "Q0114",
# "Q0115",
# "64550",
# "90901",
# "90911",
# "92507",
# "92508",
# "92520",
# "92521",
# "92522",
# "92523",
# "92524",
# "92526",
# "92597",
# "92607",
# "92608",
# "92609",
# "92610",
# "92611",
# "92612",
# "92614",
# "92616",
# "93797",
# "93798",
# "95831",
# "95832",
# "95833",
# "95834",
# "95851",
# "95852",
# "95992",
# "96000",
# "96001",
# "96002",
# "96003",
# "96105",
# "96111",
# "96125",
# "97010",
# "97012",
# "97016",
# "97018",
# "97022",
# "97024",
# "97026",
# "97028",
# "97032",
# "97033",
# "97034",
# "97035",
# "97036",
# "97039",
# "97110",
# "97112",
# "97113",
# "97116",
# "97124",
# "97139",
# "97140",
# "97150",
# "97161",
# "97162",
# "97163",
# "97164",
# "97165",
# "97166",
# "97167",
# "97168",
# "97530",
# "97532",
# "97533",
# "97535",
# "97537",
# "97542",
# "97545",
# "97546",
# "97597",
# "97598",
# "97602",
# "97605",
# "97606",
# "97607",
# "97608",
# "97610",
# "97750",
# "97755",
# "97760",
# "97761",
# "97762",
# "97799",
# "G0281",
# "G0283",
# "G0329",
# "G0451",
# "G0460",
# "0042T",
# "0159T",
# "0174T",
# "0175T",
# "0330T",
# "0331T",
# "0332T",
# "0346T",
# "0422T",
# "51798",
# "70100",
# "70110",
# "70120",
# "70130",
# "70134",
# "70140",
# "70150",
# "70160",
# "70190",
# "70200",
# "70210",
# "70220",
# "70240",
# "70250",
# "70260",
# "70300",
# "70310",
# "70320",
# "70328",
# "70330",
# "70336",
# "70350",
# "70355",
# "70360",
# "70370",
# "70371",
# "70380",
# "70450",
# "70460",
# "70470",
# "70480",
# "70481",
# "70482",
# "70486",
# "70487",
# "70488",
# "70490",
# "70491",
# "70492",
# "70496",
# "70498",
# "70540",
# "70542",
# "70543",
# "70544",
# "70545",
# "70546",
# "70547",
# "70548",
# "70549",
# "70551",
# "70552",
# "70553",
# "70554",
# "70555",
# "71010",
# "71015",
# "71020",
# "71021",
# "71022",
# "71023",
# "71030",
# "71034",
# "71035",
# "71100",
# "71101",
# "71110",
# "71111",
# "71120",
# "71130",
# "71250",
# "71260",
# "71270",
# "71275",
# "71550",
# "71551",
# "71552",
# "71555",
# "72020",
# "72040",
# "72050",
# "72052",
# "72070",
# "72072",
# "72074",
# "72080",
# "72081",
# "72082",
# "72083",
# "72084",
# "72100",
# "72110",
# "72114",
# "72120",
# "72125",
# "72126",
# "72127",
# "72128",
# "72129",
# "72130",
# "72131",
# "72132",
# "72133",
# "72141",
# "72142",
# "72146",
# "72147",
# "72148",
# "72149",
# "72156",
# "72157",
# "72158",
# "72159",
# "72170",
# "72190",
# "72191",
# "72192",
# codes = [
# "72193",
# "72194",
# "72195",
# "72196",
# "72197",
# "72198",
# "72200",
# "72202",
# "72220",
# "73000",
# "73010",
# "73020",
# "73030",
# "73050",
# "73060",
# "73070",
# "73080",
# "73090",
# "73092",
# "73100",
# "73110",
# "73120",
# "73130",
# "73140",
# "73200",
# "73201",
# "73202",
# "73206",
# "73218",
# "73219",
# "73220",
# "73221",
# "73222",
# "73223",
# "73225",
# "73501",
# "73502",
# "73503",
# "73521",
# "73522",
# "73523",
# "73551",
# "73552",
# "73560",
# "73562",
# "73564",
# "73565",
# "73590",
# "73592",
# "73600",
# "73610",
# "73620",
# "73630",
# "73650",
# "73660",
# "73700",
# "73701",
# "73702",
# "73706",
# "73718",
# "73719",
# "73720",
# "73721",
# "73722",
# "73723",
# "73725",
# "74000",
# "74010",
# "74020",
# "74022",
# "74150",
# "74160",
# "74170",
# "74174",
# "74175",
# "74176",
# "74177",
# "74178",
# "74181",
# "74182",
# "74183",
# "74185",
# "74210",
# "74220",
# "74230",
# "74240",
# "74241",
# "74245",
# "74246",
# "74247",
# "74249",
# "74250",
# "74261",
# "74262",
# "74290",
# "74710",
# "74712",
# "75557",
# "75559",
# "75561",
# "75563",
# "75565",
# "75571",
# "75572",
# "75573",
# "75574",
# "75635",
# "76000",
# "76010",
# "76100",
# "76101",
# "76102",
# "76120",
# "76125",
# "76376",
# "76377",
# "76380",
# "76499",
# "76506",
# "76510",
# "76511",
# "76512",
# "76513",
# "76514",
# "76516",
# "76519",
# "76536",
# "76604",
# "76641",
# "76642",
# "76700",
# "76705",
# "76706",
# "76770",
# "76775",
# "76776",
# "76800",
# "76801",
# "76802",
# "76805",
# "76810",
# "76811",
# "76812",
# "76815",
# "76816",
# "76818",
# "76819",
# "76820",
# "76821",
# "76825",
# "76826",
# "76827",
# "76828",
# "76856",
# "76857",
# "76870",
# "76881",
# "76882",
# "76885",
# "76886",
# "76970",
# "76977",
# "76999",
# "77058",
# "77059",
# "77061",
# "77062",
# "77063",
# "77065",
# "77066",
# "77067",
# "77071",
# "77072",
# "77073",
# "77074",
# "77075",
# "77076",
# "77077",
# "77078",
# "77080",
# "77081",
# "77084",
# "77085",
# "77086",
# "78012",
# "78013",
# "78014",
# "78015",
# "78016",
# "78018",
# "78020",
# "78070",
# "78071",
# "78072",
# "78075",
# "78099",
# "78102",
# "78103",
# "78104",
# "78135",
# "78140",
# "78185",
# "78190",
# "78195",
# "78199",
# "78201",
# "78202",
# "78205",
# "78206",
# "78215",
# "78216",
# "78226",
# "78227",
# "78230",
# "78231",
# "78232",
# "78258",
# "78261",
# "78262",
# "78264",
# "78265",
# "78266",
# "78278",
# "78282",
# "78290",
# "78291",
# "78299",
# "78300",
# "78305",
# "78306",
# "78315",
# "78320",
# "78399",
# "78428",
# "78445",
# "78451",
# "78452",
# "78453",
# "78454",
# "78456",
# "78457",
# "78458",
# "78459",
# "78466",
# "78468",
# "78469",
# "78472",
# "78473",
# "78481",
# "78483",
# "78491",
# "78492",
# "78494",
# "78496",
# "78499",
# "78579",
# "78580",
# "78582",
# "78597",
# "78598",
# "78599",
# "78600",
# "78601",
# "78605",
# "78606",
# "78607",
# "78608",
# "78610",
# "78630",
# "78635",
# "78645",
# "78647",
# "78650",
# "78660",
# "78699",
# "78700",
# "78701",
# "78707",
# "78708",
# "78709",
# "78710",
# "78730",
# "78740",
# "78761",
# "78799",
# "78800",
# "78801",
# "78802",
# "78803",
# "78804",
# "78805",
# "78806",
# "78807",
# "78811",
# "78812",
# "78813",
# "78814",
# "78815",
# "78816",
# "78999",
# "91110",
# "91111",
# "92132",
# "92133",
# "92134",
# "92227",
# "92228",
# "93303",
# "93304",
# "93306",
# "93307",
# "93308",
# "93320",
# "93321",
# "93325",
# "93875",
# "93880",
# "93882",
# "93886",
# "93888",
# "93890",
# "93892",
# "93922",
# "93923",
# "93924",
# "93925",
# "93926",
# "93930",
# "93931",
# "93965",
# "93970",
# "93971",
# "93975",
# "93976",
# "93978",
# "93979",
# "93980",
# "93981",
# "93990",
# "93998",
# "97610",
# "A4641",
# "A4642",
# "A9500",
# "A9501",
# "A9502",
# "A9503",
# "A9504",
# "A9505",
# "A9507",
# "A9508",
# "A9509",
# "A9510",
# "A9512",
# "A9515",
# "A9516",
# "A9521",
# "A9524",
# "A9526",
# "A9528",
# "A9529",
# "A9531",
# "A9532",
# "A9536",
# "A9537",
# "A9538",
# "A9539",
# "A9540",
# "A9541",
# "A9542",
# "A9546",
# "A9547",
# "A9548",
# "A9550",
# "A9551",
# "A9552",
# "A9553",
# "A9554",
# "A9555",
# "A9556",
# "A9557",
# "A9558",
# "A9559",
# "A9560",
# "A9561",
# "A9562",
# "A9566",
# "A9567",
# "A9568",
# "A9569",
# "A9570",
# "A9571",
# "A9572",
# "A9576",
# "A9577",
# "A9578",
# "A9579",
# "A9580",
# "A9584",
# "A9586",
# "A9587",
# "A9588",
# "A9597",
# "A9598",
# "A9700",
# "A9520",
# "C9457",
# "C9461",
# "C9734",
# "C9744",
# "G0130",
# "G0202",
# "G0204",
# "G0206",
# "G0279",
# "G0288",
# "G0297",
# "G0389",
# "Q0092",
# "Q9951",
# "Q9953",
# "Q9954",
# "Q9955",
# "Q9956",
# "Q9957",
# "Q9958",
# "Q9959",
# "Q9960",
# "Q9961",
# "Q9962",
# "Q9963",
# "Q9964",
# "Q9965",
# "Q9966",
# "Q9967",
# "Q9982",
# "Q9983",
# "R0070",
# "R0075",
# "0190T",
# "0394T",
# "0395T",
# "19296",
# "19297",
# "19298",
# "20555",
# "31643",
# "32553",
# "32701",
# "41019",
# "49327",
# "49411",
# "49412",
# "55875",
# "55876",
# "55920",
# "57155",
# "57156",
# "58346",
# "61770",
# "61796",
# "61797",
# "61798",
# "61799",
# "61800",
# "63620",
# "63621",
# "77261",
# "77262",
# "77263",
# "77280",
# "77285",
# "77290",
# "77295",
# "77299",
# "77300",
# "77301",
# "77306",
# "77307",
# "77316",
# "77317",
# "77318",
# "77321",
# "77331",
# "77332",
# "77333",
# "77334",
# "77336",
# "77338",
# "77370",
# "77371",
# "77372",
# "77373",
# "77385",
# "77386",
# "77399",
# "77401",
# "77402",
# "77407",
# "77412",
# "77417",
# "77422",
# "77423",
# "77427",
# "77431",
# "77432",
# "77435",
# "77470",
# "77499",
# "77520",
# "77522",
# "77523",
# "77525",
# "77600",
# "77605",
# "77610",
# "77615",
# "77620",
# "77750",
# "77761",
# "77762",
# "77763",
# "77767",
# "77768",
# "77770",
# "77771",
# "77772",
# "77776",
# "77778",
# "77785",
# "77786",
# "77789",
# "77790",
# "77799",
# "79005",
# "79101",
# "79200",
# "79300",
# "79403",
# "79440",
# "79445",
# "79999",
# "92974",
# "A4650",
# "A9517",
# "A9527",
# "A9530",
# "A9543",
# "A9563",
# "A9564",
# "A9600",
# "A9604",
# "A9606",
# "A9699",
# "C1716",
# "C1717",
# "C1719",
# "C2616",
# "C2634",
# "C2635",
# "C2636",
# "C2638",
# "C2639",
# "C2640",
# "C2641",
# "C2642",
# "C2643",
# "C2644",
# "C2645",
# "C2698",
# "C2699",
# "C9734",
# "G0173",
# "G0251",
# "G0339",
# "G0340",
# "G6001",
# "G6002",
# "G6003",
# "G6004",
# "G6005",
# "G6006",
# "G6007",
# "G6008",
# "G6009",
# "G6010",
# "G6011",
# "G6012",
# "G6013",
# "G6014",
# "G6015",
# "G6016",
# "G6017",
# "Q3001",
# "77063",
# "77067",
# "80061",
# "82270",
# "82465",
# "82947",
# "82950",
# "82951",
# "83718",
# "84478",
# "G0103",
# "G0106",
# "G0118",
# "G0120",
# "G0123",
# "G0124",
# "G0141",
# "G0143",
# "G0144",
# "G0145",
# "G0147",
# "G0148",
# "G0202",
# "G0328",
# "G0389",
# "G0432",
# "G0433",
# "G0435",
# "G0464",
# "G0475",
# "G0476",
# "G0499",
# "P3000",
# "P3001",
# "90630",
# "90654",
# "90655",
# "90656",
# "90657",
# "90660",
# "90661",
# "90662",
# "90670",
# "90672",
# "90673",
# "90674",
# "90685",
# "90686",
# "90687",
# "90688",
# "90732",
# "90740",
# "90743",
# "90744",
# "90746",
# "90747",
# "Q2034",
# "Q2035",
# "Q2036",
# "Q2037",
# "Q2038",
# "Q2039"
# ]
for code in codes:
	strcode = str(code)
	try:
		a = CodeSearch(strcode)
		if a.legit:
			client = MongoClient('mongodb://foo:bar@ds125198.mlab.com:25198/codelookup')
			db = client.codelookup
			collection = db.procedures
			post = a.return_values()
			post_id = collection.insert_one(post).inserted_id
	except:
		print('bad')
		continue