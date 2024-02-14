from translate import dad_joke, dutch_bot

text = '''
The Second War of Scottish Independence broke out in 1332 when Edward Balliol led an English-backed invasion of Scotland. Balliol, the son of former Scottish king John Balliol, was attempting to make good his claim to the Scottish throne. He was opposed by Scots loyal to the occupant of the throne, eight-year-old David II. At the Battle of Dupplin Moor Balliol's force defeated a Scottish army ten times their size and Balliol was crowned king. Within three months David's partisans had regrouped and forced Balliol out of Scotland. He appealed to the English king, Edward III, who invaded Scotland in 1333 and besieged the important trading town of Berwick. A large Scottish army attempted to relieve it but was heavily defeated at the Battle of Halidon Hill. Balliol established his authority over most of Scotland, ceded to England the eight counties of south-east Scotland and did homage to Edward for the rest of the country as a fief.

As allies of Scotland via the Auld Alliance, the French were unhappy about an English expansion into Scotland and so covertly supported and financed David's loyalists. Balliol's allies fell out among themselves and he lost control of most of Scotland again by late 1334. In early 1335 the French attempted to broker a peace. However, the Scots were unable to agree on a position and Edward prevaricated while building a large army. He invaded in July and again overran most of Scotland. Tensions with France increased. Further French-sponsored peace talks failed in 1336 and in May 1337 the French king, Philip VI, engineered a clear break between France and England, starting the Hundred Years' War. The Anglo-Scottish war became a subsidiary theatre of this larger Anglo-French war. Edward sent what troops he could spare to Scotland, in spite of which the English slowly lost ground in Scotland as they were forced to focus on the French theatre. Achieving his majority David returned to Scotland from France in 1341 and by 1342 the English had been cleared from north of the border.

In 1346 Edward led a large English army through northern France, sacking Caen, defeating the French at Crécy and besieging Calais. In response to Philip's urgent requests, David invaded England believing most of its previous defenders were in France. He was surprised by a smaller but nonetheless sizable English force, which crushed the Scots at the Battle of Neville's Cross and captured David. This, and the resulting factional politics in Scotland, prevented further large-scale Scottish attacks. A concentration on France similarly kept the English quiescent, while possible terms for David's release were discussed at length. In late 1355 a large Scottish raid into England, in breach of truce, provoked another invasion from Edward in early 1356. The English devastated Lothian but winter storms scattered their supply ships and they were forced to retreat. The following year the Treaty of Berwick was signed, which ended the war; the English dropped their claim of suzerainty, while the Scots acknowledged a vague English overlordship. A cash ransom was negotiated for David's release: 100,000 marks, to be paid over ten years. The treaty prohibited any Scottish citizen from bearing arms against Edward III or any of his men until the sum was paid in full and the English were supposed to stop attacking Scotland. This effectively ended the war, and while intermittent fighting continued, the truce was broadly observed for forty years.

'''

result = dad_joke('tell me a joke')
print (dir(result))

while True:

  result = dutch_bot(text)
  print ('translated', result.result[:50])
  print ('error', result.error_occurred)
  if result.error_occurred:
    print(result.last_error_description)
    break
